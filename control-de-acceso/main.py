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
import serial

from threading import Timer
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


#Cargamos la interfaz de usuario

from registro import Ui_Usuario

from modulos.conexion import Conectar
#Importamos el modulode validacion.
from modulos.validar import Validar
# Importamos el modulo Escanner
from modulos.escanner import Escanner
# Importamos la clase Hora, que nos regresara la fecha y hora actual.
from modulos.fecha import Tiempo

#################################################################
# Clase de inicializacion del modulo, se carga la interfaz      #
# y se conectan los eventos de los botones con sus respectivas  #
# funciones.                                                    #
#################################################################

class Registro(QtWidgets.QMainWindow, Ui_Usuario):
	"""docstring for Registro"""
	def __init__(self):

		super(Registro, self).__init__()
		
		self.setupUi(self)


		self.nControl.textChanged.connect(self.validarControl)
		self.bIngresar.setEnabled(False)
		#self.textEdit.appendPlainText("\nSending a remote call to myFunction()...")
		self.plainLog.appendPlainText('Inicializando el sistema :)')
		self.plainLog.appendPlainText('Sistema listo...\n\n')
		# Configuraciones para el reloj
		
		self.tiempoActual = QtCore.QTime(0,0,0)
		self.reloj.display(self.tiempoActual.toString('hh:mm:ss'))

		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.actualizarReloj)
		self.timer.start(1000)

		self.libres = []
		self.ocupadas = []

		for x in range(1,54):
			self.libres.append(x)
			#self.labels.append('PC_'+ str(x))
			pass
		#print(self.labels)

		# Usamos un diccionario para controlar quienes estan usando cierta maquina,
		# y si esta esta libre u ocupada
		# para ello usamos un diccionario PC_XX : nControl, odnde cada PC esta asignada 
		# a un usuario en cierto momento.

		self.pcUsr = {}

		# LLenamos le diccionario, donde el valor sera 0 para todas las maquinas.
		for x in range(1,54):
			self.pcUsr[x] = 0
			pass


		#conexion = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1.0)

		# Conectamos los eventos de los botones con sus respectivas 
		# funciones
	
		pass

#################################################################
# Mostramos la hora actual en el QLCDNumber                     #
#################################################################
	def actualizarReloj(self):

		obtener = Tiempo()
		hora = obtener.hora()
		self.reloj.setDigitCount(8)
		self.reloj.display(hora)
		pass


#################################################################
# Realizamos la validacion del numero de control                #
#################################################################
	def validarControl(self):
		# Obtenemos el texto del QLineEdit, nControl
		lineControl = self.nControl.text()

		# Revisamos que la cadena de caracteres se corresponda con la longitud
		# de un numero de control, cuando se cumple , se llama a verificarControl

		if len(lineControl) == 8:
			revisar = Validar() 
			resultado = revisar.verificarControl(lineControl)
			if (resultado == True):
				print('\tNumero de control %s valido \n' %str(lineControl))
				self.plainLog.appendPlainText('\t\n\nNumero de control %s valido' %str(lineControl))
				self.plainLog.appendPlainText('-------------------------------------------------------------------------')
				# Ya que se ha verificado nControl, se obtiene la informacion 
				# realcionadoa a dicho valor
				self.obtenerDatos(lineControl)
				pass
			elif(resultado == False):
				print('\tNumero de control no valido!!')
				self.plainLog.appendPlainText('\tNumero de control no valido!!')
				self.plainLog.appendPlainText('-------------------------------------------------------------------------')
			
			pass
		pass

#################################################################
# Obtenemos los datos del alumno en base a su nume`ro de control #
#################################################################
	def obtenerDatos(self, nControl):

		# Instanciamos la clase Conectar
		llamar = Conectar()

		# Preparamos la consulta a realizar, en este caso los datos relacionados
		# al numeri de control introducido
		sentencia= "select nombre, pApellido, mApellido, carrera from alumnos where nControl = %d;" %int(nControl)

		# Se llama a la funcion de condulta de la clase Conectar y pasamos 
		# la consulta como parametro.
		resultado = llamar.consulta(sentencia)
		
		''' Si bien se podria hacer de otra forma, como en este caso simplemente asignamos
		los resultados de la consulta a los campos correspondientes, es rapido y directo.
		'''
		self.nombre.setText(resultado[0][0])
		self.apellidos.setText(resultado[0][1] + ' ' + resultado[0][2])
		self.carrera.setText(resultado[0][3])

		# Mover a la funcion de limopieza
		resultado = ''

		# Ahora obtenemos el numero de maquina y procedemos a realiazr el registro de acceso.
		
		# Cambiamos el cursor al campo de numero de maquina
		self.maquina.setFocus()

		# Si cambia el texto en al campo 'maquina', validamos el mismo
		#self.maquina.textChanged.connect(self.validarMaquina)
	
