#!usr/bin/python

########################################
#	By: K                              #
#	Copyleft: Creative Commons         #
#	Usa, modifica, distribuye          #
#	y no olvides referenciar.          #
#	El mundo es de los geeks!!         #
########################################

import sys
import re


class Validar(object):
	"""docstring for Valida"""
	def __init__(self):
		pass


	#################################################################
	# Validar numero de control                                     #
	#################################################################
	def verificarControl(self, nControl):

		print('\nValidando el numero de control...')
		#Creamos una expresion regular que solo acepte numeros.
		expReg = r'[0-9]+'

		# Se compara con el valor de nControl
		if ((nControl.isdigit()) and re.match(expReg, nControl)):
			return True
			pass
		else:

			return False
		pass

	#################################################################
	# Verificar el numero de maquina  #
	#################################################################
	def verificarMaquina(self, maquina):
		print('Validando numero de maquina')

		expReg = r'[0-9]+'
		if ((maquina.isdigit()) and re.match(expReg, maquina)):
			return True
			pass
		elif(not maquina.isdigit()):
			print('\tSintaxis no valida\n')
			return False
			pass
		pass
	
	pass

#################################################################
# En esta funcion revisamos si una maquina esta libre o esta    #
# ocupadas                                                      #
#################################################################
	def estatus(self, nMaquina):
		pass

'''

revisar = Validar()
nControl = 11590163

resultado = revisar.verificarControl(nControl)
if resultado == True:
	print('Nmero %d de control valido' %nControl)
	pass
else:
	print('Numero de control no valido :(')

'''