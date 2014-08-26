#!/usr/bin/python

import time
from lib_si1145 import SI1145

# ===========================================================================
# Example Code of SI1145
# ===========================================================================

# Initialize the SI1145
si = SI1145()

for _ in range(100):
	uvindex = float(si.readUVIndex())/100
	visibleLevel = si.readAmbientLight()
	IRLevel = si.readIRLight()
	
	print "UV Index: %.2f, Visible Light: %d lux, IR Light: %d lux" % (uvindex, visibleLevel, IRLevel)
	
	time.sleep(1)
	
