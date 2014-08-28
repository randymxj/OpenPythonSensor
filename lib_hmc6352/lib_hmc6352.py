#!/usr/bin/python

import time
from ops_i2cbase import I2CBase

# ===========================================================================
# HMC6352 Class
# ===========================================================================

class HMC6352 :
	i2c = None
  
	# HMC6352 Address
	address = 0x42 >> 1
	
	# Commands
	CMD_READ_DATA = 0x41
	CMD_ENTER_USER_CALIBRATION = 0x45
	CMD_EXIT_USER_CALIBRATION = 0x4C

	# Constructor
	def __init__(self):
		self.i2c = I2CBase(self.address)
	
	def userCalibration(self):
		"Write 0x45 for calibration and write 0x4C for leave after 20s"
		self.i2c.write8(0x0, self.CMD_ENTER_USER_CALIBRATION)
		time.sleep(20)
		self.i2c.write8(0x0, self.CMD_EXIT_USER_CALIBRATION)
		
	def readData(self):
		"Read the heading data by write a 0x41 first"
		self.i2c.write8(0x0, self.CMD_READ_DATA)
		# Wait 6 ms
		time.sleep(0.006)
		# Read 2 bytes
		value = self.i2c.readU16(0x0)
		# Reverse the data byte order
		value = self.i2c.reverseByteOrder(value)
		# Convert to 360.0 range from the raw integer value
		value = float('%0.1f'%value)/10

		return value
