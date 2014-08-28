#!/usr/bin/python

import time, datetime, math
from ops_i2cbase import I2CBase

# ===========================================================================
# MPU6050 Class
#
# Ported from http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html
# ===========================================================================

class MPU6050:
	i2c = None
  
	# MPU6050 Address
	address = 0x68
	
	# Command / Register Address
	MPU6050_PWR_MGMT_1              = 0x6B #R/W
	MPU6050_PWR_MGMT_2              = 0x6C #R/W
	
	MPU6050_RA_ACCEL_XOUT_H         = 0x3B #R
	MPU6050_RA_ACCEL_XOUT_L     	= 0x3C #R
	MPU6050_RA_ACCEL_YOUT_H     	= 0x3D #R
	MPU6050_RA_ACCEL_YOUT_L     	= 0x3E #R
	MPU6050_RA_ACCEL_ZOUT_H     	= 0x3F #R
	MPU6050_RA_ACCEL_ZOUT_L     	= 0x40 #R
	MPU6050_RA_TEMP_OUT_H       	= 0x41 #R
	MPU6050_RA_TEMP_OUT_L       	= 0x42 #R
	MPU6050_RA_GYRO_XOUT_H      	= 0x43 #R
	MPU6050_RA_GYRO_XOUT_L      	= 0x44 #R
	MPU6050_RA_GYRO_YOUT_H      	= 0x45 #R
	MPU6050_RA_GYRO_YOUT_L      	= 0x46 #R
	MPU6050_RA_GYRO_ZOUT_H      	= 0x47 #R
	MPU6050_RA_GYRO_ZOUT_L      	= 0x48 #R
	
	MPU6050_PWR1_SLEEP_BIT          = 6
	
	# Constant
	pi = 3.1415926
	AcceRatio = 16384.0
	GyroRatio = 131.0
	
	# Variable
	offset_acc_x = 0
	offset_acc_y = 0
	offset_acc_z = 0
	offset_gyr_x = 0
	offset_gyr_y = 0
	offset_gyr_z = 0
	
	last_read_time = datetime.datetime.now()

	# Constructor
	def __init__(self):
		self.i2c = I2CBase(self.address)
		self.initialize()
		
	def initialize(self):
		"Initiate the sensor by set and clear the power sleep bit, and collector an average offset"
		
		# Set the sleep bit
		self.setBit(self.MPU6050_PWR_MGMT_1, self.MPU6050_PWR1_SLEEP_BIT)
		# Clear the sleep bit
		self.clearBit(self.MPU6050_PWR_MGMT_1, self.MPU6050_PWR1_SLEEP_BIT)
		# The above Set/Clear process is necessary to prevent the sensor going halt or freeze
		
		# Take simple and calculate the average offset
		simple_time = 200
		sum_acc_x = 0
		sum_acc_y = 0
		sum_acc_z = 0
		sum_gyro_x = 0
		sum_gyro_y = 0
		sum_gyro_z = 0
		for i in range(simple_time):
			x_accel = self.readSint16(self.MPU6050_RA_ACCEL_XOUT_H) / self.AcceRatio
			y_accel = self.readSint16(self.MPU6050_RA_ACCEL_YOUT_H) / self.AcceRatio
			z_accel = self.readSint16(self.MPU6050_RA_ACCEL_ZOUT_H) / self.AcceRatio
			
			x_gyro = self.readSint16(self.MPU6050_RA_GYRO_XOUT_H) / self.AcceRatio
			y_gyro = self.readSint16(self.MPU6050_RA_GYRO_YOUT_H) / self.AcceRatio
			z_gyro = self.readSint16(self.MPU6050_RA_GYRO_ZOUT_H) / self.AcceRatio
			
			temperature = self.readSint16(self.MPU6050_RA_TEMP_OUT_H)
			temperature = (temperature + 521.0) / 340.0 + 35.0
			
			sum_acc_x += x_accel
			sum_acc_y += y_accel
			sum_acc_z += z_accel
			
			sum_gyro_x += x_gyro
			sum_gyro_y += y_gyro
			sum_gyro_z += z_gyro
		
		self.offset_acc_x = sum_acc_x / simple_time
		self.offset_acc_y = sum_acc_y / simple_time
		self.offset_acc_z = sum_acc_z / simple_time
		
		self.offset_gyr_x = sum_gyro_x / simple_time
		self.offset_gyr_y = sum_gyro_y / simple_time
		self.offset_gyr_z = sum_gyro_z / simple_time

	def setBit(self, register, bit):
		"Set a bit in the register"
		# Read
		original = self.i2c.readU8(register)
		
		# Set
		self.i2c.write8( register, original | ( 0x01 << bit ) )
	
	def clearBit(self, register, bit):
		"Clear a bit in the register"
		# Read
		original = self.i2c.readU8(register)

		# Clear
		self.i2c.write8( register, original ^ ( 0x01 << bit ) )
		
	def readSint16(self, address):
		"Read a signed 16 bits register"
		high = self.i2c.readU8(address)
		low = self.i2c.readU8(address + 1)
		value = (high << 8) + low
		
		if (value >= 0x8000):
			return -((65535 - value) + 1)
		else:
			return value
	
	def readMPU6050(self):
		"Read and return the Gyro and the Accelerometer value"
		
		current_time = datetime.datetime.now()
		dt_timedelta = ( current_time - self.last_read_time )
		dt_milliseconds = ( dt_timedelta.seconds * 1000 * 1000 + dt_timedelta.microseconds ) / 1000
		self.last_read_time = current_time
		
		x_accel = self.readSint16(self.MPU6050_RA_ACCEL_XOUT_H) / self.AcceRatio
		y_accel = self.readSint16(self.MPU6050_RA_ACCEL_YOUT_H) / self.AcceRatio
		z_accel = self.readSint16(self.MPU6050_RA_ACCEL_ZOUT_H) / self.AcceRatio
		
		x_gyro = self.readSint16(self.MPU6050_RA_GYRO_XOUT_H) / self.AcceRatio
		y_gyro = self.readSint16(self.MPU6050_RA_GYRO_YOUT_H) / self.AcceRatio
		z_gyro = self.readSint16(self.MPU6050_RA_GYRO_ZOUT_H) / self.AcceRatio
		
		temperature = self.readSint16(self.MPU6050_RA_TEMP_OUT_H)
		temperature = (temperature + 521.0) / 340.0 + 35.0
		
		x_rotation = -math.degrees( math.atan2(x_accel, math.sqrt((y_accel*y_accel)+(z_accel*z_accel))) )
		y_rotation =  math.degrees( math.atan2(y_accel, math.sqrt((x_accel*x_accel)+(z_accel*z_accel))) )
		
		return x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, temperature, x_rotation, y_rotation
		