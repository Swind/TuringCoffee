from threading import Thread
import atexit
import Queue
import time
import atexit

import RPi.GPIO as GPIO


ON = 1
OFF = 0


def close_heater(pin_number):
    GPIO.output(pin_number, OFF)


class Heater(object):

    def __init__(self, pin_number):
        self.__queue = Queue.Queue()

        self.pin_number = pin_number
        self.worker = Thread(target=self.__manage_heat)
        self.worker.daemon = True

    def start(self):
        GPIO.setmode(GPIO.BOARD)
        if self.pin_number > 0:
            GPIO.setup(self.pin_number, GPIO.OUT)
            atexit.register(close_heater, self.pin_number)

        self.worker.start()

    def add_job(self, cycle_time, duty_cycle):
        self.__queue.put((cycle_time, duty_cycle))

    def __manage_heat(self):
        while (True):
            cycle_time, duty_cycle = self.__queue.get(block=True)

            on_time, off_time = self.__getonofftime(cycle_time, duty_cycle)
            if on_time > 0:
                GPIO.output(self.pin_number, ON)
                time.sleep(on_time)

            if off_time > 0:
                GPIO.output(self.pin_number, OFF)
                time.sleep(off_time)

    # Get time heating element is on and off during a set cycle time
    def __getonofftime(self, cycle_time, duty_cycle):
        duty = duty_cycle / 100.0

        on_time = cycle_time * (duty)
        off_time = cycle_time * (1.0 - duty)

        return on_time, off_time
