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

    def mcStateChange(self, state):
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

    def __init__(self, port=None, baudrate=None, callback_object=None):
        if callback_object is None:
            callback_object = MachineComPrintCallback()

        self._port = port
        self._baudrate = baudrate

        self._state_table = {
                State.INITIAL: self._open,
                State.CONNECTING: self._connect,
                State.OPERATIONAL: self._check_cmd_queue,
                State.PRINTING: self._exec_command,
                State.PAUSED: self._pause,
                State.CLOSED: self._close
        }

        self._serial = None
        self._callback = callback_object
        self._state = State.INITIAL
        self._cmd_queue = Queue.Queue()
        self._paused_cmd = None
        self._state_lock = threading.Lock()
        self._pause_flag = False
        self._stop_flag = False

        self._thread = threading.Thread(target=self._start)
        self._thread.daemon = True
        self._thread.start()

    def __del__(self):
        self.close()

    def _start(self):
        while True:
            state = self._get_state()
            if state in self._state_table:
                self._state_table[state]()
            else:
                logger.error('This should not happen')

    def _open(self):
        try:
            if self._port == 'VIRTUAL':
                self._serial = VirtualPrinter()
            else:
                logger.info('Open serial \'{}\' with baudrate \'{}\''.format(self._port, self._baudrate))
                self._serial = serial.Serial(
                    str(self._port), self._baudrate, timeout=5, writeTimeout=10000)
            self._change_state(State.CONNECTING)
            return True
        except serial.SerialException:
            logger.error('Unexpected error while connecting to serial')
            self._change_state(State.CLOSED_WITH_ERROR)
            return False

    def _connect(self):
        line = self._readline()

        if line is None:
            return False

        if line == '' or 'wait' in line:

            if self._write('M105') is False:
                return False

            line = self._readline()
            if line is None:
                return False

        if 'ok' not in line:
            return False

        self._change_state(State.OPERATIONAL)
        return True

    def _check_cmd_queue(self):
        while self._cmd_queue.empty():
            time.sleep(1)
        self._change_state(State.PRINTING)

    def _flush_command(self):
        self._cmd_queue.clear()

    def _exec_command(self):
        while True:
            cmd = None
            if self._paused_cmd is not None:
                cmd = self._paused_cmd
                self._paused_cmd = None
            else:
                try:
                    cmd = self._cmd_queue.get(False)
                except Queue.Empty:
                    self._change_state(State.OPERATIONAL)
                    break;

            for i in xrange(0, len(cmd)):
                gcode = cmd[i]
                if self._pause_flag is True:
                    self._change_state(State.PAUSED)
                    self._paused_cmd = cmd[i:]
                    return

                if self._stop_flag is True:
                    self._flush_command()
                    self._change_state(State.OPERATIONAL)
                    return

                if self._write(gcode) is False:
                    self._flush_command()
                    self._change_state(State.CLOSED_WITH_ERROR)
                    return

    def _pause(self):
        if self._pause_flag is False:
            self._change_state(State.PRINTING)
        if self._stop_flag is True:
            self._flush_command()
            self._change_state(State.OPERATIONAL)
        time.sleep(1)

    def _close(self):
        self._change_state(State.NONE)

    def _readline(self):
        if self._serial is None:
            return None
        try:
            ret = self._serial.readline()
        except:
            logger.error('Unexpected error while reading serial')
            self._change_state(State.CLOSED_WITH_ERROR)
            return None
        if ret == '':
            return ''
        logger.info('Recv: %s' % (
            unicode(ret, 'ascii', 'replace').encode('ascii', 'replace').rstrip()))
        return ret

    def _write(self, cmd):
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

    def _change_state(self, new_state):
        if self._state is new_state:
            return

        old_state_str = State.get_state_string(self._state)
        new_state_str = State.get_state_string(new_state)

        self._state_lock.acquire()
        self._state = new_state
        self._state_lock.release()

        logger.info('Changing state from {} to {}'.format(old_state_str, new_state_str))

    def _get_state(self):
        self._state_lock.acquire()
        state = self._state
        self._state_lock.release()
        return state

    def send_command(self, cmd):
        type_cmd = type(cmd)
        if type_cmd is str:
            self._cmd_queue.put([cmd])
        elif type_cmd is list:
            self._cmd_queue.put(cmd)
        else:
            return False
        return True

    def stop(self):
        self._stop_flag = True

    def pause(self):
        self._pause_flag = True

    def close(self):
        self.stop()
        self._wait_stop()

    def is_closed(self):
        state = self._get_state()
        if state is State.CLOSED:
            return True
        return False

    def is_operational(self):
        state = self._get_state()
        if state is State.OPERATIONAL:
            return True
        return False

    def is_printing(self):
        state = self._get_state()
        if state is State.PRINTING:
            return True
        return False

    def is_pausing(self):
        state = self._get_state()
        if state is State.PAUSED:
            return True
        return False
