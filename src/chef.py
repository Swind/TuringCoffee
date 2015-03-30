from utils import json_config
import msgpack

from threading import Thread
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

class Chef(object):
    def __init__(self):
        self.heater_temperature = 0
        self.is_water_full = False
        self.total_cmd = 0
        self.printer_progress = 0
        self.printer_state = 0
        self.printer_state_string = ""

        logger.info("Start printer server ...")
        printer_server = PrinterServer()
        printer_server_thread = Thread(target=printer_server.start)
        printer_server_thread.daemon = True
        printer_server_thread.start()

        logger.info("Start heater server ...")
        heater_server = HeaterServer()
        heater_server_thread = Thread(target=heater_server.start)
        heater_server_thread.daemon = True
        heater_server_thread.start()

        logger.info("Start refill server ...")
        refill_server = RefillServer()
        refill_server_thread = Thread(target=refill_server.start)
        refill_server_thread.daemon = True
        refill_server_thread.start()

        # Read config
        self.config = json_config.parse_json("config.json")

        # Create nanomsg socket to publish status and receive command
        cfg = self.config["PrinterServer"]
        self.printer_cmd = channel.Channel(cfg["Command_Socket_Address"], "Pair", False)
        self.printer_pub = channel.Channel(cfg["Publish_Socket_Address"], "Sub", False)

        cfg = self.config["HeaterServer"]
        self.heater_cmd = channel.Channel(cfg["Command_Socket_Address"], "Pair", False)
        self.heater_pub = channel.Channel(cfg["Publish_Socket_Address"], "Sub", False)

        cfg = self.config["RefillServer"]
        self.refill_cmd = channel.Channel(cfg["Command_Socket_Address"], "Pair", False)
        self.refill_pub = channel.Channel(cfg["Publish_Socket_Address"], "Sub", False)

        self.temperature_worker = Thread(target=self.__temperature_monitor)
        self.temperature_worker.daemon = True
        self.temperature_worker.start()

        self.water_level_worker = Thread(target=self.__water_level_monitor)
        self.water_level_worker.daemon = True
        self.water_level_worker.start()

        self.printer_worker = Thread(target=self.__printer_monitor)
        self.printer_worker.daemon = True
        self.printer_worker.start()

    def __temperature_monitor(self):
        while True:
            resp = self.heater_pub.recv()
            temperature = resp["temperature"]
            logger.debug("Now temperature {}".format(resp))
            self.heater_temperature = temperature

    def __water_level_monitor(self):
        while True:
            logger.info("Now water level {}".format(self.is_water_full))
            is_water_full = self.refill_pub.recv()["full"]
            self.is_water_full = is_water_full

    def __printer_monitor(self):
        while True:
            data = self.printer_pub.recv()
            logging.debug("Printer monitor receive {}".format(data))

            if "total" in data:
                self.total_cmd = data["total"]

            if "progress" in data:
                self.printer_progress = data["progress"]

            if "state" in data:
                self.printer_state = data["state"]
                self.printer_state_string = data["state_string"]

    def cook(self, cookbook_name):
        cmgr = CookbookManager()
        cookbook = Cookbook(cookbook_name, cmgr.read(cookbook_name))

        logger.debug("Chef look the cookbook")
        for step in cookbook.steps():
            logger.debug("# Start step {}".format(step.title))
            for process in step.processes:
                logger.debug("## Start process {}".format(process.title))
                for block in process.blocks:
                    logger.debug("### Start block {}".format(block.lang))
                    points = block.points()
                    self.handle(points)

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

    def handle(self, points):
        cmd_count = 0

        for point in points:

            logger.debug("Handle command {}".format(point))

            if type(point) is Point:
                gcode = self.__convert_to_gcode(point)
                self.printer_cmd.send({"G": gcode})
                cmd_count = cmd_count + 1

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

        if cmd_count:
            self.wait_printer_operational()
            self.printer_cmd.send({"START": True})
            self.wait_printer(cmd_count)

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
            logger.debug("Now temperature {}, waiting to {}".format(self.temperature, value))
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

