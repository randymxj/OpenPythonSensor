#!/usr/bin/python

import time, math
from ops_i2cbase import I2CBase

# ===========================================================================
# BMP180 Class
#
# Thanks for github.com/sparkfun/BMP180_Breakout/
# And github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/blob/master/Adafruit_BMP085/
# ===========================================================================

class BMP180:
	i2c = None
  
	# BMP180 Address
	address = 0x77
	
	# Commands
	BMP180_REG_CONTROL = 0xF4
	BMP180_REG_RESULT = 0xF6

	BMP180_COMMAND_TEMPERATURE = 0x2E
	BMP180_COMMAND_PRESSURE0 = 0x34
	BMP180_COMMAND_PRESSURE1 = 0x74
	BMP180_COMMAND_PRESSURE2 = 0xB4
	BMP180_COMMAND_PRESSURE3 = 0xF4

	# Constructor
	def __init__(self):
		
		# I2C
		self.i2c = I2CBase(self.address)
		
		# Calibration
		self.AC1 = self.readS16(0xAA)
		self.AC2 = self.readS16(0xAC)
		self.AC3 = self.readS16(0xAE)
		self.AC4 = self.readU16(0xB0)
		self.AC5 = self.readU16(0xB2)
		self.AC6 = self.readU16(0xB4)
		self.VB1 = self.readS16(0xB6)
		self.VB2 = self.readS16(0xB8)
		self.MB  = self.readS16(0xBA)
		self.MC  = self.readS16(0xBC)
		self.MD  = self.readS16(0xBE)
		
		self.c3 = 160.0 * pow(2,-15) * self.AC3
		self.c4 = pow(10,-3) * pow(2,-15) * self.AC4
		self.b1 = pow(160,2) * pow(2,-30) * self.VB1
		self.c5 = (pow(2,-15) / 160) * self.AC5
		self.c6 = self.AC6
		self.mc = (pow(2,11) / pow(160,2)) * self.MC
		self.md = self.MD / 160.0
		self.x0 = self.AC1
		self.x1 = 160.0 * pow(2,-13) * self.AC2
		self.x2 = pow(160,2) * pow(2,-25) * self.VB2
		self.y0 = self.c4 * pow(2,15)
		self.y1 = self.c4 * self.c3
		self.y2 = self.c4 * self.b1
		self.p0 = (3791.0 - 8.0) / 1600.0
		self.p1 = 1.0 - 7357.0 * pow(2,-20)
		self.p2 = 3038.0 * 100.0 * pow(2,-36)
	
	def readS16(self, reg):
		"Read a correct ordered 16 bits signed value"
		
		hi = self.i2c.readS8(reg)
		lo = self.i2c.readU8(reg+1)
		return (hi << 8) + lo
	
	def readU16(self, reg):
		"Read a correct ordered 16 bits unsigned value"		
		
		hi = self.i2c.readU8(reg)
		lo = self.i2c.readU8(reg+1)
		return (hi << 8) + lo
			
	def readTemperatureData(self):
		"Read temperature data from the sensor"	
		
		self.i2c.write8(self.BMP180_REG_CONTROL, self.BMP180_COMMAND_TEMPERATURE)
		time.sleep(0.005)  # Wait 5ms
		
		value = self.i2c.readList(self.BMP180_REG_RESULT, 2)
		try:
			rawTempData = ( value[0] << 8 ) + value[1]
		except:
			print "Invlid Temperature Data Read"
			return -255
		
		# Calculate the actual temperature
		X1 = ((rawTempData - self.AC6) * self.AC5) >> 15
		X2 = (self.MC << 11) / (X1 + self.MD)
		B5 = X1 + X2
		actualTemp = ((B5 + 8) >> 4) / 10.0
		
		#tu = ( value[0] << 8 ) + value[1]
		#a = self.c5 * (tu - self.c6)
		#actualTemp = a + (self.mc / (a + self.md))
				
		return actualTemp
	
	def readPressureData(self, T, mode=3):
		"Read pressure data from the sensor"	
		
		if mode is 0:
			self.i2c.write8(self.BMP180_REG_CONTROL, self.BMP180_COMMAND_PRESSURE0)
			time.sleep(0.005)  # Wait 5ms
		elif mode is 1:
			self.i2c.write8(self.BMP180_REG_CONTROL, self.BMP180_COMMAND_PRESSURE1)
			time.sleep(0.008)  # Wait 8ms
		elif mode is 2:
			self.i2c.write8(self.BMP180_REG_CONTROL, self.BMP180_COMMAND_PRESSURE2)
			time.sleep(0.014)  # Wait 14ms
		elif mode is 3:
			self.i2c.write8(self.BMP180_REG_CONTROL, self.BMP180_COMMAND_PRESSURE3)
			time.sleep(0.026)  # Wait 26ms
			
		value = self.i2c.readList(self.BMP180_REG_RESULT, 3)	
		try:
			pu = ( value[0] << 8 ) + value[1] + ( value[2] >> 8 )
		except:
			print "Invlid Pressure Data Read"
			return -255
				
		# Calculate the actual pressure				
		s = T - 25.0
		x = (self.x2 * pow(s,2)) + (self.x1 * s) + self.x0
		y = (self.y2 * pow(s,2)) + (self.y1 * s) + self.y0
		z = (pu - x) / y
		actualPressure = (self.p2 * pow(z,2)) + (self.p1 * z) + self.p0
				
		return actualPressure
	
	def readAltitude(self, pressure, baseline=1013.2):
		"Calculate the actual altitude with pressure (mb)"
		
		if pressure < 0:
			print "Invlid pressure input"
			return -255
		
		return( 44330.0 * ( 1 - pow( pressure / baseline, 1 / 5.255 ) ) )
	