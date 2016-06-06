#!/usr/bin/python

from ops_i2cbase import I2CBase

# ============================================================================================
# MAX44009 ambient light sensor
#
# Tested with GY-49 MAX44009 Sensor Module on BeagleBone Black rev. C
#
# Inspired by:
#   UPM (Useful Packages & Modules)
#     https://github.com/intel-iot-devkit/upm/tree/master/src/max44009
#   Quick2Wire (Python API for controlling GPIO and I2C devices connected to the Raspberry Pi)
#     https://gist.github.com/garbinij/11402632
#
# Coded by Tomas Psika
#
# Maxim Integrated (TM) Datasheet
#       http://datasheets.maximintegrated.com/en/ds/MAX44009.pdf
# ============================================================================================

class MAX44009:
        i2c = None

        BUS_DEFAULT = 2

        ADDR_DEFAULT = 0x4A
        ADDR_ALTERNATIVE = 0x4B

        REG_RW_INTERRUPT_ENABLE                 = 0x01
        REG_RW_CONFIGURATION                    = 0x02
        REG_RO_LUX_HIGH_BYTE                    = 0x03
        REG_RO_LUX_LOW_BYTE                     = 0x04
        REG_RW_UPPER_THRESHOLD_HIGH_BYTE        = 0x05
        REG_RW_LOWER_THRESHOLD_HIGH_BYTE        = 0x06
        REG_RW_THRESHOLD_TIMER                  = 0x07

        def __init__(self, bus = BUS_DEFAULT, address = ADDR_DEFAULT):
                self.i2c = I2CBase(address, bus)

        def readLight(self):
                lux_high_byte = self.i2c.readU8(self.REG_RO_LUX_HIGH_BYTE)
                lux_low_byte = self.i2c.readU8(self.REG_RO_LUX_LOW_BYTE)
                exponent = lux_high_byte >> 4
                if exponent == 0x0F:
                        return -1       # overrange
                mantissa = ((lux_high_byte & 0x0F) << 4) | (lux_low_byte & 0x0F)
                return 2 ** exponent * mantissa * 0.045

        def reset(self):
                self.i2c.write8(self.REG_RW_INTERRUPT_ENABLE, 0x00);
                self.i2c.write8(self.REG_RW_INTERRUPT_ENABLE, 0x00)
                self.i2c.write8(self.REG_RW_CONFIGURATION, 0x03)
                self.i2c.write8(self.REG_RW_UPPER_THRESHOLD_HIGH_BYTE, 0xFF)
                self.i2c.write8(self.REG_RW_LOWER_THRESHOLD_HIGH_BYTE, 0x00)
                self.i2c.write8(self.REG_RW_THRESHOLD_TIMER, 0xFF)

