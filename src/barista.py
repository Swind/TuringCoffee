from utils import json_config
import msgpack

from threading import Thread
import Queue
import time

from cookbook_manager import CookbookManager
from cookbook import Cookbook

from process.process import Point
from process.process import Command
from process.process import Process

from printer_server import PrinterServer
from heater_server import HeaterServer
from refill_server import RefillServer

from nanomsg import (
    SUB,
    SUB_SUBSCRIBE,
    PAIR,
    DONTWAIT,
    Socket
)

from utils import channel

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

class Barista(object):
    IDLE = "Idle"
    BREWING = "Brewing"

    def __init__(self):
        self.heater_temperature = 0
        self.is_water_full = False
        self.total_cmd = 0
        self.state = self.IDLE
        self.printer_progress = 0
        self.printer_state = 0
        self.printer_state_string = ""

        self.now_cookbook_name = ""
        self.now_step = ""
        self.now_step_index = 0
        self.now_process = ""
        self.now_process_index = 0

        self.brew_queue = Queue.Queue()

        logger.info("Start printer server ...")
        printer_server = PrinterServer()
        printer_server_thread = self.__start_worker(target=printer_server.start)

        logger.info("Start heater server ...")
        heater_server = HeaterServer()
        heater_server_thread = self.__start_worker(target=heater_server.start)

        logger.info("Start refill server ...")
        refill_server = RefillServer()
        refill_server_thread = self.__start_worker(target=refill_server.start)

        # Read config
        self.config = json_config.parse_json("config.json")

        # Create nanomsg socket to publish status and receive command
        logger.info("Connect to printer server ...")
        cfg = self.config["PrinterServer"]
        self.printer_cmd = channel.Channel(cfg["Command_Socket_Address"], "Pair", False)
        self.printer_pub = channel.Channel(cfg["Publish_Socket_Address"], "Sub", False)

        logger.info("Connect to heater server ...")
        cfg = self.config["HeaterServer"]
        self.heater_cmd = channel.Channel(cfg["Command_Socket_Address"], "Pair", False)
        self.heater_pub = channel.Channel(cfg["Publish_Socket_Address"], "Sub", False)

        logger.info("Connect to refill server ...")
        cfg = self.config["RefillServer"]
        self.refill_cmd = channel.Channel(cfg["Command_Socket_Address"], "Pair", False)
        self.refill_pub = channel.Channel(cfg["Publish_Socket_Address"], "Sub", False)

        logger.info("Start monitor workers ...")
        self.temperature_worker = self.__start_worker(self.__temperature_monitor)
        self.water_level_worker = self.__start_worker(self.__water_level_monitor)
        self.printer_worker = self.__start_worker(self.__printer_monitor)
        self.brew_worker = self.__start_worker(self.__brew_worker)

    def __start_worker(self, target):
        worker = Thread(target=target)
        worker.daemon = True
        worker.start()

        return worker

    def __temperature_monitor(self):
        while True:
            resp = self.heater_pub.recv()
            temperature = resp.get("temperature", None)
            self.heater_temperature = temperature

            logger.debug("Receive new temperature {}".format(resp))

    def __water_level_monitor(self):
        while True:
            resp = self.refill_pub.recv()
            self.is_water_full = resp.get("full", None)

            logger.debug("Receive new water level {}".format(self.is_water_full))

    def __printer_monitor(self):
        while True:
            data = self.printer_pub.recv()
            logging.debug("Receive message from printer: {}".format(data))

            if "total" in data:
                self.total_cmd = data["total"]

            if "progress" in data:
                self.printer_progress = data["progress"]

            if "state" in data:
                self.printer_state = data["state"]
                self.printer_state_string = data["state_string"]

    def __change_state(self, state):
        logger.info("Barista change state from {} to {}".format(self.state, state))
        self.state = state

    def __brew_worker(self):
        while True:
            cookbook_name = self.brew_queue.get()

            logger.info("Start to cook {}".format(cookbook_name))
            self.__change_state(self.BREWING)
            self.now_cookbook_name = cookbook_name
            self.__brew(cookbook_name)
            self.__change_state(self.IDLE)

    def __brew(self, cookbook_name):
        cmgr = CookbookManager()
        cookbook = cmgr.get(cookbook_name)

        logger.debug("Barista look the cookbook")
        self.wait_printer_operational()

        self.__init_printer()
        for step_index, step in enumerate(cookbook.steps):
            logger.debug("# Start step {}".format(step.title))
            self.now_step = step.title
            self.now_step_index = step_index

            for process_index, process in enumerate(step.processes):
                logger.debug("## Start process {}".format(process.title))
                self.now_process = process.title
                self.now_process_index = process_index

                for block in process.blocks:
                    logger.debug("### Start block {}".format(block.lang))
                    self.handle_block(block)

        self.now_step = ""
        self.now_step_index = 0

        self.now_process = ""
        self.now_process_index = 0

    def __init_printer(self):
        self.printer_cmd.send({"C": "G21"})
        self.printer_cmd.send({"C": "G28"})
        self.printer_cmd.send({"C": "G90"})
        self.printer_cmd.send({"C": "M83"})

    def __convert_to_gcode(self, point):
        gcode = "G1"
        if point.x is not None:
            gcode = gcode + " X{}".format(point.x)

        if point.y is not None:
            gcode = gcode + " Y{}".format(point.y)

        if point.z is not None:
            gcode = gcode + " Z{}".format(point.z)

        if point.e1 is not None:
            gcode = gcode + " E{}".format(point.e1)

        if point.f is not None:
            gcode = gcode + " F{}".format(point.f)

        return gcode

    def brew(self, name):
        self.brew_queue.put(name)

    def handle_block(self, block):
        points = block.points()
        cmd_count = 0

        gcodes = []
        for point in points:

            if type(point) is Point:
                gcode = self.__convert_to_gcode(point)
                logger.debug("send command {}".format(gcode))
                gcodes.append(gcode)

            elif type(point) is Command:

                cmd = point.command
                value = point.value

                if cmd == "Home":
                    self.printer.cmd.send({"C": "G28"})

                elif cmd == "Refill":
                    self.refill.cmd.send({"Refill": True})
                    self.wait_refill()

                elif cmd == "Heat":
                    # Wait temperature to target temperature
                    self.wait_temperature(value)

        if gcodes:
            self.wait_printer_operational()
            self.printer_cmd.send({"G": gcodes})
            self.printer_cmd.send({"START": True})
            self.wait_printer(cmd_count)

    def printer_jog(self, x, y, z, e1, e2, f):
        point = Point(x, y, z, e1, e2, f)
        self.printer_cmd.send({"C": self.__convert_to_gcode(point)})
        return
    # ===============================================================================
    #
    # Waitting
    #
    # ===============================================================================
    def wait_printer_operational(self):
        while self.printer_state_string != "Operational":
            logger.debug("Wait printer state from {} to Operational".format(self.printer_state_string))
            time.sleep(2)

    def wait_temperature(self, value):
        payload = {
            "cycle_time": 1,
            "k": 44,
            "i": 165,
            "d": 4,
            "set_point": value
        }

        self.heater_cmd.send(payload)

        # Wait the tempature
        while not ((value - 0.5) < self.temperature < (value + 0.5)):
            logger.debug("Waiting temperature to {}".format(self.temperature, value))
            time.sleep(2)

    def wait_refill(self):
        self.refill_cmd.send({"Refill": True})

        # Wait refill finished
        while not self.is_water_full:
            logger.debug("Now water level is {}, waiting to full".format(self.is_water_full))
            time.sleep(2)

    def wait_printer(self, cmd_count):
        while not (self.printer_progress == cmd_count and self.total_cmd == cmd_count):
            logger.debug("Now printer total cmd {}, progress {}, wait it to {}".format(self.total_cmd, self.printer_progress, cmd_count))
            time.sleep(1)

