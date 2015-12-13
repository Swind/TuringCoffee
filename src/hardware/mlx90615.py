from struct import *
import PyBCM2835 as soc

class MLX90615(object):

    def __init__(self):
        soc.init()
        soc.i2c_begin()
        soc.i2c_setBaudrate(100000)
        soc.i2c_setSlaveAddress(0x5a)

    def read(self):
        reg = chr(7)
        buf = "000"
        soc.i2c_begin()
        soc.i2c_write(reg, 1)
        soc.i2c_read_register_rs(reg, buf, 3)
        buf = bytearray(buf)

        r = (int(buf[1]) << 8) + int(buf[0])
        r = float(r)

        r = r * 0.02 - 0.01
        r = r - 273.15
        return r
