import time
import math
import json

import spidev


class PT100(object):

    def __init__(self, number, average_number=5):
        self.__average_number = average_number

        self.spi = spidev.SpiDev()
        self.spi.open(0, number)
        self.spi.max_speed_hz = 100000
        self.spi.mode = 1
        """
            Configuration bits:
            Vbias           1=on
            Conversion mode 1=auto,0=normally off
            1-shot          1=1-shot (auto-clear)
            3-wire          1=3-wire,0=2/4 wire
            Fault detection
            Fault detection
            Fault Status    1=clear
            Filter          1=50Hz,2=60Hz
        """
        config = 0b11110011

        # Write Config
        self.spi.xfer([0x80, config])
        self.spi.xfer([0x05, 0x00])
        self.spi.xfer([0x06, 0x00])
        self.spi.xfer([0x03, 0xff])
        self.spi.xfer([0x04, 0xff])

        with open('max31865_table.json', 'r') as table:
            self.table = json.loads(table.read())

        # The first read after start is 0 0
        self.read()

    def _interpolation(self, rtdRaw):
        for index, item in enumerate(self.table):
            if rtdRaw <= int(item['code_dec']):
                break

        a1 = self.table[index - 1]
        a1_code_dec = float(a1['code_dec'])
        a1_temperature = float(a1['temperature'])

        a2 = self.table[index]
        a2_code_dec = float(a2['code_dec'])
        a2_temperature = float(a2['temperature'])

        return ((rtdRaw - a1_code_dec) / (a2_code_dec - a1_code_dec) * (a2_temperature - a1_temperature)) + a1_temperature

    def _RawToTemp(self, msb_rtd, lsb_rtd):
        a = 3.90830e-3
        b = -5.77500e-7

        rtdR = 400
        rtd0 = 100

        rtdRaw = ((msb_rtd << 7) + ((lsb_rtd & 0xFE) >> 1))

        return self._interpolation(rtdRaw)

    def read(self):
        # Read RTD multiple times and average these
        temp = 0

        for index in range(0, self.__average_number):
            MSB = self.spi.xfer([0x01, 0x00])[1]
            LSB = self.spi.xfer([0x02, 0x00])[1]

            temp = temp + self._RawToTemp(MSB, LSB)

        return (temp / self.__average_number)
