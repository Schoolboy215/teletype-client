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

	def write(self,buffer):
		if enableSerial:
			buffer = wordWrap.correctWidth(buffer,33)
			self.printer.write(buffer.encode('ascii',errors='ignore'))
			self.printer.feed()
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
	def feed(self,linesToFeed):
		if enableSerial:
			self.printer.feed(linesToFeed)
	def resetAll(self):
		if enableSerial:
			pass
	def welcome(self):
		if enableSerial:
			self.printer.write(wordWrap.correctWidth(const.WELCOME_MESSAGE.encode(),30))
