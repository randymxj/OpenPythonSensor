#!/usr/bin/python

import time
from lib_mpu6050 import MPU6050

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the MPU6050
mpu = MPU6050()

# read
for _ in range(1000):

	x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, temperature, x_rotation, y_rotation = mpu.readMPU6050()
	
	print "Accel X: %.2f, Y: %.2f, Z: %.2f, Gyro X: %.2f, Y: %.2f, Z: %.2f, Temperature: %.2f, x_rotation: %.2f, y_rotation: %.2f" % (x_accel, y_accel, z_accel, x_gyro, y_gyro, z_gyro, temperature, x_rotation, y_rotation)
	
	time.sleep(0.1)
