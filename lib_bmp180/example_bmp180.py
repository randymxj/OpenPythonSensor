#!/usr/bin/python

import time
from lib_bmp180 import BMP180

# ===========================================================================
# Example Code of BMP180
# ===========================================================================

# Initialize the BMP180
bmp = BMP180()

for _ in range(100):
	temp = bmp.readTemperatureData()
	pre = bmp.readPressureData(temp, 3)
	alt = bmp.readAltitude(pre, 29.92 * 33.8637526)
	
	print "Temperature: %.2f C, Pressure: %.2f Hpa, Altitude: %.2f M" % (temp, pre, alt)
	
	time.sleep(1)
	
