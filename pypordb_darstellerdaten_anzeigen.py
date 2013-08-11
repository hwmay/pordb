# -*- coding: iso-8859-1 -*-

import os
import urllib
import time
from PyQt4 import QtGui, QtCore
from pordb_iafd import Ui_DatenausderIAFD as pordb_iafd
from pypordb_dblesen import DBLesen
from pypordb_dbupdate import DBUpdate

class DarstellerdatenAnzeigen(QtGui.QDialog, pordb_iafd):
	def __init__(self, app, url, darstellerseite, verzeichnis_thumbs):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		
		self.connect(self.pushButtonUebernehmen, QtCore.SIGNAL("clicked()"), self.onUebernehmen)
		self.connect(self.pushButtonCancel, QtCore.SIGNAL("clicked()"), self.onClose)
		
		self.darstellerseite = darstellerseite
		self.app = app
		self.url = url
		self.verzeichnis_thumbs = verzeichnis_thumbs
		
		self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		
		monate = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12", }
		haarfarben = {"Brown":"br", "Brown/Light Brown":"br", "Dark Brown":"br", "Light Brown":"br", "Black":"s", "Red":"r", "Blond":"bl", "Honey Blond":"bl", "Dark Blond":"bl", "Dirty Blond":"bl", "Sandy Blond":"bl", "Strawberry Blond":"bl", "Auburn":"r"}
		ethniticies = {"Caucasian": "w", "Black": "s", "Asian": "a", "Latin": "l"}
		self.coding = "iso-8859-1"
		
		# Darsteller Name
		anfang = self.darstellerseite.find('<h1>')
		if anfang < 0:
			self.app.restoreOverrideCursor()
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("This site seams not to be an actor site of the IAFD"))
			return
		ende = self.darstellerseite.find('</h1>', anfang)
		self.name = self.darstellerseite[anfang+4:ende].decode(self.coding).strip()
		self.labelName.setText(self.name)
		self.lineEditName.setText(self.name)
			
		# Darsteller Bild
		anfang = self.darstellerseite.find('/graphics/headshots/')
		if anfang < 0:
			self.app.restoreOverrideCursor()
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("This site seams not to be an actor site of the IAFD"))
			return
		ende = self.darstellerseite.find('"></div>', anfang)
		self.bild = (self.darstellerseite[anfang+20:ende].decode(self.coding)) 
		url =  'http://www.iafd.com/graphics/headshots/' + self.bild
		self.verz = os.path.expanduser("~") +os.sep +"tmp"
		urllib._urlopener=urllib.URLopener()
		urllib.URLopener.version="Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; T312461)"
		urllib.FancyURLopener.prompt_user_passwd = lambda self, host, realm: (None, None)
		while True:
			try:
				bild=urllib.urlretrieve(url, self.verz +os.sep +self.bild)
				break
			except:
				pass
		bild = QtGui.QPixmap(self.verz +os.sep +self.bild)
		self.labelBild.setPixmap(bild)
			
		# Darsteller Geschlecht
		anfang = self.darstellerseite.find('&amp;gender=')
		ende = self.darstellerseite.find('"', anfang)
		self.geschlecht = self.darstellerseite[anfang+12:ende].decode(self.coding)
		if self.geschlecht == "f":
			self.geschlecht = "w"
		elif self.geschlecht != "m":
			self.app.restoreOverrideCursor()
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("This site seams not to be an actor site of the IAFD"))
			return
		self.lineEditGeschlecht.setText(self.geschlecht)
		
		# Darsteller Pseudonyme
		anfang = self.darstellerseite.find('AKA</b>')
		anfang = self.darstellerseite.find('</td><td>', anfang)
		ende = self.darstellerseite.find('</td>', anfang+1)
		self.pseudonyme = self.darstellerseite[anfang+9:ende].decode(self.coding)
		if self.pseudonyme != "No known aliases":
			self.lineEditPseudo.setText(self.pseudonyme)
	
		# Darsteller Land
		anfang = self.darstellerseite.find('Nationality/Heritage</b></td><td>')
		ende = self.darstellerseite.find('</td></tr>', anfang)
		self.land = self.darstellerseite[anfang+33:ende].decode(self.coding)
		if self.land == "No data":
			self.lineEditLand.setText("")
		else:
			self.lineEditLand.setText(self.land)
			zu_lesen = "select iso from pordb_iso_land where national = '" +self.land + "'"
			self.lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(self.lese_func)
			if len(res) > 0:
				self.lineEditLand.setText(res[0][0])
		
		# Darsteller Ethnic
		anfang = self.darstellerseite.find('Ethnicity</b></td><td>')
		ende = self.darstellerseite.find('</td></tr>', anfang)
		self.ethnic = self.darstellerseite[anfang+22:ende].decode(self.coding)
		ethnic = ethniticies.get(self.ethnic, self.trUtf8("nicht vorhanden"))
		if ethnic != self.trUtf8("nicht vorhanden"):
			self.ethnic = ethnic
		self.lineEditEthnic.setText(self.ethnic)
		
		# Darsteller Haarfarbe
		anfang = self.darstellerseite.find('Hair Colors</b></td><td>')
		offset = 24
		if anfang < 0:
			anfang = self.darstellerseite.find('Hair Color</b></td><td>')
			offset = 23
		ende = self.darstellerseite.find('</td></tr>', anfang)
		self.haare = self.darstellerseite[anfang+offset:ende].decode(self.coding)
		haarfarbe = haarfarben.get(self.haare, self.trUtf8("nicht vorhanden"))
		if haarfarbe != self.trUtf8("nicht vorhanden"):
			self.haare = haarfarbe
		self.lineEditHaare.setText(self.haare)
		
		# Darsteller Tattoos
		anfang = self.darstellerseite.find('Tattoos</b></td><td>')
		ende = self.darstellerseite.find('</td>', anfang+20)
		self.tattoos = self.darstellerseite[anfang+20:ende].decode(self.coding)
		if self.tattoos == "None" or self.tattoos == "none":
			self.lineEditTattos.setText("-")
		elif self.tattoos == "No data" or self.tattoos == "No Data":
			self.lineEditTattos.setText(" ")
		else:
			self.lineEditTattos.setText(self.tattoos)
			
		# Darsteller Geboren
		anfang = self.darstellerseite.find('<b>Birthday')
		anfang = self.darstellerseite.find('">', anfang)
		ende = self.darstellerseite.find('</a>', anfang)
		self.geboren = self.darstellerseite[anfang+2:ende].decode(self.coding)
		monat = monate.get(self.geboren[0:self.geboren.find(" ")], self.trUtf8("not available"))
		if monat != self.trUtf8("not available"):
			tag = self.geboren[self.geboren.find(" ")+1:self.geboren.find(",")]
			jahr = self.geboren[self.geboren.find(", ")+2:]
			self.geboren = jahr +"-" + monat + "-" + tag
			self.labelGeboren.setText(self.geboren)
		else:
			self.geboren = 0
			self.labelGeboren.setText("-")
		
		# Darsteller Anzahl Filme
		anfang = self.darstellerseite.find('moviecount">')
		if anfang > 0:
			ende = self.darstellerseite.find(' Title', anfang+1)
			self.filme = self.darstellerseite[anfang+12:ende].decode(self.coding)
		else:
			self.filme = 0
		
		# Darsteller aktiv von / bis
		anfang = self.darstellerseite.find('Years Active</b></td><td>')
		if anfang == -1:
			anfang = self.darstellerseite.find('Years Active as Performer</b></td><td>') 
			if anfang == -1:
				anfang = self.darstellerseite.find('Year Active</b></td><td>') + 24
			else:
				anfang += 38
		else:
			anfang += 25
		aktiv_von = self.darstellerseite[anfang:anfang + 4].decode(self.coding)
		try:
			self.aktiv_von_int = int(aktiv_von)
		except:
			self.aktiv_von_int = 0
		aktiv_bis = self.darstellerseite[anfang + 5:anfang + 9].decode(self.coding)
		try:
			self.aktiv_bis_int = int(aktiv_bis)
		except:
			self.aktiv_bis_int = 0
		
		self.checkBoxPseudo.setCheckState(QtCore.Qt.Checked)
		self.checkBoxGeboren.setCheckState(QtCore.Qt.Checked)
		self.checkBoxLand.setCheckState(QtCore.Qt.Checked)
		self.checkBoxEthnic.setCheckState(QtCore.Qt.Checked)
		self.checkBoxHaare.setCheckState(QtCore.Qt.Checked)
		self.checkBoxTattos.setCheckState(QtCore.Qt.Checked)
		
		self.app.restoreOverrideCursor()
		
	def onUebernehmen(self):
		if self.lineEditGeschlecht.text() != 'm' and self.lineEditGeschlecht.text() != 'w':
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Invalid gender"))
			self.app.restoreOverrideCursor()
		if self.checkBoxName.isChecked():
			zu_lesen = "select * from pordb_darsteller where darsteller = '" +str(self.lineEditName.text()).replace("'", "''").title() +"'"
		else:
			zu_lesen = "select * from pordb_darsteller where darsteller = '" +self.name.strip().replace("'", "''").title() +"'"
		self.lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(self.lese_func)
		zu_erfassen = []
		
		# Darsteller existiert noch nicht
		if len(res) == 0:
			messageBox = QtGui.QMessageBox()
			messageBox.addButton(self.trUtf8("Yes"), QtGui.QMessageBox.AcceptRole)
			messageBox.addButton(self.trUtf8("No"), QtGui.QMessageBox.RejectRole)
			messageBox.setWindowTitle(self.trUtf8("Actor ") +self.name.strip() +self.trUtf8(" not yet in database"))
			messageBox.setIcon(QtGui.QMessageBox.Question)
			messageBox.setText(self.trUtf8("Should the actor be created?"))
			message = messageBox.exec_()
			if message == 0:
				if str(self.labelGeboren.text()).strip() == "-":
					geboren = "0001-01-01"
				else:
					geboren = str(self.labelGeboren.text())
				datum = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(time.localtime()[2])
				zu_erfassen.append("INSERT into pordb_darsteller VALUES ('" +str(self.lineEditName.text()).title().replace("'", "''") +"', '" +str(self.lineEditGeschlecht.text()) + "', '" +str(0) +"', '" +datum +"', '" +str(self.lineEditHaare.text()).lower() +"', '" +str(self.lineEditLand.text()).upper()[0:2] +"', '" +str(self.lineEditTattos.text().replace("'", "''")) +"', '" +str(self.lineEditEthnic.text()).lower() + "', '" +str(0) +"', '" +geboren +"', '" +str(self.filme) +"', '" +str(self.url).replace("'", "''") +"', '" +str(self.aktiv_von_int) +"', '" +str(self.aktiv_bis_int) +"', '" +datum +"')")
				if self.checkBoxPseudo.isChecked():
					self.pseudo_uebernehmen(str(self.lineEditName.text()), zu_erfassen)
				extension = os.path.splitext(str(self.verz +os.sep +self.bild))[-1].lower()
				if extension == ".jpeg":
					extension = ".jpg"
				if extension <> ".gif":
					newfilename = self.verzeichnis_thumbs +os.sep +"darsteller_" +self.lineEditGeschlecht.text() +os.sep +str(self.lineEditName.text()).strip().replace("'", "_apostroph_").replace(" ", "_").lower() + extension
					os.rename(self.verz +os.sep +self.bild, newfilename)
			else:
				self.close()
		# Darsteller existiert bereits
		else:
			if self.checkBoxBild.isChecked():
				extension = os.path.splitext(str(self.verz +os.sep +self.bild))[-1].lower()
				if extension == ".jpeg":
					extension = ".jpg"
				if extension <> ".gif":
					if self.checkBoxName.isChecked():
						newfilename = self.verzeichnis_thumbs +os.sep +"darsteller_" +self.lineEditGeschlecht.text() +os.sep +str(self.lineEditName.text()).strip().replace("'", "_apostroph_").replace(" ", "_").lower() + extension
					else:
						newfilename = self.verzeichnis_thumbs +os.sep +"darsteller_" +self.lineEditGeschlecht.text() +os.sep +self.name.strip().replace("'", "_apostroph_").replace(" ", "_").lower() + extension
					os.rename(self.verz +os.sep +self.bild, newfilename)
			else:
				try:
					os.remove(self.verz +os.sep +self.bild)
				except:
					pass
			if self.checkBoxGeboren.isChecked():
				if str(self.labelGeboren.text()).strip() == "-":
					if res[0][9] and res[0][9] != '0001-01-01':
						pass
					else:
						zu_erfassen.append("update pordb_darsteller set geboren = '0001-01-01' where darsteller = '" +res[0][0].replace("'", "''") +"'")
				else:
					zu_erfassen.append("update pordb_darsteller set geboren = '" +str(self.labelGeboren.text()) +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			if self.checkBoxLand.isChecked() and str(self.lineEditLand.text()):
				zu_erfassen.append("update pordb_darsteller set nation = '" +str(self.lineEditLand.text()).upper() +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			if self.checkBoxEthnic.isChecked():
				zu_erfassen.append("update pordb_darsteller set ethnic = '" +str(self.lineEditEthnic.text()).lower() +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			if self.checkBoxHaare.isChecked():
				zu_erfassen.append("update pordb_darsteller set haarfarbe = '" +str(self.lineEditHaare.text()).lower() +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			if self.checkBoxTattos.isChecked() and str(self.lineEditTattos.text()):
				if len((self.lineEditTattos.text())) > 500:
					message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Too many characters in tattos (") +str(len((self.lineEditTattos.text()))) +")")
					return
				zu_erfassen.append("update pordb_darsteller set tattoo = '" +str(self.lineEditTattos.text()).replace("'", "''") +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			zu_erfassen.append("update pordb_darsteller set filme = '" +str(self.filme) +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			zu_erfassen.append("update pordb_darsteller set url = '" +unicode(self.url).encode(self.coding).replace("'", "''") +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			zu_erfassen.append("update pordb_darsteller set aktivvon = '" +str(self.aktiv_von_int) +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			zu_erfassen.append("update pordb_darsteller set aktivbis = '" +str(self.aktiv_bis_int) +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			if self.checkBoxPseudo.isChecked():
				zu_erfassen.append("delete from pordb_pseudo where darsteller = '" +res[0][0].replace("'", "''") + "'")
				self.pseudo_uebernehmen(res[0][0], zu_erfassen)
				
			datum = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(time.localtime()[2])
			zu_erfassen.append("update pordb_darsteller set besuch = '" +datum +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
				
		if zu_erfassen:
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
		self.close()
	# end of onUebernehmen
		
	def pseudo_uebernehmen(self, name, zu_erfassen):
		pseudos = unicode(self.lineEditPseudo.text()).split(", ")
		for i in pseudos:
			if i and i.title() != name.title().strip():
				if pseudos.count(i.title()) > 1:
					pass
				else:
					zu_erfassen.append("insert into pordb_pseudo (pseudo, darsteller) values ('" +i.title().strip().replace("'", "''") +"', '" +name.title().replace("'", "''") +"')")
					
	def onClose(self):
		try:
			os.remove(self.verz +os.sep +self.bild)
		except:
			pass
		self.close()
