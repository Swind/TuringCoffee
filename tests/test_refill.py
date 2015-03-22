import os
import sys
sys.path.insert(0, "../src")

import time

import unittest
from utils import json_config

import msgpack

from nanomsg import (
    SUB,
    PAIR,
    DONTWAIT,
    Socket,
    SUB_SUBSCRIBE
)

from threading import Thread

import printer_server

class TestPrinter(unittest.TestCase):
    def setUp(self):
        # Read config
        self.config = json_config.parse_json("config.json")

        self.cmd_socket = Socket(PAIR)
        self.cmd_socket.connect(self.config["RefillServer"]["Command_Socket_Address"])

    def test_printer_server(self):
        self.cmd_socket.send(msgpack.packb({"Refill": True}))
        print "Test Done"

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestPrinter("test_printer_server"))
    unittest.TextTestRunner().run(suite)
