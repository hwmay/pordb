# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from pordb_historie import Ui_Dialog as pordb_historie
from pypordb_dblesen import DBLesen

class Historie(QtGui.QDialog, pordb_historie):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		
		self.connect(self.pushButtonGo, QtCore.SIGNAL("clicked()"), self.onGo)
		self.connect(self.pushButtonAbbrechen, QtCore.SIGNAL("clicked()"), self.close)
		
		self.row = 0
		self.column = 0
		self.zu_lesen = None
		self.tableWidgetHistory.setAlternatingRowColors(True)
		self.tableWidgetHistory.clearContents()
		
		self.zu_lesen = "select * from pordb_history order by time DESC"
		self.lese_func = DBLesen(self, self.zu_lesen)
		self.res = DBLesen.get_data(self.lese_func)
		res = DBLesen.get_data(self.lese_func)
		self.tableWidgetHistory.setRowCount(len(self.res))
		for i in self.res:
			# Checkbox
			newitem = QtGui.QTableWidgetItem()
			newitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
			newitem.setCheckState(QtCore.Qt.Unchecked)
			self.tableWidgetHistory.setItem(self.row, self.column, newitem)
			# Befehl
			self.column += 1
			newitem = QtGui.QTableWidgetItem(i[0].decode("utf-8"))
			self.tableWidgetHistory.setItem(self.row, self.column, newitem)
			# Time
			self.column += 1
			newitem = QtGui.QTableWidgetItem(str(i[1]))
			self.tableWidgetHistory.setItem(self.row, self.column, newitem)
			self.column = 0
			self.row += 1
		self.tableWidgetHistory.resizeColumnsToContents()
		
	def onGo(self):
		for i in range(len(self.res)):
			if self.tableWidgetHistory.item(i, 0).checkState():
				self.zu_lesen = unicode(self.tableWidgetHistory.item(i, 1).text().replace('"', "'")).encode("utf-8")
				break
		
		self.close()
