from pid import pid

import time
from threading import Thread

import hardware
from utils import json_config


class PIDController(object):
    def __init__(self, config):
        # Heat
        self.__heater = hardware.get_heater(config)
        self.__sensors = hardware.get_sensors(config)

        # PID configuration
        pid_config = config["PID"]

        self.cycle_time = pid_config["cycle_time"]
        self.set_point = 0

        # Init PID module
        self.pid = pid(self.cycle_time, pid_config["k"], pid_config["i"], pid_config["d"])

        # Worker thread
        self.worker = Thread(target=self.__control_temperature)
        self.worker.daemon = True

        self.__observers = []

    def start(self):
        self.__heater.start()

        for sensor in self.__sensors:
            sensor.start()

        self.worker.start()

    def set_params(self, cycle_time, k_param, i_param, d_param, set_point):
        self.cycle_time = cycle_time
        self.set_point = set_point

        self.pid.set_params(self.cycle_time, k_param, i_param, d_param)

    def get_temperature(self):
        def get_sensor_records_avg(sensor):
            records = sensor.get_records()

            total = 0
            if records:
                for record in records:
                    total = total + record[0]

                return total / len(records)
            else:
                return 0

        return reduce(lambda total, sensor: total + get_sensor_records_avg(sensor), self.__sensors, 0) / len(self.__sensors)

    def add_observer(self, callback_func):
        self.__observers.append(callback_func)

    def __control_temperature(self):

        while (True):
            # Get the average of all sensors
            temperature = self.get_temperature()

            duty_cycle = self.pid.calcPID_reg4(temperature, self.set_point, True)
            self.__heater.add_job(self.cycle_time, duty_cycle)

            # notify to all observers
            for observer in self.__observers:
                observer(self.cycle_time, duty_cycle, self.set_point, temperature)

            # Wait heat job done
            time.sleep(self.cycle_time)
