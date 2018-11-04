import const
import struct
import serial
import wordWrap
from Adafruit_Thermal import *

enableSerial = True

class ThermalPrinter:
	ser = None
	def __init__(self):
		if enableSerial:
			self.printer = Adafruit_Thermal("/dev/ttyS0")
			#self.ser =	serial.Serial(
			#			port = '/dev/ttyS0',
			#			baudrate = 19200,
			#			parity = serial.PARITY_NONE,
			#			stopbits = serial.STOPBITS_ONE,
			#			bytesize = serial.EIGHTBITS,
			#			timeout = 1
			#		)

	def write(self,buffer):
		if enableSerial:
			buffer = wordWrap.correctWidth(buffer,30)
			self.printer.write(buffer)
			self.printer.feed()
			#self.ser.write(buffer.encode())
			#self.ser.write(const.CARRIAGE_RETURN.encode())
		else:
			print(buffer)
	def printImage(self, image):
		if enableSerial:
			self.printer.printImage(image)
			self.printer.feed()
	def thickBar(self):
		if enableSerial:
			self.printer.write(const.HORIZONTAL_BAR.encode())
			self.printer.feed()
			#self.ser.write(const.HORIZONTAL_BAR.encode())
			#self.ser.write(const.CARRIAGE_RETURN.encode())
	def feed(self,linesToFeed):
		if enableSerial:
			#linePart = "\x03"
			#toSend = "\x1B\x64" + linePart
			#self.ser.write(toSend.encode())
			self.printer.feed(linesToFeed)
	def resetAll(self):
		if enableSerial:
			pass
			#self.ser.write(const.RESET_ALL.encode())
	def welcome(self):
		if enableSerial:
			self.printer.write(const.WELCOME_MESSAGE)
			#self.write(const.WELCOME_MESSAGE)
