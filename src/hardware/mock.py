from threading import Thread
import Queue
import time

ON = 1
OFF = 0

import logging
logger = logging.Logger(__name__)


class MockHeater(object):

    def __init__(self, heater_conf):
        """
        power unit: w
        capacity:   ml
        """
        self.__queue = Queue.Queue()
        self.power = float(heater_conf['power'])
        self.capacity = float(heater_conf['capacity'])
        self.start_temperature = float(heater_conf['start_temperature'])
        self.heat_dissipation = float(
            self.capacity) / heater_conf['heat_dissipation_per_c']

        self.worker = Thread(target=self.__manage_heat)
        self.worker.daemon = True

        self.emulator_worker = Thread(target=self.__emulator)
        self.emulator_worker.daemon = True
        self.emulator_interval = 0.1

        self.pin_status = OFF
        self.__total_cal = 0

        # every 10 min the temperature -1
        self.heat_dissipation = self.capacity / (10 * 60)

    def start(self):
        self.worker.start()
        self.emulator_worker.start()

    def add_job(self, cycle_time, duty_cycle):
        self.__queue.put((cycle_time, duty_cycle))

    def get_temperature(self):
        return self.start_temperature + (self.__total_cal / self.capacity)

    def __manage_heat(self):
        while (True):
            cycle_time, duty_cycle = self.__queue.get(block=True)

            on_time, off_time = self.__getonofftime(cycle_time, duty_cycle)
            if on_time > 0:
                self.pin_status = ON
                time.sleep(on_time)

            if off_time > 0:
                self.pin_status = OFF
                time.sleep(off_time)

            self.pin_status = OFF

    # Get time heating element is on and off during a set cycle time
    def __getonofftime(self, cycle_time, duty_cycle):
        duty = duty_cycle / 100.0

        on_time = cycle_time * (duty)
        off_time = cycle_time * (1.0 - duty)

        return on_time, off_time

    def __emulator(self):

        while(True):
            # every 0.1 second will check the pin status and change the total
            # cal
            if self.pin_status:
                add_temperature = (self.power / 4.184) * self.emulator_interval
                self.__total_cal = self.__total_cal + add_temperature
            else:
                desc_temperature = self.heat_dissipation * \
                    self.emulator_interval
                self.__total_cal = self.__total_cal - desc_temperature

            time.sleep(self.emulator_interval)


class MockSensor(object):

    def __init__(self, heater):
        self.__heater = heater

    def read(self):
        return self.__heater.get_temperature()


class MockRefill(object):

    full_flag = False

    def is_water_full(self):
        return self.full_flag

    def refill_water(self):
        self.full_flag = False
        time.sleep(5)
        self.full_flag = True
