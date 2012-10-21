# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import psycopg2
import psycopg2.extensions

class DBLesen():
	def __init__(self, fenster, zu_lesen):
		self.fenster = fenster
		self.zu_lesen = str(zu_lesen)
		self.res = []
		self.conn = None
		self.cur = None
		
	def get_data(self):
		db_host="localhost"
		try:
			self.conn = psycopg2.connect(database="por", host=db_host)
		except Exception, e:
			print e
			message = QtGui.QMessageBox.critical(self.fenster, self.fenster.trUtf8("Error "), str(e))
			return 
		self.cur = self.conn.cursor()
		try:
			self.cur.execute(self.zu_lesen)
		except Exception, e:
			print self.zu_lesen, type(self.zu_lesen)
			print e
			message = QtGui.QMessageBox.critical(self.fenster, self.fenster.trUtf8("Error "), str(e))
			return 
		self.res = self.cur.fetchall()
		return self.res
