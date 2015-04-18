from threading import Thread
import Queue

import time


class TemperatureMonitor(object):
    MAX_RECORD_NUMBER = 64

    def __init__(self, sensor, interval=0.5):
        self.__sensor = sensor
        self.__interval = interval
        self.records = []

        self.worker = Thread(target=self.__mointor_sensor)
        self.worker.daemon = True

    def start(self):
        self.worker.start()

    def __mointor_sensor(self):
        # The montior will get the temperature every 0.5 second
        while (True):
            time.sleep(self.__interval)

            self.records.append((self.__sensor.read(), time.time()))

            if len(self.records) > self.MAX_RECORD_NUMBER:
                # Remove the oldest record
                self.records.pop(0)

    def get_records(self, time_range=3):
        # Time range unit is second
        record_num = time_range * 2
        if record_num > self.MAX_RECORD_NUMBER:
            record_num = self.MAX_RECORD_NUMBER

        return self.records[-record_num:]
