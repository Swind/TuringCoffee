import time
from threading import Thread
import RPi.GPIO as GPIO

from utils import json_config
from utils import channel

import logging
logger = logging.getLogger(__name__)


class RefillServer(object):

    stop = False

    def __init__(self):
        # Read Config
        self.config = json_config.parse_json("config.json")
        refill_config = self.config["Refill"]

        # Setup Raspberry Pi GPIO
        GPIO.setmode(GPIO.BOARD)

        self.water_level_pin = refill_config["water_level_pin"]
        GPIO.setup(self.water_level_pin[0], GPIO.OUT)
        GPIO.setup(self.water_level_pin[1], GPIO.IN)
        logger.info("Set water level GPIO {} to OUT and {} to IN".format(self.water_level_pin[0], self.water_level_pin[1]))

        self.motor_pin = refill_config["motor_pin"]
        GPIO.setup(self.motor_pin[0], GPIO.OUT)
        GPIO.setup(self.motor_pin[1], GPIO.OUT)
        logger.info("Set motor GPIO {} and {} to OUT".format(self.motor_pin[0], self.motor_pin[1]))

        self.valve_pin = refill_config["valve_pin"]
        GPIO.setup(self.valve_pin, GPIO.OUT)
        logger.info("Set valve GPIO {} to OUT".format(self.valve_pin))

        self.motor_direct = refill_config["motor_direct"]

        # Create a socket to receive refill command
        address = self.config["RefillServer"]["Command_Socket_Address"]
        self.cmd_channel = channel.Channel(address, "Pair", True)
        logger.info("Create a PAIR socket at {}".format(address))

    def start(self):
        """
        Receive command:
        e.g
        {
            "Refill": "START"
        }
        """

        try:
            # The main thread will handle the command socket
            while(True):
                cmd = self.cmd_channel.recv()

                logger.info("Receive command {}".format(cmd))

                if "Refill" in cmd:
                    if cmd["Refill"] == "START":
                        self.__refill_water()
                        self.cmd_channel.send({"Refill": "OK"})
                    elif cmd["Refill"] == "STOP":
                        self.stop = True
                        self.cmd_channel.send({"Refill": "OK"})
        finally:
            GPIO.cleanup()

    def __is_water_fill(self):
        return GPIO.input(self.water_level_pin[1])

    def __refill_water(self):
        GPIO.output(self.valve_pin, True)
        GPIO.output(self.water_level_pin[0], True)
        GPIO.output(self.motor_pin[1], self.motor_direct)

        try:
            while (not self.__is_water_fill() and not self.stop):

                # Every 200 steps check water level and stop flag
                for index in range(0, 200):
                    GPIO.output(self.motor_pin[0], True)
                    time.sleep(0.001)
                    GPIO.output(self.motor_pin[0], False)
                    time.sleep(0.001)
        finally:
            GPIO.output(self.valve_pin, False)
            GPIO.output(self.water_level_pin[0], False)
            GPIO.output(self.motor_pin[1], False)
            self.stop = False

if __name__ == '__main__':
    server = RefillServer()
    server.start()
