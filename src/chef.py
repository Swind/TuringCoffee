from utils import json_config
import msgpack

from threading import Thread
import time

from cookbook_manager import CookbookManager
from cookbook import Cookbook

from process.process import Point
from process.process import Command
from process.process import Process

from nanomsg import (
    SUB,
    SUB_SUBSCRIBE,
    PAIR,
    DONTWAIT,
    Socket
)

from utils import channel


class Chef(object):
    def __init__(self):
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

        self.heater_temperature = 0
        self.is_water_full = False
        self.total_cmd = 0
        self.printer_progress = 0

    def __temperature_monitor(self):
        while True:
            temperature = self.heater_pub.recv()["temperature"]
            self.heater_temperature = temperature

    def __water_level_monitor(self):
        while True:
            self.is_water_full = self.refill_pub.recv()["full"]

    def __printer_monitor(self):
        while True:
            data = self.printer_pub.recv()
            self.total_cmd = data["total"]
            self.printer_progress = data["progress"]

    def cook(self, cookbook_name):
        cmgr = CookbookManager()
        cookbook = Cookbook(cookbook_name, cmgr.read(cookbook_name))

        for step in cookbook.steps():
            for process in step.processes:
                for block in process.blocks:
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

        return gcode

    def handle(self, points):
        cmd_count = 0

        for point in points:

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

            self.printer_cmd.send({"START": True})
            self.wait_printer(cmd_count)

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
            time.sleep(2)

    def wait_refill(self):
        self.refill_cmd.send({"Refill": True})

        # Wait refill finished
        while not self.is_water_full:
            time.sleep(2)

    def wait_printer(self, cmd_count):
        while not (self.printer_progress == cmd_count and self.total_cmd == cmd_count):
            time.sleep(1)

