import time
import math
import json

import spidev


class MAX31856(object):

    def __init__(self, number, average_number=1):
        self.spi = spidev.SpiDev()
        self.spi.open(0, number)
        self.spi.max_speed_hz = 100000
        self.spi.mode = 1
        self.writeRegister(1, 0x07) # t-type
        time.sleep(2)

    def readRegister(self, reg_num, byte):
        self.spi.xfer([reg_num])
        buf = self.spi.readbytes(17)
        print buf
        return buf[reg_num+1:reg_num+1+byte]

    def writeRegister(self, reg_num, data):
        address_byte = 0x80 | reg_num
        self.spi.xfer([address_byte, data])

    def requestTempConv(self):
        self.writeRegister(0, 0x42)
        time.sleep(.2)

    def read(self):

        while True:
            time.sleep(.5)
            self.requestTempConv()
            out = self.readRegister(0x0c, 4)

            print out

            [tc_highByte, tc_middleByte, tc_lowByte] = [out[0], out[1], out[2]]
            temp = ((tc_highByte << 16) | (tc_middleByte << 8) | tc_lowByte) >> 5

            if (tc_highByte & 0x80):
                temp -= 0x80000

            temp_C = temp * 0.0078125

            fault = out[3]

            print "%08x" % fault
            if ((fault & 0x80)):
                print ("Cold Junction Out-of-Range")
                continue
            if ((fault & 0x40)):
                print ("Thermocouple Out-of-Range")
                continue
            if ((fault & 0x20)):
                print ("Cold-Junction High Fault")
                continue
            if ((fault & 0x10)):
                print ("Cold-Junction Low Fault")
                continue
            if ((fault & 0x08)):
                print ("Thermocouple Temperature High Fault")
                continue
            if ((fault & 0x04)):
                print ("Thermocouple Temperature Low Fault")
                continue
            if ((fault & 0x02)):
                print ("Overvoltage or Undervoltage Input Fault")
                continue
            if ((fault & 0x01)):
                print ("Thermocouple Open-Circuit Fault")
                continue

            break

        return temp_C
