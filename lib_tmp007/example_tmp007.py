#!/usr/bin/python

import time
from lib_tmp007 import TMP007

# ===========================================================================
# Example Code of TMP007
# ===========================================================================

# Initialize the TMP007
tmp = TMP007()

for _ in range(100):
	objTemp = tmp.readObjTemp()
	dieTemp = tmp.readDieTemp()
	irVoltage = tmp.readSensorVoltage()
	
	print "Object Temp: %.2f C, Die Temp: %.2f C, Voltage: %.2f mV" % (objTemp, dieTemp, irVoltage)
	
	time.sleep(1)
	
