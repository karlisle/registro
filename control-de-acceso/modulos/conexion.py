#!usr/bin/python

########################################
#	By: K                              #
#	Copyleft: Creative Commons         #
#	Usa, modifica, distribuye          #
#	y no olvides referenciar.          #
#	El mundo es de los geeks!!         #
########################################

import pymysql

class Conectar(object):
	def __init__(self):
		pass

		self.conn = pymysql.connect(host="localhost", port=3306, user="root",passwd="d-music", db="registro")

		self.cursor = self.conn.cursor()
		pass
		
#####################################################################

	def insertar(self, query):
		try:
			self.cursor.execute(query)
			self.conn.commit()
			self.conn.close()
			return True
			pass
		except Exception:
			return False
		
		pass

#####################################################################

	def consulta(self, consulta):
		try:
			self.cursor.execute(consulta)
			datos = self.cursor.fetchall()
			return datos
		except Exception:
			self.conn.rollback()
			self.conn.close()
			return False

		pass
	pass
'''

llamar = Conectar()


nControl = 11590163
nMaquina = 10

sentencia = "SELECT * FROM alumnos"
sentencia2 = "INSERT INTO entrada(nControl, nMaquina, fentrada, hentrada) VALUES(11590198, 19, '23/05/15', '18:25:42')"
consulta = "select id_entrada as ID, nMaquina as Maquina, nControl as Control  from entrada where nControl = %d and nMaquina = %d;" %(nControl, nMaquina)

resultado = llamar.consulta(consulta)

#llamar.insertar(sentencia2)

ultimo = len(resultado)

print('ID: ',resultado[ultimo -1][0])
print('nMaquina: ',resultado[ultimo -1][1])
print('nControl: ',resultado[ultimo -1][2])

'''