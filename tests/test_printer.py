import os
import sys
sys.path.insert(0, '../src')

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
        self.config = json_config.parse_json('config.json')
        self.pub_socket = Socket(SUB)
        self.pub_socket.connect(
            self.config['PrinterServer']['Publish_Socket_Address'])
        self.pub_socket.set_string_option(SUB, SUB_SUBSCRIBE, '')

        self.cmd_socket = Socket(PAIR)
        self.cmd_socket.connect(
            self.config['PrinterServer']['Command_Socket_Address'])

        # Start printer server
        server = printer_server.PrinterServer()
        self.p = Thread(target=server.start)
        self.p.daemon = True
        self.p.start()
        time.sleep(1)

    def __wait_operational(self):
        while True:
            self.cmd_socket.send(msgpack.packb({'INFORMATION': True}))
            result = msgpack.unpackb(self.cmd_socket.recv())

            print result
            if result['state'] == 5:
                break

            time.sleep(1)

    def test_printer_server(self):
        for index in range(0, 128):
            # Send a z change command and try to receive a monitor message
            print 'Send command {}'.format(index)
            self.cmd_socket.send(msgpack.packb({'G': 'G1 Z80'}))

        self.__wait_operational()

        self.cmd_socket.send(msgpack.packb({'START': True}))

        time.sleep(5)

        while True:
            #result = self.pub_socket.recv(flags=DONTWAIT)
            result = self.pub_socket.recv()
            cmd = msgpack.unpackb(result)
            print cmd

        print 'Test Done'

    def tearDown(self):
        print 'Send SHUTDOWN'
        self.cmd_socket.send(msgpack.packb({'SHUTDOWN': True}))
        self.p.join()

        self.pub_socket.close()
        self.cmd_socket.close()
        pass

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestPrinter('test_printer_server'))
    unittest.TextTestRunner().run(suite)
