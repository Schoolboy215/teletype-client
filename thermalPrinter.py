import const
import struct
import serial
import wordWrap

class ThermalPrinter:
	ser = None
	def __init__(self):
		self.ser =	serial.Serial(
        			port = '/dev/ttyS0',
        			baudrate = 19200,
        			parity = serial.PARITY_NONE,
        			stopbits = serial.STOPBITS_ONE,
        			bytesize = serial.EIGHTBITS,
        			timeout = 1
				)
		#self.ser.write(const.RESET_ALL.encode())
		#self.ser.write(const.MAKE_DENSE.encode())
	def write(self,buffer):
		buffer = wordWrap.correctWidth(buffer,30)
		self.ser.write(buffer.encode())
		self.ser.write(const.CARRIAGE_RETURN.encode())
	def thickBar(self):
		self.ser.write(const.HORIZONTAL_BAR.encode())
		self.ser.write(const.CARRIAGE_RETURN.encode())
	def feed(self,linesToFeed):
		#linePart = struct.pack(">c",bytes(linesToFeed)[0])
		linePart = "\x03"
		toSend = "\x1B\x64" + linePart
		self.ser.write(toSend.encode())
	def resetAll(self):
		self.ser.write(const.RESET_ALL.encode())
	def welcome(self):
		self.write(const.WELCOME_MESSAGE)