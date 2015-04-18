import time
from threading import Thread
import RPi.GPIO as GPIO

from utils import json_config

import logging
logger = logging.getLogger(__name__)


class Refill(object):

    stop = False

    def __init__(self):
        # Read Config
        self.config = json_config.parse_json('config.json')
        refill_config = self.config['Refill']

        # Setup Raspberry Pi GPIO
        GPIO.setmode(GPIO.BOARD)

        self.water_level_pin = refill_config['water_level_pin']
        GPIO.setup(self.water_level_pin[0], GPIO.OUT)
        GPIO.output(self.water_level_pin[0], True)

        GPIO.setup(
            self.water_level_pin[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        logger.info('Set water level GPIO {} to OUT and {} to IN'.format(
            self.water_level_pin[0], self.water_level_pin[1]))

        self.motor_pin = refill_config['motor_pin']
        GPIO.setup(self.motor_pin[0], GPIO.OUT)
        GPIO.setup(self.motor_pin[1], GPIO.OUT)
        logger.info('Set motor GPIO {} and {} to OUT'.format(
            self.motor_pin[0], self.motor_pin[1]))

        self.motor_direct = refill_config['motor_direct']

    def is_water_full(self):
        result = self.water_level_pin[1]
        logger.debug('Read water level pin value: {}'.format(result))
        if GPIO.input(result):
            return True
        else:
            return False

    def refill_water(self):
        GPIO.output(self.motor_pin[1], self.motor_direct)

        try:
            while (not self.is_water_full() and not self.stop):

                # Every 200 steps check water level and stop flag
                for index in range(0, 200):
                    GPIO.output(self.motor_pin[0], True)
                    time.sleep(0.001)
                    GPIO.output(self.motor_pin[0], False)
                    time.sleep(0.001)
        finally:
            GPIO.output(self.water_level_pin[0], False)
            GPIO.output(self.motor_pin[1], False)
            self.stop = False

    def cleanup(self):
        GPIO.cleanup()
