#!usr/bin/python

########################################
#	By: Kharl                          #
#	Copyleft: Creative Commons         #
#	Usa, modifica, distribuye          #
#	y no olvides referenciar.          #
#	El mundo es de los lo contruyen!!  #
########################################

import time


class Escanner():
		
	def escanear(self):

		try:
			import serial
			nControl = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1.0)
			pass
		except (ImportError, serial.SerialException):
			print('Error')
			pass

		with nControl:
			while True:
				try:
					linea = nControl.readline()
					valor = linea.decode("utf-8")
					return valor
					pass
				except KeyboardInterrupt:
					print('Saliendo')
				pass
		pass
	pass