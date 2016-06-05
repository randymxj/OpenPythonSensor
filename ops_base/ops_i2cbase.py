#!/usr/bin/python

import smbus

# ===========================================================================
# I2C Base Class
# Thanks for Adafruit-Raspberry-Pi-Python-Code - Adafruit_I2C.py
# ===========================================================================

class I2CBase :

        I2C_BUS_DEFAULT = 1
 
        def __init__(self, address, bus = I2C_BUS_DEFAULT):
                self.address = address
                self.bus = smbus.SMBus(bus)

        def reverseByteOrder(self, data):
                "Reverses the byte order of an int (16-bit) or long (32-bit) value"
                if data is None:
                        print "ERROR: Invlid data"
                        return 0
                # Courtesy Vishal Sapre
                byteCount = len(hex(data)[2:].replace('L','')[::2])
                val = 0
                for i in range(byteCount):
                        val    = (val << 8) | (data & 0xff)
                        data >>= 8
                return val

        def writeList(self, reg, list):
                "Writes an array of bytes using I2C format"
                try:
                        self.bus.write_i2c_block_data(self.address, reg, list)
                except IOError, err:
                        print "ERROR: failed to writeList to 0x%02X" % self.address

        def write8(self, reg, value):
                "Writes an 8-bit value to the specified register/address"
                try:
                        self.bus.write_byte_data(self.address, reg, value)
                except IOError, err:
                        print "ERROR: failed to write8 to 0x%02X" % self.address

        def write16(self, reg, value):
                "Writes a 16-bit value to the specified register/address pair"
                try:
                        self.bus.write_word_data(self.address, reg, value)
                except IOError, err:
                        print "ERROR: failed to write16 to 0x%02X" % self.address
                        
        def readList(self, reg, length):
                "Read a list of bytes from the I2C device"
                try:
                        results = self.bus.read_i2c_block_data(self.address, reg, length)
                        return results
                except IOError, err:
                        print "ERROR: failed to readList from 0x%02X" % self.address
                        return 0

        def readU8(self, reg):
                "Read an unsigned byte from the I2C device"
                try:
                        result = self.bus.read_byte_data(self.address, reg)
                        return result
                except IOError, err:
                        print "ERROR: failed to readU8 from 0x%02X" % self.address
                        return 0

        def readS8(self, reg):
                "Reads a signed byte from the I2C device"
                try:
                        result = self.bus.read_byte_data(self.address, reg)
                        if result > 127: 
                                result -= 256
                        return result
                except IOError, err:
                        print "ERROR: failed to readS8 from 0x%02X" % self.address
                        return 0

        def readU16(self, reg):
                "Reads an unsigned 16-bit value from the I2C device"
                try:
                        result = self.bus.read_word_data(self.address,reg)
                        return result
                except IOError, err:
                        print "ERROR: failed to readU16 from 0x%02X" % self.address
                        return 0

        def readS16(self, reg):
                "Reads a signed 16-bit value from the I2C device"
                try:
                        result = self.bus.read_word_data(self.address,reg)
                        return result
                except IOError, err:
                        print "ERROR: failed to readS16 from 0x%02X" % self.address
                        return 0

