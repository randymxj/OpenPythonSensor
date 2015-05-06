#!/usr/bin/python

from ops_i2cbase import I2CBase

# ===========================================================================
# SI1145 Class
#
# Ported from github.com/adafruit/Adafruit_SI1145_Library/
# ===========================================================================

class SI1145:
	i2c = None
  
	# SI1145 Address
	address = 0x60
	
	# Commands
	SI1145_PARAM_QUERY = 0x80
	SI1145_PARAM_SET = 0xA0
	
	SI1145_PSALS_AUTO = 0x0F
	
	# Parameters
	SI1145_PARAM_I2CADDR = 0x00
	SI1145_PARAM_CHLIST = 0x01
	SI1145_PARAM_CHLIST_ENUV = 0x80
	SI1145_PARAM_CHLIST_ENAUX = 0x40
	SI1145_PARAM_CHLIST_ENALSIR = 0x20
	SI1145_PARAM_CHLIST_ENALSVIS = 0x10
	SI1145_PARAM_CHLIST_ENPS1 = 0x01
	SI1145_PARAM_CHLIST_ENPS2 = 0x02
	SI1145_PARAM_CHLIST_ENPS3 = 0x04

	# Registers
	SI1145_REG_PARTID = 0x00
	
	SI1145_REG_UCOEFF0 = 0x13
	SI1145_REG_UCOEFF1 = 0x14
	SI1145_REG_UCOEFF2 = 0x15
	SI1145_REG_UCOEFF3 = 0x16
	SI1145_REG_PARAMWR = 0x17
	SI1145_REG_COMMAND = 0x18
	
	SI1145_REG_MEASRATE0 = 0x08
	SI1145_REG_MEASRATE1 = 0x09

	# Constructor
	def __init__(self):
		
		# I2C
		self.i2c = I2CBase(self.address)
		
		id = self.i2c.readU8(self.SI1145_REG_PARTID)
		if (id != 0x45):
			print "SI1145 is not found"
			
		# to enable UV reading, set the EN_UV bit in CHLIST, and configure UCOEF [0:3] to the default values of 0x7B, 0x6B, 0x01, and 0x00. 
		self.i2c.write8(self.SI1145_REG_UCOEFF0, 0x7B)
		self.i2c.write8(self.SI1145_REG_UCOEFF1, 0x6B)
		self.i2c.write8(self.SI1145_REG_UCOEFF2, 0x01)
		self.i2c.write8(self.SI1145_REG_UCOEFF3, 0x00)
		
		# enable UV sensor
		self.i2c.write8(self.SI1145_REG_PARAMWR, self.SI1145_PARAM_CHLIST_ENUV | self.SI1145_PARAM_CHLIST_ENALSIR | self.SI1145_PARAM_CHLIST_ENALSVIS | self.SI1145_PARAM_CHLIST_ENPS1)
		self.i2c.write8(self.SI1145_REG_COMMAND, self.SI1145_PARAM_CHLIST | self.SI1145_PARAM_SET)
	
		# measurement rate for auto
		self.i2c.write8(self.SI1145_REG_MEASRATE0, 0xFF)
		
		# auto run
		self.i2c.write8(self.SI1145_REG_COMMAND, self.SI1145_PSALS_AUTO)
			
	def readUVIndex(self):
		"Read UV index data from sensor (UV index * 100)"	
		
		rawData = self.i2c.readU16(0x2C)
		
		if rawData > 0x0258:
			return 0x0258
		else:
			return rawData

	def readAmbientLight(self):
		"Read Ambient Light data from sensor (Visible light + IR) in lux"
		
		rawData = self.i2c.readU16(0x22)
				
		return rawData
		
	def readIRLight(self):
		"Read IR data from sensor in lux"
		
		rawData = self.i2c.readU16(0x24)
				
		return rawData	
		