from math import fabs
try:
    import smbus
    I2C = True
except:
    I2C = False
import time


#    -[w1]<-l1->|        [w2]
#    |          |
#    l2         |
#    |          |
#    -----------|
#               |
#               |
#               |
#     [w3]      |        [w4]
#
# http://cdn.intechopen.com/pdfs-wm/465.pdf


class Rever(object):
    def __init__(self, l1, l2):
        self.i2c_bus = smbus.SMBus(0) if I2C else None
        self.mplex = 0x08
        self.l1 = l1
        self.l2 = l2
        self._w1 = 0
        self._w2 = 0
        self._w3 = 0
        self._w4 = 0
        self.w1 = 0
        self.w2 = 0
        self.w3 = 0
        self.w4 = 0

    def move(self, Vx=0, Vy=0, Vw=0):
        w1 = Vx + Vy - Vw * (self.l1 + self.l2)
        w2 = Vx + Vy - Vw * (self.l1 + self.l2)
        w3 = Vx + Vy - Vw * (self.l1 + self.l2)
        w4 = Vx + Vy - Vw * (self.l1 + self.l2)
        _max = max([fabs(w1), fabs(w2), fabs(w3), fabs(w4)])
        _max = _max if _max > 1 else 1
        self.wheel_speeds = w1/_max, w2/_max, w3/_max, w4/_max

    @property
    def wheel_speeds(self):
        return self.w1, self.w2, self.w3, self.w4

    @wheel_speeds.setter
    def wheel_speeds(self, w1, w2, w3, w4):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4

    @property
    def w1(self):
        return self._w1

    @w1.setter
    def w1(self, w1):
        self._w1 = w1
        self._write(self.i2c_bus, self.mplex, w1)

    @property
    def w2(self):
        return self._w2

    @w2.setter
    def w2(self, w2):
        self._w2 = w2
        self._write(self.i2c_bus, self.mplex, w2)

    @property
    def w3(self):
        return self._w3

    @w3.setter
    def w3(self, w3):
        self._w3 = w3
        self._write(self.i2c_bus, self.mplex, w3)

    @property
    def w4(self):
        return self._w4

    @w4.setter
    def w4(self, w4):
        self._w4 = w4
        self._write(self.i2c_bus, self.mplex, w4)

    def _write(self, bus, destiny, value):
        if I2C:
            i2c_write(bus, destiny, value)
        else:
            pass


def i2c_write(i2c_bus, destiny, value):
    if type(value) is str:
        for part in value:
            i2c_bus.write_byte(destiny, ord(part))
    else:
        i2c_bus.write_byte(destiny, value)
    time.sleep(0.1)
