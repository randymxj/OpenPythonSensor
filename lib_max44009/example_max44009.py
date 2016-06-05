#!/usr/bin/python

import time
from lib_max44009 import MAX44009

# ========================
# Example Code of MAX44009
# ========================

# change I2C bus number and address eventually!
I2C_BUS = 2
MAX44009_ADDR = 0x4A
#MAX44009_ADDR = 0x4B

max44009 = MAX44009(I2C_BUS, MAX44009_ADDR)
max44009.reset()

for _ in range(100):
        light = max44009.readLight()

        print("light: %.2f lux" % light)

        time.sleep(1)
