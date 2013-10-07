# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from pordb_pseudo import Ui_Pseudo as pordb_pseudo
from pypordb_dbupdate import DBUpdate

class PseudonymeBearbeiten(QtGui.QDialog, pordb_pseudo):
	def __init__(self, darsteller, pseudonyme):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		
		self.connect(self.pushButtonPseudo, QtCore.SIGNAL("clicked()"), self.onPseudo)
		self.connect(self.pushButtonSpeichern, QtCore.SIGNAL("clicked()"), self.onSpeichern)
		self.connect(self.pushButtonAbbrechen, QtCore.SIGNAL("clicked()"), self.close)
		
		self.darsteller = darsteller.lstrip('=').decode("utf-8").replace("'", "''")
		self.setWindowTitle(self.trUtf8("Edit aliases for ") +self.darsteller.replace("''", "'"))
		row = 0
		column = 0
		self.lineEditPseudo.setFocus()
		self.tableWidgetPseudo.clearContents()
		for i in pseudonyme:
			for j in i:
				newitem = QtGui.QTableWidgetItem(j.decode("utf-8").strip())
				self.tableWidgetPseudo.setItem(row, column, newitem)
				row += 1
		self.tableWidgetPseudo.setAlternatingRowColors(True)
		self.tableWidgetPseudo.resizeColumnsToContents()
		self.tableWidgetPseudo.resizeRowsToContents()
		
	def onPseudo(self):
		pseudos = unicode(self.lineEditPseudo.text()).strip().split(",")
		row = 0
		column = 0
		for i in pseudos:
			if len(i) > 0:
				newitem = QtGui.QTableWidgetItem(i.strip())
				self.tableWidgetPseudo.setItem(row, column, newitem)
				row += 1
	
	def onSpeichern(self):
		zu_erfassen = []
		zu_erfassen.append("delete from pordb_pseudo where darsteller = '" +self.darsteller +"'")
		
		position = 0
		for i in range(self.tableWidgetPseudo.rowCount()):
			cell = []
			position += 1
			for j in range(self.tableWidgetPseudo.columnCount()):
				tableItem = self.tableWidgetPseudo.item(i, j)
				try:
					cellItem = unicode(QtGui.QTableWidgetItem(tableItem).text()).decode("utf-8")
					cell.append(cellItem)
				except:
					pass
			if cell and cell[0]:
				zu_erfassen.append("insert into pordb_pseudo (pseudo, darsteller) values ('" +cell[0].title().replace("'", "''") +"', '" +self.darsteller +"')")
			    
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		
		self.close()
