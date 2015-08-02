import threading
import time
import Queue

import logging
import serial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MachineComPrintCallback(object):

    """Base class for callbacks from the MachineCom class.

    This class has all empty implementations and is attached to the
    MachineCom if no other callback object is attached.

    """

    def mcLog(self, message):
        pass

    def mcStateChange(self, state, state_string):
        pass

    def mcMessage(self, message):
        pass

    def mcProgress(self, lineNr):
        pass


class VirtualPrinter(object):

    def __init__(self):
        pass

    def readline(self):
        return 'ok'

    def write(self, msg):
        print msg


class State:
    INITIAL = 0
    CONNECTING = 1
    OPERATIONAL = 2
    PRINTING = 3
    PAUSED = 4
    CLOSED = 5
    ERROR = 6
    CLOSED_WITH_ERROR = 7

    @staticmethod
    def get_state_string(state):
        if state is State.INITIAL:
            return 'Offline'
        elif state is State.CONNECTING:
            return 'Connecting'
        elif state is State.OPERATIONAL:
            return 'Operational'
        elif state is State.PRINTING:
            return 'Printing'
        elif state is State.PAUSED:
            return 'Paused'
        elif state is State.CLOSED:
            return 'Closed'
        elif state is State.ERROR:
            return 'Error'
        elif state is State.CLOSED_WITH_ERROR:
            return 'Closed with error'


class Smoothie(object):

    def __init__(self, port=None, baudrate=None):
        self._port = port
        self._baudrate = baudrate
        self._serial = None

    def __del__(self):
        self._serial.close()

    def open(self):
        try:
            if self._port == 'VIRTUAL':
                self._serial = VirtualPrinter()
            else:
                logger.info('Open serial \'{}\' with baudrate \'{}\''.format(self._port, self._baudrate))
                self._serial = serial.Serial(
                    str(self._port), self._baudrate, timeout=5, writeTimeout=10000)
            return True
        except serial.SerialException:
            logger.error('Unexpected error while connecting to serial')
            return False

    def readline(self):
        if self._serial is None:
            return None
        try:
            ret = self._serial.readline()
        except:
            logger.error('Unexpected error while reading serial')
            return None
        if ret == '':
            return ''
        logger.info('Recv: %s' % (
            unicode(ret, 'ascii', 'replace').encode('ascii', 'replace').rstrip()))
        return ret

    def write(self, cmd):
        if self._serial is None:
            return
        logger.info('Write \'{}\''.format(cmd))
        try:
            self._serial.write(cmd + '\n')
        except serial.SerialTimeoutException:
            logger.warning(
                'Serial timeout while writing to serial port, trying again.')
            try:
                time.sleep(0.5)
                self._serial_write(cmd + '\n')
            except:
                logger.error('Unexpected error while writing serial')
                return False
        except:
            logger.error('Unexpected error while writing serial')
            return False

        return True
