# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from pordb_original import Ui_Dialog as pordb_original

class OriginalErfassen(QtGui.QDialog, pordb_original):
	def __init__(self, original_weitere=None, parent=None):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)

		self.original_weitere = original_weitere
		if self.original_weitere:
			row = 0
			self.tableWidget.clearContents()
			for i in self.original_weitere:
				newitem = QtGui.QTableWidgetItem(i.strip().decode("utf-8"))
				self.tableWidget.setItem(row, 0, newitem)
				row += 1

		self.connect(self.pushButtonSpeichern, QtCore.SIGNAL("clicked()"), self.onSpeichern)
		self.connect(self.pushButtonAbbrechen, QtCore.SIGNAL("clicked()"), self.close)
		
	def onSpeichern(self):
		self.original = []
		for i in range(10):
			tableItem = self.tableWidget.item(i, 0)
			if tableItem:
				cellItem = unicode(QtGui.QTableWidgetItem(tableItem).text()).encode("utf-8")
				self.original.append(cellItem)
		self.close()
