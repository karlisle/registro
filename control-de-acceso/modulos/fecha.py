#!usr/bin/python

########################################
#	By: Kharl                          #
#	Copyleft: Creative Commons         #
#	Usa, modifica, distribuye          #
#	y no olvides referenciar.          #
#	El mundo es de los lo contruyen!!  #
########################################

import sys
import time



class Tiempo(object):
	"""docstring for Hora"""
	def __init__(self):
		pass

	def fecha(self):
		return time.strftime('%y/%m/%d')
		pass

	def hora(self):
		return time.strftime("%H:%M:%S")
		pass
	pass