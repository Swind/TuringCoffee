"""
Serial communication with the printer for printing is done from a separate process,
this to ensure that the PIL does not block the serial printing.

This file is the 2nd process that is started to handle communication with the printer.
And handles all communication with the initial process.
"""

__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"
import sys
import time
import os
import json

from utils import machineCom

from utils import json_config
from utils import channel



class PrinterServer(object):

    """
    The serialComm class is the interface class which handles the communication between stdin/stdout and the machineCom class.
    This interface class is used to run the (USB) serial communication in a different process then the GUI.
    """

    def __init__(self):
        # Read config
        self.config = json_config.parse_json("config.json")

        # Create nanomsg socket to publish status and receive command
        self.pub_channel = channel.Channel(self.config["PrinterServer"]["Publish_Socket_Address"], "Pub", True)

        # Receive the printer command
        self.cmd_channel = channel.Channel(self.config["PrinterServer"]["Command_Socket_Address"], "Pair", True)

        self._comm = None
        self._gcodeList = []

        port_name = self.config["Printer"]["PortName"]
        baudrate = int(self.config["Printer"]["Baudrate"])

        self._comm = machineCom.MachineCom(port_name, baudrate, callbackObject=self)

    # ================================================================================
    #
    #   MachineCom callback Interface
    #
    # ================================================================================
    def mcLog(self, message):
        self.pub_channel.send({"log": message})

    def mcTempUpdate(self, temp, bedTemp, targetTemp, bedTargetTemp):
        # Because now the temperature is not controled by arduino
        pass

    def mcStateChange(self, state):
        if self._comm is None:
            return

        self.pub_channel.send({"state": self._comm.getState(), "state_string": self._comm.getStateString()})

    def mcMessage(self, message):
        self.pub_channel.send({"message": message})

    def mcProgress(self, lineNr):
        self.pub_channel.send({"progress": lineNr})

    def mcZChange(self, newZ):
        self.pub_channel.send({"changeZ": newZ})

    def monitorStdin(self):
        while True:
            cmd = self.cmd_channel.recv()

            if 'STOP' in cmd:
                self._comm.cancelPrint()
                self._gcodeList = ['M110']
            elif 'G' in cmd:
                self._gcodeList.append(cmd["G"])
            elif 'C' in cmd:
                self._comm.sendCommand(cmd["C"])
            elif 'START' in cmd:
                self._comm.printGCode(self._gcodeList)
            elif 'INFORMATION' in cmd:
                self.cmd_channel.send({"state": self._comm.getState(), "state_string": self._comm.getStateString()})
            elif 'SHUTDOWN' in cmd:
                self.mcMessage("Shoutdown printer server")
                break


def startMonitor():
    server = PrinterServer()
    server.monitorStdin()

if __name__ == '__main__':
    startMonitor()
