import time
from threading import Thread

from utils import json_config
from utils import channel

import hardware

import logging
logger = logging.getLogger(__name__)


class RefillServer(object):

    stop = False
    full = False

    def __init__(self):
        # Read config
        self.config = json_config.parse_json("config.json")

        self.refill = hardware.get_refill(self.config)

        # Create a socket to receive refill command
        cmd_address = self.config["RefillServer"]["Command_Socket_Address"]
        self.cmd_channel = channel.Channel(cmd_address, "Pair", True)

        pub_address = self.config["RefillServer"]["Publish_Socket_Address"]
        self.pub_channel = channel.Channel(pub_address, "Pub", True)

        self.publish_worker = Thread(target=self.publish_water_level_status)
        self.publish_worker.daemon = True

        self.refill_worker = Thread(target=self.refill_water)
        self.refill_worker.daemon = True

        self.pause = False

    def start(self):
        """
        Receive command:
        e.g
        {
            "Refill": "START"
        }
        """
        self.publish_worker.start()
        self.refill_worker.start()

        try:
            # The main thread will handle the command socket
            while(True):
                cmd = self.cmd_channel.recv()

                logger.info("Receive command {}".format(cmd))

                if "Refill" in cmd:
                    if cmd["Refill"] == "START":
                        self.pause = False
                    elif cmd["Refill"] == "STOP":
                        self.pause = True
        finally:
            self.refill.cleanup()

    def refill_water(self):
        try:
            # The main thread will handle the command socket
            while(True):
                if not self.pause and not self.refill.is_water_full():
                    self.refill.refill_water()

                time.sleep(5)
        finally:
            self.refill.cleanup()


    def publish_water_level_status(self):
        while True:
            self.pub_channel.send({"full": self.refill.is_water_full()})
            time.sleep(1)

if __name__ == '__main__':
    server = RefillServer()
    server.start()
