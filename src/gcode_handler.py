from utils import json_config
import msgpack

from process import Point
from process import Command
from process import Process

from nanomsg import (
    SUB,
    SUB_SUBSCRIBE,
    PAIR,
    DONTWAIT,
    Socket
)

class SocketPair(object):
    def __init__(self, pub_address, cmd_address):
        self.pub = Socket(SUB)
        self.pub.connect(pub_address)
        self.pub.set_string_option(SUB, SUB_SUBSCRIBE, "")

        self.cmd = Socket(PAIR)
        self.cmd.connect(cmd_address)

class PointHandler(object):
    def __init__(self, gcode_list):
        # Read config
        self.config = json_config.parse_json("config.json")

        # Create nanomsg socket to publish status and receive command
        cfg = self.config["PrinterServer"]
        self.printer = SocketPair(cfg["Publish_Socket_Address"], cfg["Command_Socket_Address"])

        cfg = self.config["HeaterServer"]
        self.heater = SocketPair(cfg["Publish_Socket_Address"], cfg["Command_Socket_Address"])

        cfg = self.config["RefillServer"]
        self.refill = SocketPair(cfg["Publish_Socket_Address"], cfg["Command_Socket_Address"])

    def handle(self, points):
        for point in points:

            if type(point) is Point:
                gcode = self.__convert_to_gcode(point)
                self.printer.cmd.send(msgpack.packb({"G": gcode}))

            elif type(point) is Command:

                cmd = point.command
                value = point.value

                if cmd == "Home":
                    self.printer.cmd.send(msgpack.packb({"C": "G28"}))

                elif cmd == "Refill":
                    self.refill.cmd.send(msgpack.packb({"Refill": True}))

                    # Wait refill finished
                    result = self.refill.cmd.recv()

                elif cmd == "Heat":
                    payload = {
                        "cycle_time": 1,
                        "k": 44,
                        "i": 165,
                        "d": 4,
                        "set_point": value
                    }

                    self.heater.cmd.send(msgpack.packb(payload))

                    # Wait temperature to target temperature
                    self.wait_temperature()

    def wait_temperature():

        pass

    def start(self):
        self.printer.cmd.send(msgpack.packb({"START": True}))

