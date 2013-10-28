# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import psycopg2
import psycopg2.extensions

class DBUpdate():
	def __init__(self, fenster, update):
		self.fenster = fenster
		self.update = update
		self.conn = None
		self.cur = None
		db_host='localhost'
		try:
			self.conn = psycopg2.connect(database="por", host=db_host)
		except Exception, e:
			print e
			message = QtGui.QMessageBox.critical(self.fenster, self.fenster.trUtf8("Fehler "), str(e))
			return 
		self.cur = self.conn.cursor()
		
	def update_data(self):
		update_db = []
		if type(self.update) == str or type(self.update) == unicode or type(self.update) ==  QtCore.QString:
			update_db.append(self.update)
		else:
			for i in self.update:
				try:
					update_db.append(unicode(i))
				except:
					update_db.append(i)
		for i in update_db:
			try:
				self.cur.execute(i)
			except Exception, e:
				print "Error:", e
				print i
				message = QtGui.QMessageBox.critical(self.fenster, self.fenster.trUtf8("Error "), str(e))
				return 
		self.commit()
		
	def commit(self):
		self.conn.commit()
		self.cur.close()
		self.conn.close()
