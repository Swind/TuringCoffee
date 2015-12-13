"""Serial communication with the printer for printing is done from a separate
process, this to ensure that the PIL does not block the serial printing.

This file is the 2nd process that is started to handle communication
with the printer. And handles all communication with the initial
process.

"""

__copyright__ = 'Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License'

import threading
import Queue
import time

from utils import smoothie

from utils import json_config
from utils import channel

import logging
logger = logging.getLogger(__name__)


class GCODE_G1:

    @staticmethod
    def parse_axis(axis, string, end_with):
        len_of_axis = len(axis)
        start_axis = string.find(axis) + len_of_axis
        end_axis = string.find(end_with, start_axis)
        if end_axis == -1:
            end_axis = len(string)
        return float(string[start_axis:end_axis])

    @staticmethod
    def parse(string):
        if 'G1' not in string:
            return None

        x = y = z = e1 = e2 = f = None

        if 'X' in string:
            x = GCODE_G1.parse_axis('X', string, ' ')
        if 'Y' in string:
            y = GCODE_G1.parse_axis('Y', string, ' ')
        if 'Z' in string:
            z = GCODE_G1.parse_axis('Z', string, ' ')
        if 'E1' in string:
            e1 = GCODE_G1.parse_axis('E1', string, ' ')
        if 'E2' in string:
            e2 = GCODE_G1.parse_axis('E2', string, ' ')
        if 'F' in string:
            f = GCODE_G1.parse_axis('F', string, '\n')

        return GCODE_G1(x, y, z, e1, e2, f)

    def __init__(self, x = None, y = None, z = None, e1 = None, e2 = None, f = None):
        self.x = x
        self.y = y
        self.z = z
        self.e1 = e1
        self.e2 = e2
        self.f = f

    def __str__(self):
        gcode = 'G1'
        if self.x is not None:
            gcode = gcode + ' X{}'.format(self.x)

        if self.y is not None:
            gcode = gcode + ' Y{}'.format(self.y)

        if self.z is not None:
            gcode = gcode + ' Z{}'.format(self.z)

        if self.e1 is not None:
            gcode = gcode + ' E{}'.format(self.e1)

        if self.e2 is not None:
            gcode = gcode + ' E{}'.format(self.e2)

        if self.f is not None:
            gcode = gcode + ' F{}'.format(self.f)

        return gcode