#################################################################
# Validar numero de                                             #
#################################################################
	def validarMaquina(self):
		
		# Obtenemos el texto del QLineEdit
		nMaquina = self.maquina.text()
		

		#Instanciamos la clase Validar
		opcion = Validar()
		# Hora validamos que posea una sintaxis valida
		# Usamos la instanciasion previa de la clase Validar
		# Obtenemos el rasultado de validarMaquina
		resultado = opcion.verificarMaquina(nMaquina)

		# Revisamos si esta ocupada o no
		disponible = True
		for x in range(0, len(self.ocupadas)):
			if (resultado == True and self.ocupadas[x] == int(nMaquina)):
				disponible = False
				pass
			pass
		# Ahora usamos el estatus de disponibilidad para poder validar el resto

		if (resultado == True and int(nMaquina) <= int(len(self.libres))):
			# Si esta disponible...
			if disponible == True:
				print('\tMaquina disponible, validando datos. . .')				
				self.plainLog.appendPlainText('\tValidadando datos... maquina %s disponible' %nMaquina)

				# si el resultado es valido...
				if resultado == True:
					print('\tNumero de maquina valido')
					self.plainLog.appendPlainText('\tNumero de maquina valido')
					# Agregamos la nMaquina a la lista de ocupadas
					self.ocupadas.append(int(nMaquina))
					#Marcamos la maquina en cuestion como ocupada en el diagrama 
					self.mapa(nMaquina)
					return True
					pass
				elif resultado == False:
					print('\nNumero de maquina no valido :(!')
					self.plainLog.appendPlainText('\tNumero de maquina no valido :(')
					return False
					pass
				pass
			elif disponible == False:
				print('\n\tMaquina %s Ocupada' %nMaquina)
				self.plainLog.appendPlainText('\tMaquina %s: Ocupada' %nMaquina)
				return False
				pass
			pass
		elif ( resultado == True and int(nMaquina) > int(len(self.libres)) ):
			print('\tEsta maquina aun no existe, :P!!')
			self.plainLog.appendPlainText('\tEsta maquina aun no existe :P!!')
			return False
			pass
		elif (resultado == False):
			print('\t Ups, creo eso no es un numero :}- \t Intenta nuevamente :)')
			self.plainLog.appendPlainText('\t Ups, creo que eso no es un numero :}- \n Intenta nuevamente :)')
			# Si el resultado es falso, ponemos el cursor sobre el TextEdit de maquina
			self.maquina.setFocus()
			self.maquina.setText('')
			pass
		pass

#################################################################
# Marcamos la maquina como no dosponible en el mapa             #
#################################################################
	def mapa(self, nMaquina):
		pc = 'PC_' + nMaquina
		self.__dict__[pc].setText('N/D')
		
		pass

#################################################################
# Registramos la salida y liberamos la maquina en cuation       #
#################################################################

	def libreOcupada(self, nMaquina, nControl):
		# Obtenemos la clave y valor del diccionario
		for pc, usr in pcUsr.items():
			if pc == nMaquina and usr == nControl:
				print('Maquina %s ocupada por  el usuario %s' %(nMaquina,nControl))
				print('Liberando la maquina %s!' %nMaquina)
				pcUsr[nMaquina] = 0
				print('Salida completada con exito, adios!')
				return False
				pass
			elif pc == nMaquina and usr == 0:
				print('Maquina %s libre' %pc)
				print('Asignando maquina %s al usuario %d' %(nMaquina, nControl))
				pcUsr[nMaquina] = nControl
				pass
			elif pc == nMaquina and usr != nControl:
				print('Maquina %s ocupada' %nMaquina)
			pass

		pass



#################################################################
# Realizamos una insercion                                      #
#################################################################
	def recolectarDatos(self):
		print('\tRecolectando datos de registro :)!')
		self.plainLog.appendPlainText('\tRecolectando datos de registro')
		self.plainLog.appendPlainText('-----------------------------------------------------------------------')
		# Obtenemos la hora y la fecha de la clase Tiempo
		datos = []

		obtener = Tiempo()
	
		control = self.nControl.text()
		datos.append(int(control))

		maquina = self.maquina.text()
		datos.append(int(maquina))

		dia = obtener.fecha()
		datos.append(dia)

		hora = obtener.hora()
		datos.append(hora)
		
		return datos
		pass
#################################################################
# Detectamos evento  si se presiona la tecla enter              #
#################################################################
	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Enter:
			
			self.bIngresar.setEnabled(True)
			self.bIngresar.setFocus()
			#Validamos el numero de maquina
			esValida = self.validarMaquina()
			if esValida == True:
				# Recolectamos la informacion de los formularios, por medio de la funcion recolectarDatos()
				datos = self.recolectarDatos()
				#Preparamos la consulta 
				#INSERT INTO entrada(nControl, nMaquina, fentrada, hentrada) VALUES(11590198, 19, '23/05/15', '18:25:42')
				consulta = "INSERT INTO entrada(nControl, nMaquina, fentrada, hentrada) VALUES(%d, %d, '%s', '%s')" %(int(datos[0]), int(datos[1]), datos[2], datos[3])
				
				# Realizamos el registro de entrada.
				#print(consulta)
				intentar = Conectar()
				resultado = intentar.insertar(consulta)

				print('#############################################################')
				pass
			elif esValida == False:

				print('\tIntente con otra maquina')
				self.plainLog.appendPlainText('\tIntete con otra maquina')
				# Dado que no esta disponible enfocamos self.maquina y borramos el contenido previo
				self.maquina.setFocus()
				self.maquina.setText('')
				print('#############################################################')
				self.plainLog.appendPlainText('-------------------------------------------------------------------------')
				pass
			#print('Ok, ahora recolectamos los datos :)')
			
			
			pass
		pass



#################################################################
# Ejecutamos la aplicacion	                                    #
#################################################################

if __name__ == '__main__':

	# Creamos un objeto de tipo QApplication
	App = QtWidgets.QApplication(sys.argv)
	# Instanciamos la clase Registro
	registro = Registro()
	# Hacemos visible la aplicacion
	
	registro.show()

	# Capturamos los eventos de la ventana(en este caso la salida)
	sys.exit(App.exec_())