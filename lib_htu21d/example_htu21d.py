#!/usr/bin/python

import time
from lib_htu21d import HTU21D

# ===========================================================================
# Example Code of HTU21D
# ===========================================================================

# Initialize the HTU21D
htu = HTU21D()

for _ in range(100):
	temp = htu.readTemperatureData()
	rh = htu.readHumidityData()
	
	if temp > -40 and rh > 0:
		print "Temperature: %.2f C, Humidity: %.2f %%" % (temp, rh)
	elif temp == -255:
		print "Temperature data CRC failed"
	elif rh == -255:
		print "RH data CRC failed"
	else:
		print "Invalid:" + str(temp) + ", " + str(rh)
	
	time.sleep(1)
	
