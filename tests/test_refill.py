import os
import sys
sys.path.insert(0, "../src")

import time

import unittest
from utils import json_config

from utils import channel

class TestPrinter(unittest.TestCase):
    def setUp(self):
        # Read config
        self.config = json_config.parse_json("config.json")
	address = self.config["RefillServer"]["Command_Socket_Address"]
	self.channel = channel.Channel(address, "Pair", False)

    def test_printer_server(self):
        self.channel.send({"Refill": "START"})
	result = self.channel.recv()
        print result 

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestPrinter("test_printer_server"))
    unittest.TextTestRunner().run(suite)
