import time
from threading import Thread

from utils import json_config

import msgpack
from nanomsg import (
    PUB,
    PAIR,
    DONTWAIT,
    Socket
)

import RPi.GPIO as GPIO

class RefillServer(object):

    stop = False

    def __init__(self):
        # Read Config
        self.config = json_config.parse_json("config.json")

        self.refill_pin = self.config["Refill"]["water_level_pin"]
        self.motor_pin = self.config["Refill"]["motor_pin"]
        #self.valve_pin = self.config["Refill"]["valve_pin"]

	print self.refill_pin

	GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.refill_pin[0], GPIO.OUT)
        GPIO.setup(self.refill_pin[1], GPIO.IN)

	print self.motor_pin

        GPIO.setup(self.motor_pin[0], GPIO.OUT)
        GPIO.setup(self.motor_pin[1], GPIO.OUT)

        #GPIO.setup(self.valve_pin, GPIO.OUT)

        self.water_level_worker = Thread(target=self.__monitor_water_level)
        self.water_level_worker.daemon = True

        # Receive the pid controller command
        self.cmd_socket = Socket(PAIR)
        self.cmd_socket.bind(self.config["RefillServer"]["Command_Socket_Address"])

    def start(self):
        """
        Receive command:
        e.g
        {
            "Refill": "START"
        }
        """

        # The main thread will handle the command socket
	"""
        while(True):
            req = self.cmd_socket.recv()
            cmd = msgpack.unpackb(req)

	    print cmd

            if "Refill" in cmd:
                if cmd["Refill"] == "START":
                    self._refill_water()
                    self.cmd_socket.send({"Refill": "OK"})
                elif cmd["Refill"] == "STOP":
                    self.stop = True
                    self.cmd_socket.send({"Refill": "OK"})
	"""
	self.__refill_water()

    def __monitor_water_level(self):
        while True:
            result = GPIO.input(self.refill_pin[1])

	    print result
            if result:
                self.stop = True
                break
	    time.sleep(1)

    def __refill_water(self):
        self.water_level_worker.start()

        # Open valve
        #GPIO.output(self.valve_pin, True)
	GPIO.output(self.motor_pin[1], False)
        while True:
            if not self.stop:
                GPIO.output(self.motor_pin[0], True)
                time.sleep(0.001)
                GPIO.output(self.motor_pin[0], False)
                time.sleep(0.001)
	    else:
		break

        # Close valve
        #GPIO.output(self.valve_pin, False)
        self.stop = False

if __name__ == '__main__':
    server = RefillServer()
    server.start()
