import time
import math
import json

import spidev


class MAX31855(object):

    def __init__(self, number, average_number=1):
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
        # The first read after start is 0 0
        self.read()

    def read_internal_c(self, v):
        """Return internal temperature value in degrees celsius."""
        # Ignore bottom 4 bits of thermocouple data.
        v >>= 4
        # Grab bottom 11 bits as internal temperature data.
        internal = v & 0x7FF
        if v & 0x800:
            # Negative value, take 2's compliment. Compute this with subtraction
            # because python is a little odd about handling signed/unsigned.
            internal -= 4096
        # Scale by 0.0625 degrees C per bit and return value.
        return internal * 0.0625

    def read_outer_c(self, v):
        """Return the thermocouple temperature value in degrees celsius."""
        # Check for error reading value.
        if v & 0x7:
            return float('0')
        # Check if signed bit is set.
        if v & 0x80000000:
            # Negative value, take 2's compliment. Compute this with subtraction
            # because python is a little odd about handling signed/unsigned.
            v >>= 18
            v -= 16384
        else:
            # Positive value, just shift the bits to get the value.
            v >>= 18
        # Scale by 0.25 degrees C per bit and return value.
        return v * 0.25

    def read32(self):
        # Read 32 bits from the SPI bus.
        raw = self.spi.readbytes(4)
        if raw is None or len(raw) != 4:
            raise RuntimeError('Did not read expected number of bytes from device!')
        value = raw[0] << 24 | raw[1] << 16 | raw[2] << 8 | raw[3]
        return value

    def read(self):
        v = self.read32()
        return self.read_internal_c(v) + self.read_outer_c(v)
