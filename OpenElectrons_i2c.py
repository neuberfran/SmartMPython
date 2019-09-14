
# import smbus
import ctypes


try:
    from machine import I2C
except ImportError:
    raise ImportError("Can't find the micropython machine.I2C class: "
                      "perhaps you don't need this adapter?")


class SMBus(I2C):
    """ Provides an 'SMBus' module which supports some of the py-smbus
        i2c methods, as well as being a subclass of machine.I2C
        Hopefully this will allow you to run code that was targeted at
        py-smbus unmodified on micropython.
	    Use it like you would the machine.I2C class:
            bus = SMBus(1, pins=('G15','G10'), baudrate=100000)
            bus.read_byte_data(addr, register)
            ... etc
	"""

    def read_byte_data(self, addr, register):
        """ Read a single byte from register of device at addr
            Returns a single byte """
        return self.readfrom_mem(addr, register, 1)[0]

    def read_i2c_block_data(self, addr, register, length):
        """ Read a block of length from register of device at addr
            Returns a bytes object filled with whatever was read """
        return self.readfrom_mem(addr, register, length)

    def write_byte_data(self, addr, register, data):
        """ Write a single byte from buffer `data` to register of device at addr
            Returns None """
        # writeto_mem() expects something it can treat as a buffer
        if isinstance(data, int):
            data = bytes([data])
        return self.writeto_mem(addr, register, data)

    def write_i2c_block_data(self, addr, register, data):
        """ Write multiple bytes of data to register of device at addr
            Returns None """
        # writeto_mem() expects something it can treat as a buffer
        if isinstance(data, int):
            data = bytes([data])
        return self.writeto_mem(addr, register, data)

    # The follwing haven't been implemented, but could be.
    def read_byte(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")

    def write_byte(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")

    def read_word_data(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")

    def write_word_data(self, *args, **kwargs):
        """ Not yet implemented """
        raise RuntimeError("Not yet implemented")
        
## OpenElectrons_i2c: this class provides i2c functions
#  for read and write operations.
class OpenElectrons_i2c(object):

    @staticmethod
    def pi_rev():
        try:
            with open('/proc/cpuinfo','r') as cpuinfo:
                for line in cpuinfo: 
                    if line.startswith('Hardware'):
                        #print " rstrip output  " +str(line.rstrip()[-4:])
                        cpu = 10 if line.rstrip()[-4:] in ['2709'] else 0
                       
                    if line.startswith('Revision'):
                        # case '3' is for some rare pi board - Deepak
                        #print " rstrip output  " +str(line.rstrip()[-1])
                        rev =  1 if line.rstrip()[-1] in ['1','2','3'] else 2
                return cpu+rev        
                     
        except:
            return 0

    @staticmethod
    def which_bus():
        return 1 if OpenElectrons_i2c.pi_rev() > 1 else 0

    ## Initialize the class with the i2c address of your device
    #  @param i2c_address address of your device
    def __init__(self, i2c_address):
        self.address = i2c_address
        b = OpenElectrons_i2c.which_bus()
        self.bus = SMBus(b)

    ## Write a byte to your i2c device at a given location
    #  @param self The object pointer.
    #  @param reg the register to write value at.
    #  @param value value to write.
    def writeByte(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def readByte(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        return (result)
     
    # for read_i2c_block_data and write_i2c_block_data to work correctly,
    # ensure that i2c speed is set correctly on your pi:
    # ensure following file with contents as follows:
    #    /etc/modprobe.d/i2c.conf
    # options i2c_bcm2708 baudrate=50000
    # (without the first # and space on line above)
    #
    def readArray(self, reg, length):
        results = self.bus.read_i2c_block_data(self.address, reg, length)
        return results

    def writeArray(self, reg, arr):
        self.bus.write_i2c_block_data(self.address, reg, arr)

    def writeArray_byte_at_a_time(self, reg, arr):
        x=0
        for y in arr:
            self.writeByte(reg+x, y)
            x+=1
        return

    def readString(self, reg, length):
        ss = ''
        for x in range(0, length):
            ss = ''.join([ss, chr(self.readByte(reg+x))])
        return ss

    def readArray_byte_at_a_time(self, reg, length):
        ss = []
        for x in range(0, length):
            w=self.readByte(reg+x)
            ss.append(w)
        return ss

    def readInteger(self, reg):
        b0 = self.readByte(reg)
        b1 = self.readByte(reg+1)
        r = b0 + (b1<<8)
        return r

    def readIntegerSigned(self, reg):
        a = self.readInteger(reg)
        signed_a = ctypes.c_int(a).value
        return signed_a

    def readLong(self, reg):
        b0 = self.readByte(reg)
        b1 = self.readByte(reg+1)
        b2 = self.readByte(reg+2)
        b3 = self.readByte(reg+3)
        r = b0 + (b1<<8) + (b2<<16) + (b3<<24)
        return r

    def readLongSigned(self, reg):
        a = self.readLong(reg)
        signed_a = ctypes.c_long(a).value
        return signed_a

    ##  Read the firmware version of the i2c device
    def GetFirmwareVersion(self):
        ver = self.readString(0x00, 8)
        return ver

    ##  Read the vendor name of the i2c device
    def GetVendorName(self):
        vendor = self.readString(0x08, 8)
        return vendor

    ##  Read the i2c device id
    def GetDeviceId(self):
        device = self.readString(0x10, 8)
        return device