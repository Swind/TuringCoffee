"""Serial communication with the printer for printing is done from a separate
process, this to ensure that the PIL does not block the serial printing.

This file is the 2nd process that is started to handle communication
with the printer. And handles all communication with the initial
process.

"""

__copyright__ = 'Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License'

from utils import smoothie

from utils import json_config
from utils import channel

import logging
logger = logging.getLogger(__name__)


class PrinterServer(object):

    """The serialComm class is the interface class which handles the
    communication between stdin/stdout and the machineCom class.

    This interface class is used to run the (USB) serial communication
    in a different process then the GUI.

    """

    def __init__(self):
        # Read config
        self.config = json_config.parse_json('config.json')

        # Create nanomsg socket to publish status and receive command
        pub_address = self.config['PrinterServer']['Publish_Socket_Address']
        self.pub_channel = channel.Channel(pub_address, 'Pub', True)
        logger.info('Create the publish channel at {}'.format(pub_address))

        # Receive the printer command
        cmd_address = self.config['PrinterServer']['Command_Socket_Address']
        self.cmd_channel = channel.Channel(cmd_address, 'Pair', True)
        logger.info('Create the command channel at {}'.format(cmd_address))

        self._comm = None
        self._gcodeList = []
        self._printing_gcodeList = []

        if self.config['Emulator']:
            port_name = 'VIRTUAL'
        else:
            port_name = self.config['Printer']['PortName']

        baudrate = int(self.config['Printer']['Baudrate'])

        self._comm = smoothie.Smoothie(
            port_name, baudrate, callback_object=self)

    # ================================================================================
    #
    #   MachineCom callback Interface
    #
    # ================================================================================
    def mcLog(self, message):
        #self.pub_channel.send({"log": message})
        pass

    def mcTempUpdate(self, temp, bedTemp, targetTemp, bedTargetTemp):
        # Because now the temperature is not controled by arduino
        #self.pub_channel.send({"temperature": temp})
        pass

    def mcStateChange(self, state, state_string):
        if self._comm is None:
            return

        self.pub_channel.send(
            {'state': state, 'state_string': state_string})

    def mcMessage(self, message):
        #self.pub_channel.send({"message": message})
        pass

    def mcProgress(self, lineNr):
        self.pub_channel.send({'progress': lineNr})

    def mcZChange(self, newZ):
        #self.pub_channel.send({"changeZ": newZ})
        pass

    # ================================================================================
    #
    #   Printer Server API
    #
    # ================================================================================
    def start(self):
        while True:
            cmd = self.cmd_channel.recv()

            if 'STOP' in cmd:
                self._comm.stop()

            elif 'G' in cmd:
                self._comm.send_command(cmd['G'])

            elif 'C' in cmd:
                self._comm.send_command(cmd['C'])

            elif 'INFORMATION' in cmd:
                self.cmd_channel.send(
                    {'state': self._comm.getState(), 'state_string': self._comm.getStateString()})

            elif 'SHUTDOWN' in cmd:
                self.mcMessage('Shoutdown printer server')
                break

            elif 'PAUSE' in cmd:
                self._comm.pause()

            elif 'RESET_COUNT' in cmd:
                self._comm.reset_count()


if __name__ == '__main__':
    server = PrinterServer()
    server.start()