class State:
    INITIAL = 0
    CONNECTING = 1
    OPERATIONAL = 2
    PRINTING = 3
    PAUSED = 4
    CLOSED = 5
    ERROR = 6
    CLOSED_WITH_ERROR = 7
    STOPPING = 8

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
        elif state is State.STOPPING:
            return 'STOPPING'


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

        if self.config['Emulator']:
            port_name = 'VIRTUAL'
        else:
            port_name = self.config['Printer']['PortName']
            port_name2 = self.config['Printer']['PortName2']

        baudrate = int(self.config['Printer']['Baudrate'])

        self._comm = smoothie.Smoothie(port_name, baudrate)
        self._comm2 = smoothie.Smoothie(port_name2, baudrate)

        self._callback = self

        self._state = State.INITIAL
        self._cmd_queue = Queue.Queue()
        self._reset_count()

        self._state_table = {
                State.INITIAL: self._open,
                State.CONNECTING: self._connect,
                State.OPERATIONAL: self._check_cmd_queue,
                State.PRINTING: self._exec_command,
                State.PAUSED: self._pause,
                State.STOPPING: self._stop,
                State.CLOSED: self._close
        }

        self._paused_cmd = None
        self._stop_flag = False
        self._pause_flag = False

        self._state_lock = threading.Lock()
        self._thread = threading.Thread(target=self._start)
        self._thread.daemon = True
        self._thread.start()

    def __del__(self):
        self.close()

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
        if self._comm2 is None:
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

    def stop(self):
        self._stop_flag = True

    def pause(self):
        self._pause_flag = True

    def close(self):
        self.stop()

    def _start(self):
        while True:
            state = self._get_state()
            print 'Current state {}'.format(state)
            if state in self._state_table:
                self._state_table[state]()
            else:
                logger.error('This should not happen')

    def _change_state(self, new_state):
        if self._state is new_state:
            return

        old_state_str = State.get_state_string(self._state)
        new_state_str = State.get_state_string(new_state)

        self._state_lock.acquire()
        self._state = new_state
        self._state_lock.release()

        self._callback.mcStateChange(new_state, new_state_str)

        logger.info('Changing state from {} to {}'.format(old_state_str, new_state_str))

    def _get_state(self):
        self._state_lock.acquire()
        state = self._state
        self._state_lock.release()
        return state

    def _open(self):
        if self._comm.open() == True and self._comm2.open():
            self._change_state(State.CONNECTING)
            return True
        else:
            self._change_state(State.CLOSED_WITH_ERROR)
            return False

    def _close(self):
        self._change_state(State.NONE)

    def _connect(self):
        line = self._comm.readline()

        if line is None:
            return False

        if line == '' or 'wait' in line:

            if self._comm.write('M105') is False:
                return False

            line = self._comm.readline()
            if line is None:
                return False

        if 'ok' not in line:
            return False

        if line is None:
            return False

        if line == '' or 'wait' in line:

            if self._comm2.write('M105') is False:
                return False

            line = self._comm2.readline()
            if line is None:
                return False

        if 'ok' not in line:
            return False

        self._change_state(State.OPERATIONAL)
        return True

    def _exec_command(self):
        current_comm = self._comm
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

            i = 0
            while i < len(cmd):
                gcode = cmd[i]

                g1 = GCODE_G1.parse(gcode)
                #print 'G1 {}'.format(g1)
                if g1 is None:
                    if self._comm.write(gcode) is False:
                        self._flush_command()
                        self._change_state(State.CLOSED_WITH_ERROR)
                        return

                    while 'ok' not in self._comm.readline():
                        continue

                    if self._comm2.write(gcode) is False:
                        self._flush_command()
                        self._change_state(State.CLOSED_WITH_ERROR)
                        return

                    while 'ok' not in self._comm2.readline():
                        continue

                else:
                    if self._pause_flag is True:
                        self._change_state(State.PAUSED)
                        self._paused_cmd = cmd[i:]
                        return

                    if self._stop_flag is True:
                        self._change_state(State.STOPPING)
                        return

                    g1_hot = g1
                    g1_cold = None
                    if (g1.e1 is not None) and (g1.e2 is not None):
                        g1_cold = GCODE_G1(e1 = g1.e2, f = (g1.f * (g1.e2/g1.e1)))
                        g1_hot.e2 = None
                    elif (g1.e1 is None) and (g1.e2 is not None):
                        g1_cold = GCODE_G1(e1 = g1.e2, f = g1.f)
                        g1_hot.e2 = None

                    if g1_hot is not None:
                        self._comm.write(str(g1_hot))
                    if g1_cold is not None:
                        self._comm2.write(str(g1_cold))

                    if g1_hot is not None:
                        while 'ok' not in self._comm.readline():
                            continue

                    if g1_cold is not None:
                        while 'ok' not in self._comm2.readline():
                            continue

                self._cmd_counter = self._cmd_counter + 1
                self._callback.mcProgress(self._cmd_counter)
                i = i + 1

    def _pause(self):
        if self._pause_flag is False:
            self._change_state(State.PRINTING)
        if self._stop_flag is True:
            self._change_state(State.STOPPING)
        time.sleep(1)

    def _stop(self):
        self._flush_command()
        self._change_state(State.OPERATIONAL)
        self._stop_flag = False

    def _close(self):
        self._change_state(State.NONE)

    def _check_cmd_queue(self):
        while self._cmd_queue.empty():
            time.sleep(1)
        self._change_state(State.PRINTING)

    def _flush_command(self):
        while not self._cmd_queue.empty():
            self._cmd_queue.get()

    def _send_command(self, cmd):
        type_cmd = type(cmd)
        if type_cmd is str:
            self._cmd_queue.put([cmd])
        elif type_cmd is list:
            self._cmd_queue.put(cmd)
        else:
            return False
        return True

    def _reset_count(self):
        self._cmd_counter = 0

    def start(self):
        while True:
            cmd = self.cmd_channel.recv()

            if 'STOP' in cmd:
                self.stop()

            elif 'G' in cmd:
                self._send_command(cmd['G'])

            elif 'C' in cmd:
                self._send_command(cmd['C'])

            elif 'INFORMATION' in cmd:
                self.cmd_channel.send(
                    {'state': self._comm.getState(), 'state_string': self._comm.getStateString()})

            elif 'SHUTDOWN' in cmd:
                self.mcMessage('Shoutdown printer server')
                break

            elif 'PAUSE' in cmd:
                self._comm.pause()

            elif 'RESET_COUNT' in cmd:
                self._reset_count()

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


if __name__ == '__main__':
    server = PrinterServer()
    server.start()
