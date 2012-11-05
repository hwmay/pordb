#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import datetime
import platform
import urllib2
import gobject # verhindert Absturz bei Anzeige von Webseiten mit Flash
import psycopg2
from PyQt4 import QtGui, QtCore
from PyQt4.QtWebKit import QWebPage
from PyQt4.QtWebKit import QWebFrame
import PyQt4.QtWebKit as webkit
from pordb_hauptdialog import Ui_MainWindow as MainWindow

from pypordb_suchen import Suchen
from pypordb_cover import Cover
from pypordb_neu import Neueingabe
from pypordb_dblesen import DBLesen
from pypordb_dbupdate import DBUpdate
from pypordb_original import OriginalErfassen
from pypordb_darsteller_suchen import DarstellerSuchen
from pypordb_darsteller_anzeige_gross import DarstellerAnzeigeGross
from pypordb_darsteller_umbenennen import DarstellerUmbenennen
from pypordb_land import LandBearbeiten
from pypordb_suchbegriffe import SuchbegriffeBearbeiten
from pypordb_suche_video import SucheVideo
from pypordb_historie import Historie
from pypordb_pseudo import PseudonymeBearbeiten
from pypordb_bookmarks import Bookmarks
from pypordb_darstellerdaten_anzeigen import DarstellerdatenAnzeigen
from pypordb_devices import Devices

size = QtCore.QSize(260, 260)
sizeneu = QtCore.QSize(500, 400)
size_neu = QtCore.QSize(130, 130)
size_darsteller = QtCore.QSize(1920, 1080)

dbname = "por"
initial_run = True

__version__ = "5.4.2"

# Make a connection to the database and check to see if it succeeded.
db_host = "localhost"
try:
	conn = psycopg2.connect(database=dbname, host=db_host)
except Exception, e:
	print "FATAL PorDB: Database server not running"
	sys.exit()

def age(dob):
	today = datetime.date.today()
	if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
		return today.year - dob.year - 1
	else:
		return today.year - dob.year
# end of age

class MeinDialog(QtGui.QMainWindow, MainWindow):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		
		# Slot für Splitter zum Re-Scalen des Darstellerbildes
		self.connect(self.splitter, QtCore.SIGNAL("splitterMoved(int, int)"), self.bildSetzen)
		
		# Slot für Aktivieren von Buttons bei Wechsel des Tabs
		self.connect(self.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.onTabwechsel)
		
		# Slots einrichten für Bilder
		self.connect(self.actionNeueingabe, QtCore.SIGNAL("triggered()"), self.onNeueingabe)
		self.connect(self.actionDarsteller, QtCore.SIGNAL("triggered()"), self.onDarsteller)
		self.connect(self.actionCd, QtCore.SIGNAL("triggered()"), self.onCD)
		self.connect(self.actionTitel, QtCore.SIGNAL("triggered()"), self.onTitel)
		self.connect(self.actionOriginal, QtCore.SIGNAL("triggered()"), self.onOriginal)
		self.connect(self.actionSuche, QtCore.SIGNAL("triggered()"), self.onSuche)
		self.connect(self.actionCoverErstellen, QtCore.SIGNAL("triggered()"), self.onCover)
		self.connect(self.actionDrucken, QtCore.SIGNAL("triggered()"), self.onDrucken)
		self.connect(self.tableWidgetBilder, QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.onKorrektur)
		self.connect(self.tableWidgetBilderAktuell, QtCore.SIGNAL("cellDoubleClicked(int, int)"), self.onNeuDoubleClick)
		self.connect(self.tableWidgetBilder, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContexttableWidgetBilder)
		self.connect(self.actionDarstellerUebernehmen, QtCore.SIGNAL("triggered()"), self.onDarstellerUebernehmen)
		self.connect(self.actionAnzeigenOriginal, QtCore.SIGNAL("triggered()"), self.onAnzeigenOriginal)
		self.connect(self.actionSortieren_nach_Darsteller, QtCore.SIGNAL("triggered()"), self.onSortieren_nach_Darsteller)
		self.connect(self.actionSortieren_nach_CD, QtCore.SIGNAL("triggered()"), self.onSortieren_nach_CD)
		self.connect(self.actionSortieren_nach_Titel, QtCore.SIGNAL("triggered()"), self.onSortieren_nach_Titel)
		self.connect(self.actionOriginal_umbenennen, QtCore.SIGNAL("triggered()"), self.onOriginal_umbenennen)
		self.connect(self.actionOriginal_weitere, QtCore.SIGNAL("triggered()"), self.onOriginal_weitere)
		self.connect(self.actionSortieren_nach_Original, QtCore.SIGNAL("triggered()"), self.onSortieren_nach_Original)
		self.connect(self.actionOriginalIntoClipboard, QtCore.SIGNAL("triggered()"), self.onOriginalIntoClipboard)
		self.connect(self.actionCovergross, QtCore.SIGNAL("triggered()"), self.onCovergross)
		self.connect(self.tableWidgetBilderAktuell, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContexttableWidgetBilderAktuell)
		self.connect(self.actionBildLoeschen, QtCore.SIGNAL("triggered()"), self.onBildLoeschen)
		self.connect(self.actionLand, QtCore.SIGNAL("triggered()"), self.onLand)
		self.connect(self.actionSuchbegriffe, QtCore.SIGNAL("triggered()"), self.onSuchbegriffe)
		self.connect(self.actionSucheVideo, QtCore.SIGNAL("triggered()"), self.onSucheVideo)
		self.connect(self.actionFirst, QtCore.SIGNAL("triggered()"), self.onPageFirst)
		self.connect(self.actionPrev, QtCore.SIGNAL("triggered()"), self.onPageUp)
		self.connect(self.actionNext, QtCore.SIGNAL("triggered()"), self.onPageDown)
		self.connect(self.actionLast, QtCore.SIGNAL("triggered()"), self.onPageLast)
		self.connect(self.actionUndo, QtCore.SIGNAL("triggered()"), self.onUndo)
		self.connect(self.actionOnHelp, QtCore.SIGNAL("triggered()"), self.onHelp)
		self.connect(self.pushButtonDir, QtCore.SIGNAL("clicked()"), self.onDirectoryChange)
		
		# Slots einrichten für Darsteller
		self.connect(self.bildAnzeige, QtCore.SIGNAL("clicked()"), self.onbildAnzeige)
		self.connect(self.pushButtonDarstellerspeichern, QtCore.SIGNAL("clicked()"), self.onDarstellerspeichern)
		self.connect(self.pushButtonIAFDholen, QtCore.SIGNAL("clicked()"), self.onIAFD)
		self.connect(self.pushButtonIAFDBackground, QtCore.SIGNAL("clicked()"), self.onIAFDBackground)
		self.connect(self.pushButtonDarstellerLoeschen, QtCore.SIGNAL("clicked()"), self.onDarstellerloeschen)
		self.connect(self.listWidgetDarsteller, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContextDarsteller)
		self.connect(self.actionAnzeigenPaar, QtCore.SIGNAL("triggered()"), self.onAnzeigenPaar)
		self.connect(self.labelBildanzeige, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onBildgross)
		self.connect(self.actionBildanzeigegross, QtCore.SIGNAL("triggered()"), self.onDarstellerGross)
		self.connect(self.listWidgetFilme, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContextFilm)
		self.connect(self.actionFilm_zeigen, QtCore.SIGNAL("triggered()"), self.onFilm_zeigen)
		self.connect(self.listWidgetStatistik, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.onContextCS)
		self.connect(self.actionCSZeigen, QtCore.SIGNAL("triggered()"), self.onCSZeigen)
		self.connect(self.pushButtonDarstellerSuchen, QtCore.SIGNAL("clicked()"), self.onDarstellerSuchen)
		self.connect(self.pushButtonUmbenennen, QtCore.SIGNAL("clicked()"), self.onDarstellerUmbenennen)
		self.connect(self.pushButtonDarstellerBild, QtCore.SIGNAL("clicked()"), self.onDarstellerBild)
		self.connect(self.pushButtonSort, QtCore.SIGNAL("clicked()"), self.onFilmeSortieren)
		self.connect(self.pushButtonPartnerZeigen, QtCore.SIGNAL("clicked()"), self.onPartnerZeigen)
		self.connect(self.pushButtonPseudo, QtCore.SIGNAL("clicked()"), self.onPseudo)
		
		# Slots einrichten für Dateien suchen
		self.connect(self.pushButtonSuchen, QtCore.SIGNAL("clicked()"), self.onSuchen)
		self.connect(self.pushButtonClear, QtCore.SIGNAL("clicked()"), self.onClear)
		self.connect(self.pushButtonUebernehmen, QtCore.SIGNAL("clicked()"), self.onDateinamenUebernehmen)
		
		# Slots einrichten für Web
		self.connect(self.webView, QtCore.SIGNAL("loadStarted()"), self.onLoadStarted)
		self.connect(self.webView, QtCore.SIGNAL("loadFinished (bool)"), self.onLoadFinished)
		self.connect(self.pushButtonVideo, QtCore.SIGNAL("clicked()"), self.onVideoSuchen)
		self.connect(self.pushButtonIAFD, QtCore.SIGNAL("clicked()"), self.onIAFDSeite)
		self.connect(self.pushButtonAbholen, QtCore.SIGNAL("clicked()"), self.onDarstellerdatenAbholen)
		self.connect(self.pushButtonUrl, QtCore.SIGNAL("clicked()"), self.onUrlVerwalten)
		self.connect(self.webView, QtCore.SIGNAL("linkClicked (const QUrl&)"), self.onLinkClicked)
		self.connect(self.webView, QtCore.SIGNAL("urlChanged (const QUrl&)"), self.onUrlChanged)
		
		# Slots einrichten für Statistiken
		self.connect(self.pushButtonCS, QtCore.SIGNAL("clicked()"), self.onStatistikCS)
		self.connect(self.pushButtonDarstellerW, QtCore.SIGNAL("clicked()"), self.onStatistikDarstellerW)
		self.connect(self.pushButtonDarstellerM, QtCore.SIGNAL("clicked()"), self.onStatistikDarstellerM)
		self.connect(self.pushButtonAnzahlClips, QtCore.SIGNAL("clicked()"), self.onStatistikAnzahlClips)
		self.connect(self.pushButtonClipsJahr, QtCore.SIGNAL("clicked()"), self.onStatistikAnzahlClipsJahr)
		
		# Slots einrichten für Tools
		self.connect(self.pushButtonBackup, QtCore.SIGNAL("clicked()"), self.onBackup)
		self.connect(self.pushButtonRestore, QtCore.SIGNAL("clicked()"), self.onRestore)
		self.connect(self.pushButtonWartung, QtCore.SIGNAL("clicked()"), self.onWartung)
		self.connect(self.pushButtonDateikatalog, QtCore.SIGNAL("toggled(bool)"), self.frame_Dateikatalog, QtCore.SLOT("setVisible(bool)"))
		self.frame_Dateikatalog.hide()
		self.connect(self.pushButtonVerwalten, QtCore.SIGNAL("clicked()"), self.onDevicesVerwalten)
		self.connect(self.pushButtonStart, QtCore.SIGNAL("clicked()"), self.onStartScan)
		self.connect(self.pushButtonDeleteDuplicates, QtCore.SIGNAL("clicked()"), self.onDeleteDuplicates)
		self.connect(self.pushButtonDeselect, QtCore.SIGNAL("clicked()"), self.onDeselect)
		self.pushButtonDeleteDuplicates.setEnabled(False)
		self.pushButtonDeselect.setEnabled(False)
		
		global initial_run
		if initial_run:
			bild = QtGui.QPixmap(os.getcwd() +os.sep +"pypordb" +os.sep +"8027068_splash.png").scaled(276, 246, QtCore.Qt.KeepAspectRatio)
			splash = QtGui.QSplashScreen(bild)
			splash.show()
			zu_lesen = "select * from pordb_history order by time DESC LIMIT 50"
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			if res:
				zu_erfassen = "delete from pordb_history where time < '" +str(res[-1][-1]) +"'"
				update_func = DBUpdate(self, zu_erfassen)
				DBUpdate.update_data(update_func)
			self.verzeichnis = os.path.expanduser("~") +os.sep +"mpg"
			self.verzeichnis_original = self.verzeichnis
			self.verzeichnis_thumbs = os.path.expanduser("~") +os.sep +"thumbs_sammlung"
			self.verzeichnis_trash = self.verzeichnis_thumbs +os.sep +"trash"
			self.verzeichnis_cover = self.verzeichnis_thumbs +os.sep +"cover"
			self.verzeichnis_tools = None
			settings = QtCore.QSettings()
			window_size = settings.value("MeinDialog/Size", QtCore.QVariant(QtCore.QSize(600, 500))).toSize()
			self.resize(window_size)
			window_position = settings.value("MeinDialog/Position", QtCore.QVariant(QtCore.QPoint(0, 0))).toPoint()
			self.move(window_position)
			self.restoreState(settings.value("MeinDialog/State").toByteArray())
			self.splitter.restoreState(settings.value("splitter").toByteArray())
			
		# Populate statusbar
		self.anzahl = QtGui.QLabel()
		self.statusBar.addPermanentWidget(self.anzahl)
		
		self.mpg_aktuell = QtGui.QLabel()
		self.mpg_aktuell.setText(self.trUtf8("Actual volume: "))
		self.statusBar.addPermanentWidget(self.mpg_aktuell)
		
		self.spinBoxAktuell = QtGui.QSpinBox()
		self.spinBoxAktuell.setRange(1, 9999)
		self.statusBar.addPermanentWidget(self.spinBoxAktuell)
		self.connect(self.spinBoxAktuell, QtCore.SIGNAL("valueChanged(int)"), self.onVidNeuAktualisieren)
		
		self.pushButtonHistorie = QtGui.QPushButton()
		self.pushButtonHistorie.setText(QtGui.QApplication.translate("Dialog", "Historie", None, QtGui.QApplication.UnicodeUTF8))
		self.statusBar.addPermanentWidget(self.pushButtonHistorie)
		self.connect(self.pushButtonHistorie, QtCore.SIGNAL("clicked()"), self.onHistorie)
		
		self.labelSeite = QtGui.QLabel()
		self.statusBar.addPermanentWidget(self.labelSeite)
		
		# populate toolbar
		self.suchfeld = QtGui.QComboBox()
		self.suchfeld.setMinimumWidth(250)
		self.suchfeld.setEditable(True)
		self.suchfeld.setWhatsThis(self.trUtf8("Searching field. By pressing the escape key it will be cleared and gets the focus."))
		self.toolBar.insertWidget(self.actionSuchfeld, self.suchfeld)
		self.toolBar.removeAction(self.actionSuchfeld)
		
		self.toolBar.removeAction(self.actionAnzahlBilder)
		
		self.setWindowTitle("PorDB")
		self.screen = QtGui.QDesktopWidget().screenGeometry()
		#print self.screen.width(), self.screen.height()
		if initial_run:
			splash.showMessage("Loading history", color = QtGui.QColor("red"))
			app.processEvents()
		self.historie()
		if initial_run:
			splash.showMessage("Initializing ...", color = QtGui.QColor("red"))
			for i in os.listdir(os.path.expanduser("~" +os.sep +"tmp")):
				os.remove(os.path.expanduser("~" +os.sep +"tmp" +os.sep +i))
			app.processEvents()
		
		self.aktuelle_ausgabe = " "
		self.suche_darsteller = self.suche_cd = self.suche_titel = self.suche_original = self.suche_cs = ""
		self.bilddarsteller = ""
		self.tabWidget.setCurrentIndex(0)
		self.video = False
		self.bilddarsteller = None
		self.columns = 3.0
		self.tableWidgetBilder.setColumnCount(self.columns)
		self.tableWidgetBilder.setIconSize(size)
		self.letzter_select = ""
		self.letzter_select_komplett = ""
		self.aktuelles_res = []
		self.start_bilder = 0
		self.nationen = []
		self.paarung = []
		self.bilderliste = []
		self.tableWidgetBilderAktuell.clear()
		
		self.pushButtonIAFDBackground.setEnabled(False)
		
		self.updatetimer = QtCore.QTimer()
		QtCore.QObject.connect(self.updatetimer, QtCore.SIGNAL("timeout()"), self.bilder_aktuell)
		self.connect(self.tableWidgetBilderAktuell, QtCore.SIGNAL("cellPressed(int, int)"), self.onTimerStop)
		self.updatefrequenz = 1000
		self.updatetimer.start(self.updatefrequenz)
		
		self.tableWidgetBilderAktuell.setColumnCount(1)
		self.tableWidgetBilderAktuell.setIconSize(size_neu)

		self.printer = QtGui.QPrinter(QtGui.QPrinter.ScreenResolution)
		self.printer.setOutputFileName(self.verzeichnis_original + os.sep + "print.pdf")
		
		zu_lesen = "select cd, partnerw, partnerm, anzahl_bilder, anzahl_spalten from pordb_vid_neu"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		self.spinBoxAktuell.setValue(res[0][0])
		self.lineEditAnzahlM.setText(str(res[0][2]))
		self.lineEditAnzahlW.setText(str(res[0][1]))
		
		self.spinBoxZeilen = QtGui.QSpinBox()
		self.spinBoxZeilen.setRange(1, 99)
		try:
			self.spinBoxZeilen.setValue(res[0][3])
		except:
			self.spinBoxZeilen.setValue(12)
		self.spinBoxZeilen.setToolTip(self.trUtf8("Images per page"))
		self.toolBar.insertWidget(self.actionAnzahlBilder, self.spinBoxZeilen)
		self.connect(self.spinBoxZeilen, QtCore.SIGNAL("valueChanged(int)"), self.onAnzahlZeilen)
		
		self.spinBoxSpalten = QtGui.QSpinBox()
		self.spinBoxSpalten.setRange(1, 10)
		try:
			self.spinBoxSpalten.setValue(res[0][4])
		except:
			self.spinBoxSpalten.setValue(3)
		self.spinBoxSpalten.setToolTip(self.trUtf8("Columns"))
		self.toolBar.insertWidget(self.actionAnzahlBilder, self.spinBoxSpalten)
		self.connect(self.spinBoxSpalten, QtCore.SIGNAL("valueChanged(int)"), self.onAnzahlSpalten)
		
		self.anzahl_bilder = self.spinBoxZeilen.value()
		self.onAnzahlZeilen()
		self.onAnzahlSpalten()
		
		if initial_run:
			splash.showMessage("Getting search items", color = QtGui.QColor("red"))
			app.processEvents()
		self.suchbegriffe_lesen()
		
		def feldnamen_vergleich(a, b):
			if a[4] < b[4]:
				return -1
			else:
				return 1
		
		zu_lesen = "select * from information_schema.columns where table_name = 'pordb_vid'"
		lese_func = DBLesen(self, zu_lesen)
		felder = DBLesen.get_data(lese_func)
		felder.sort(feldnamen_vergleich)
		self.fieldnames_vid = []
		for i in felder:
			x = i[3]
			self.fieldnames_vid.append(x.title())
			
		zu_lesen = "select * from information_schema.columns where table_name = 'pordb_mpg_katalog'"
		lese_func = DBLesen(self, zu_lesen)
		felder = DBLesen.get_data(lese_func)
		felder.sort(feldnamen_vergleich)
		self.fieldnames_mpg = []
		for i in felder:
			x = i[3]
			self.fieldnames_mpg.append(x.title())
		self.fieldnames_mpg.append("MB")
		self.cumshots = {"f":"Facial", "h":"Handjob", "t":str(self.trUtf8("Tits")), "c":"Creampie", "x":"Analcreampie", "o":"Oralcreampie", "v":str(self.trUtf8("Cunt")), "b":str(self.trUtf8("Belly")), "a":str(self.trUtf8("Ass")), "s":str(self.trUtf8("Others"))}
		self.cumshots_reverse = {"Facial":"f", "Handjob":"h", str(self.trUtf8("Tits")):"t", "Creampie":"c", "Analcreampie":"x", "Oralcreampie":"o", str(self.trUtf8("Cunt")):"v", str(self.trUtf8("Belly")):"b", str(self.trUtf8("Ass")):"a", str(self.trUtf8("Others")):"s"}
		
		if initial_run:
			splash.showMessage("Getting device names", color = QtGui.QColor("red"))
			app.processEvents()
		self.device_fuellen()
		
		if initial_run: 
			splash.showMessage("Loading IAFD", color = QtGui.QColor("red"))
			app.processEvents()
			while True: # scheint nicht zu funktionieren
				try:
					seite = urllib2.urlopen("http://www.iafd.com/").read()
					if seite:
						self.webView.load(QtCore.QUrl("http://www.iafd.com/"))
						break
					else:
						pass
				except:
				    pass
			self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
				
		if initial_run:
			splash.showMessage("Ready", color = QtGui.QColor("green"))
			app.processEvents()
			splash.finish(self)
			initial_run = False
			
		self.suchfeld.setCurrentIndex(-1)
		
	def closeEvent(self, event):
		settings = QtCore.QSettings()
		settings.setValue("MeinDialog/Size", QtCore.QVariant(self.size()))
		settings.setValue("MeinDialog/Position", QtCore.QVariant(self.pos()))
		settings.setValue("MeinDialog/State", QtCore.QVariant(self.saveState()))
		settings.setValue("splitter", QtCore.QVariant(self.splitter.saveState()))
		
	def bilder_aktuell(self):
		self.label_akt_verzeichnis.setText(self.verzeichnis)
		dateiliste = os.listdir(self.verzeichnis)
		zeile = -1
		dateiliste_bereinigt = dateiliste[:]
		for i in dateiliste:
			zeile += 1
			if os.path.splitext(i)[-1].lower() == ".jpg" or os.path.splitext(i)[-1].lower() == ".jpeg" or os.path.splitext(i)[-1].lower() == ".png":
				pass
			else:
				del dateiliste_bereinigt[zeile]
				zeile -= 1
		self.tableWidgetBilderAktuell.setRowCount(len(dateiliste_bereinigt))
		zeile = -2
		dateiliste_bereinigt.sort()
		if self.bilderliste != dateiliste_bereinigt:
			for i in dateiliste_bereinigt:
				bild = QtGui.QPixmap(self.verzeichnis +os.sep +i).scaled(size, QtCore.Qt.KeepAspectRatio)
				bild = QtGui.QIcon(bild)
				newitem = QtGui.QTableWidgetItem(bild, i)
				zeile += 1
				self.tableWidgetBilderAktuell.setItem(zeile, 1, newitem)
			self.tableWidgetBilderAktuell.resizeColumnsToContents()
			self.tableWidgetBilderAktuell.resizeRowsToContents()
			self.tableWidgetBilderAktuell.scrollToTop()
			self.bilderliste = dateiliste_bereinigt[:]
		if not self.updatetimer.isActive():
			if len(dateiliste_bereinigt) > 10000:
				self.updatefrequenz = 10000000
			elif len(dateiliste_bereinigt) > 1000:
				self.updatefrequenz = 1000000
			elif len(dateiliste_bereinigt) > 100:
				self.updatefrequenz = 100000
			elif len(dateiliste_bereinigt) > 10:
				self.updatefrequenz = 10000
			else:
				self.updatefrequenz = 1000
			self.updatetimer.start(self.updatefrequenz)
		#print "Anzahl Bilder:", len(dateiliste_bereinigt), str(time.localtime()[3]) +":" +str(time.localtime()[4]) +":" +str(time.localtime()[5])
	# end of bilder_aktuell
	
	def onTimerStop(self, zeile, spalte):
		self.updatetimer.stop()
	
	def suchbegriffe_lesen(self):
		zu_lesen = "select * from pordb_suchbegriffe"
		lese_func = DBLesen(self, zu_lesen)
		self.suchbegriffe = dict(DBLesen.get_data(lese_func))
		self.suchbegriffe_rekursiv = {}
		for i in self.suchbegriffe:
			self.suchbegriffe_rekursiv[self.suchbegriffe[i]] = i.strip()
		self.suchbegriffe.update(self.suchbegriffe_rekursiv)

	def nation_fuellen(self):
		# Combobox für Nation füllen
		zu_lesen = "select * from pordb_iso_land where aktiv = 'x' order by land"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		self.nationen = []
		self.comboBoxNation.clear()
		for i in res:
			text = '%2s %-50s' % (i[0], i[1])
			self.comboBoxNation.addItem(text)
			self.nationen.append(i[0])
			
	def keyPressEvent(self, event):
		if event.modifiers() & QtCore.Qt.MetaModifier:
			if event.key() == QtCore.Qt.Key_F1:
				self.tabWidget.setCurrentIndex(0)
				self.suchfeld.setFocus()
			elif event.key() == QtCore.Qt.Key_F2:
				self.tabWidget.setCurrentIndex(1)
				self.suchfeld.setFocus()
			elif event.key() == QtCore.Qt.Key_F3:
				self.tabWidget.setCurrentIndex(2)
				self.suchfeld.setFocus()
			elif event.key() == QtCore.Qt.Key_F4:
				self.tabWidget.setCurrentIndex(3)
				self.suchfeld.setFocus()
			elif event.key() == QtCore.Qt.Key_F5:
				self.tabWidget.setCurrentIndex(4)
				self.suchfeld.setFocus()
			elif event.key() == QtCore.Qt.Key_F6:
				self.tabWidget.setCurrentIndex(5)
				self.suchfeld.setFocus()
		elif event.key() == QtCore.Qt.Key_F2:
			self.changeTab("F2")
		elif event.key() == QtCore.Qt.Key_F3:
			self.changeTab("F3")
		elif event.key() == QtCore.Qt.Key_F5:
			if len(self.tableWidgetBilderAktuell.selectedItems()) == 2:
				items = self.tableWidgetBilderAktuell.selectedItems()
				dateien = []
				for i in items:
					dateien.append(str(self.verzeichnis +os.sep +i.text()))
				self.onCover(dateien)
			elif len(self.tableWidgetBilderAktuell.selectedItems()) == 1:
				items = self.tableWidgetBilderAktuell.selectedItems()
				dateien = []
				for i in items:
					dateien.append(str(self.verzeichnis +os.sep +i.text()))
				self.onNeueingabe(dateien=dateien)
			else:
				self.onNeueingabe()
			self.bilder_aktuell()
		elif event.key() == QtCore.Qt.Key_Escape:
			self.suchfeld.setCurrentIndex(-1)
			self.suchfeld.setFocus()
		elif event.key() == QtCore.Qt.Key_PageUp:
			self.onPageUp()
		elif event.key() == QtCore.Qt.Key_PageDown:
			self.onPageDown()
		elif event.key() == (QtCore.Qt.Key_Enter or QtCore.Qt.Key_Return) and self.tabWidget.currentIndex() == 3:
			self.GetWebsite()
		elif event.key() == QtCore.Qt.Key_Z and self.tabWidget.currentIndex() == 3:
			self.webView.back()
		elif event.key() == QtCore.Qt.Key_X and self.tabWidget.currentIndex() == 3:
			self.webView.forward()
		elif event.key() == QtCore.Qt.Key_S and self.tabWidget.currentIndex() == 3:
			self.webView.stop()
		elif event.key() == QtCore.Qt.Key_C and self.tabWidget.currentIndex() == 3:
			self.onCopyintoClipboard()
		elif event.modifiers() & QtCore.Qt.ControlModifier:
			if event.key() == QtCore.Qt.Key_B:
				self.tabWidget.setCurrentIndex(1)
				self.onbildAnzeige()
				
	def onPageFirst(self):
		self.start_bilder = 0
		if self.aktuelle_ausgabe == "Darsteller":
			self.ausgabedarsteller()
		else:
			self.ausgabe_in_table()
	
	def onPageUp(self):
		self.start_bilder = self.start_bilder - self.anzahl_bilder
		if self.start_bilder > -1:
			if self.aktuelle_ausgabe == "Darsteller":
				self.ausgabedarsteller()
			else:
				self.ausgabe_in_table()
		else:
			self.start_bilder = 0
			if self.aktuelle_ausgabe == "Darsteller":
				self.ausgabedarsteller()
			else:
				self.ausgabe_in_table()
			
	def onPageDown(self):
		self.start_bilder = self.start_bilder + self.anzahl_bilder
		if self.start_bilder < len(self.aktuelles_res):
			if self.aktuelle_ausgabe == "Darsteller":
				self.ausgabedarsteller()
			else:
				self.ausgabe_in_table()
		else:
			self.start_bilder = len(self.aktuelles_res)
			
	def onPageLast(self):
		self.start_bilder = int(len(self.aktuelles_res) / self.anzahl_bilder) * self.anzahl_bilder
		if self.start_bilder == len(self.aktuelles_res):
			self.start_bilder = self.start_bilder - self.anzahl_bilder
		if self.start_bilder > -1:
			if self.aktuelle_ausgabe == "Darsteller":
				self.ausgabedarsteller()
			else:
				self.ausgabe_in_table()
		else:
			self.start_bilder = 0
			if self.aktuelle_ausgabe == "Darsteller":
				self.ausgabedarsteller()
			else:
				self.ausgabe_in_table()
	
	def onNeuDoubleClick(self):
		items = self.tableWidgetBilderAktuell.selectedItems()
		dateien = []
		for i in items:
			dateien.append(str(self.verzeichnis +os.sep +i.text()))
		self.onNeueingabe(dateien=dateien)
		self.bilder_aktuell()
				
	def onAnzahlZeilen(self):
		if self.columns == float(self.spinBoxZeilen.value()):
			return
		zu_erfassen = "update pordb_vid_neu set anzahl_bilder = '" +str(int(self.spinBoxZeilen.value())) +"'"
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		self.rows = float(self.spinBoxZeilen.value())
		self.tableWidgetBilder.setRowCount(self.rows)
		self.anzahl_bilder = self.rows
		if self.aktuelle_ausgabe == "Darsteller" or not self.letzter_select_komplett:
			self.ausgabedarsteller()
		else:
			if len(self.aktuelles_res) > 0:
				self.ausgabe(self.letzter_select_komplett, self.letzter_select_komplett)
	
	def onAnzahlSpalten(self):
		if self.columns == float(self.spinBoxSpalten.value()):
			return
		zu_erfassen = "update pordb_vid_neu set anzahl_spalten = '" +str(int(self.spinBoxSpalten.value())) +"'"
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		self.columns = float(self.spinBoxSpalten.value())
		self.tableWidgetBilder.setColumnCount(self.columns)
		if self.aktuelle_ausgabe == "Darsteller" or not self.letzter_select_komplett:
			self.ausgabedarsteller()
		else:
			if len(self.aktuelles_res) > 0:
				self.ausgabe(self.letzter_select_komplett, self.letzter_select_komplett)
				
	def onDirectoryChange(self):
		datei = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8(u"Select directory"), self.verzeichnis)
		if datei:
			self.verzeichnis = str(datei)
			app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.bilder_aktuell()
			app.restoreOverrideCursor()
			
	def onHistorie(self):
		historiedialog = Historie()
		historiedialog.exec_()
		zu_lesen = historiedialog.zu_lesen
		if zu_lesen and not "pordb_history" in zu_lesen:
			self.start_bilder = 0
			self.ausgabe(zu_lesen, zu_lesen)
		else:
			self.suchfeld.setFocus()
			
	def onVidNeuAktualisieren(self):
		zu_erfassen = "UPDATE pordb_vid_neu SET cd = " +str(self.spinBoxAktuell.value())
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
			
	def changeTab(self, taste):
		if taste == "F3":
			neuer_tab = self.tabWidget.currentIndex() + 1
			if neuer_tab == 6:
				neuer_tab = 0
			self.tabWidget.setCurrentIndex(neuer_tab)
			self.suchfeld.setFocus()
		elif taste == "F2":
			neuer_tab = self.tabWidget.currentIndex() - 1
			if neuer_tab == -1:
				neuer_tab = 5
			self.tabWidget.setCurrentIndex(neuer_tab)
			self.suchfeld.setFocus()
			
	def onContextDarsteller(self, event):
		menu = QtGui.QMenu(self.listWidgetDarsteller)
		menu.addAction(self.actionAnzeigenPaar)
		menu.addAction(self.actionBildanzeigegross)
		menu.exec_(self.listWidgetDarsteller.mapToGlobal(event))
			
	def onContextCS(self, event):
		menu = QtGui.QMenu(self.listWidgetStatistik)
		menu.addAction(self.actionCSZeigen)
		menu.exec_(self.listWidgetStatistik.mapToGlobal(event))
		
	def onContextFilm(self, event):
		menu = QtGui.QMenu(self.listWidgetFilme)
		menu.addAction(self.actionFilm_zeigen)
		menu.exec_(self.listWidgetFilme.mapToGlobal(event))
		
	def onContexttableWidgetBilder(self, event):
		menu = QtGui.QMenu(self.tableWidgetBilder)
		if self.aktuelle_ausgabe == "Darsteller":
			menu.addAction(self.actionDarstellerUebernehmen)
			menu.addAction(self.actionBildanzeigegross)
		else:
			menu.addAction(self.actionAnzeigenOriginal)
			menu.addAction(self.actionSortieren_nach_Darsteller)
			menu.addAction(self.actionSortieren_nach_CD)
			menu.addAction(self.actionSortieren_nach_Original)
			menu.addAction(self.actionSortieren_nach_Titel)
			menu.addAction(self.actionOriginal_umbenennen)
			menu.addAction(self.actionOriginal_weitere)
			item = self.tableWidgetBilder.currentItem()
			if item:
				text = unicode(item.text()).encode("utf-8")
				if "Cover (" in text:
					menu.addAction(self.actionCovergross)
			menu.addAction(self.actionOriginalIntoClipboard)
		menu.exec_(self.tableWidgetBilder.mapToGlobal(event))
			
	def onContexttableWidgetBilderAktuell(self, event):
		if len(self.bilderliste) > 0:
			menu = QtGui.QMenu(self.tableWidgetBilderAktuell)
			menu.addAction(self.actionBildLoeschen)
			menu.exec_(self.tableWidgetBilderAktuell.mapToGlobal(event))
		
	def onDarstellerUebernehmen(self):
		item = self.tableWidgetBilder.currentItem()
		text = str(item.text()).split("\n")
		if text:
			self.suchfeld.insertItem(0, "=" + text[0].strip())
			self.suchfeld.setCurrentIndex(0)
	
	def onBildgross(self, event):
		menu = QtGui.QMenu(self.labelBildanzeige)
		menu.addAction(self.actionBildanzeigegross)
		menu.exec_(self.labelBildanzeige.mapToGlobal(event))
		
	def onAnzeigenPaar(self):
		ein = self.eingabe_auswerten().lstrip("=")
		if not ein:
			return
		name = str(self.labelDarsteller.text()).strip().lstrip("=")
		if ein <> name:
			if self.comboBoxGeschlecht.currentText() == 'w':
				suchtext = name + ", %" + ein
			else:
				suchtext = ein + ", %" + name
			self.suchfeld.insertItem(0, suchtext)
			self.suchfeld.setCurrentIndex(0)
			self.tabWidget.setCurrentIndex(0)
			self.onDarsteller()
			self.listWidgetDarsteller.clearSelection()
		
	def onFilm_zeigen(self):
		selected = self.listWidgetFilme.selectedItems()
		if selected:
			original = unicode(selected[0].text()).strip().rstrip(" Wmv")
			if original[-1] == ")":
				original = original[0:len(original)-7]
			self.suchfeld.insertItem(0, original)
			self.suchfeld.setCurrentIndex(0)
			self.tabWidget.setCurrentIndex(0)
			self.onOriginal()
			self.listWidgetFilme.clearSelection()
		
	def onCSZeigen(self):
		selected = self.listWidgetStatistik.selectedItems()
		if selected:
			cs = str(selected[0].text()).strip()
			cs_found = None
			for i in self.cumshots.values():
				if i in cs:
					cs_found = self.cumshots_reverse.get(i)
			if cs_found:
				ein = str(self.labelDarsteller.text()).strip().title()
				self.start_bilder = 0
				app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
				eingabe = ein.title().replace("'", "''")
				zu_lesen = "SELECT * FROM pordb_vid where (darsteller = '" +eingabe +"' or darsteller like '" +eingabe +",%' or darsteller like '%, " +eingabe +",%' or darsteller like '%, " +eingabe +"')"
				zu_lesen += " and cs" +cs_found +" <> 0" 
				self.letzter_select = zu_lesen
				zu_lesen += " order by cd, bild, darsteller"
				self.ausgabe(ein, zu_lesen)
				app.restoreOverrideCursor()
		
	def onAnzeigenOriginal(self):
		item = self.tableWidgetBilder.currentItem()
		column = self.tableWidgetBilder.column(item)
		row = self.tableWidgetBilder.row(item)
		index = int(row * self.columns + column + self.start_bilder)
		if self.aktuelles_res[index][5]:
			original = self.aktuelles_res[index][5].decode("utf-8")
		else:
			original = ""
		if original and original != "Wmv":
			if original[-1] == ")":
				original = original[0:len(original)-7]
			self.suchfeld.insertItem(0, original)
			self.suchfeld.setCurrentIndex(0)
			self.onOriginal()
			
	def onSortieren_nach_Darsteller(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = self.letzter_select + " order by darsteller, cd, bild"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(zu_lesen, zu_lesen)
		app.restoreOverrideCursor()
		
	def onSortieren_nach_CD(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = self.letzter_select + " order by cd, darsteller, bild"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(zu_lesen, zu_lesen)
		app.restoreOverrideCursor()
		
	def onSortieren_nach_Original(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = self.letzter_select + " order by original, cd, darsteller, bild"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(zu_lesen, zu_lesen)
		app.restoreOverrideCursor()
		
	def onSortieren_nach_Titel(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = self.letzter_select + " order by titel, cd, darsteller, bild"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(zu_lesen, zu_lesen)
		app.restoreOverrideCursor()
		
	def onOriginal_umbenennen(self):
		item = self.tableWidgetBilder.currentItem()
		column = self.tableWidgetBilder.column(item)
		row = self.tableWidgetBilder.row(item)
		index = int(row * self.columns + column + self.start_bilder)
		if self.aktuelles_res[index][5]:
			original = self.aktuelles_res[index][5].decode("utf-8")
		else:
			original = ""
		if not original:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("There is no original title: cannot be renamed"))
			app.restoreOverrideCursor()
			return
		umbenennen = DarstellerUmbenennen(original)
		if umbenennen.exec_():
			neuer_name = unicode(umbenennen.lineEditNeuerName.text())
			if neuer_name:
				app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
				zu_erfassen = "update pordb_vid set original = '" +neuer_name.title().replace("'", "''") +"' where original = '" +original.replace("'", "''") +"'"
				update_func = DBUpdate(self, zu_erfassen)
				DBUpdate.update_data(update_func)
				zu_lesen = "select * from pordb_vid where original = '" +unicode(neuer_name).title().encode("utf-8").replace("'", "''") +"' order by original, cd, bild, darsteller"
				self.letzter_select_komplett = zu_lesen
				self.start_bilder = 0
				self.ausgabe(zu_lesen, zu_lesen)
				app.restoreOverrideCursor()
				
		self.suchfeld.setFocus()
		
	def onOriginal_weitere(self):
		item = self.tableWidgetBilder.currentItem()
		column = self.tableWidgetBilder.column(item)
		row = self.tableWidgetBilder.row(item)
		index = int(row * self.columns + column + self.start_bilder)
		if self.aktuelles_res[index][5]:
			original = self.aktuelles_res[index][5].decode("utf-8")
		else:
			original = ""
		if not original:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Movie has no original title"))
			app.restoreOverrideCursor()
			return
		zu_lesen = "select primkey from pordb_vid where original = '" +unicode(original).encode("utf-8").replace("'", "''") +"'"
		lese_func = DBLesen(self, zu_lesen)
		res_primkey = DBLesen.get_data(lese_func)
		for i in res_primkey:
			zu_lesen = "select original from pordb_original where foreign_key_pordb_vid = " +str(i[0])
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			if res:
				break
		original_vorhanden = []
		for i in res:
			original_vorhanden.append(i[0])
		if res:
			originaldialog = OriginalErfassen(original_vorhanden)
		else:
			originaldialog = OriginalErfassen()
		originaldialog.exec_()
		original_weitere = []
		try:
			original_weitere = originaldialog.original
		except:
			pass
		
		if original_weitere:
			zu_erfassen = []
			for i in res_primkey:
				zu_erfassen.append("delete from pordb_original where foreign_key_pordb_vid = " +str(i[0]))
			
				for j in original_weitere:
					if j:
						zu_erfassen.append("insert into pordb_original (original, foreign_key_pordb_vid) values ('" +j.decode('utf-8').title().replace("'", "''") +"', " +str(i[0]) +")")
						
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
						
		self.suchfeld.setFocus()
		
	def onOriginalIntoClipboard(self):
		item = self.tableWidgetBilder.currentItem()
		column = self.tableWidgetBilder.column(item)
		row = self.tableWidgetBilder.row(item)
		index = int(row * self.columns + column + self.start_bilder)
		if self.aktuelles_res[index][5]:
			original = self.aktuelles_res[index][5].decode("utf-8")
		else:
			original = ""
		if item:
			zu_erfassen = "UPDATE pordb_vid_neu SET original = '" +original.replace("'", "''") +"'"
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
			self.statusBar.showMessage('"' +original +'"' +self.trUtf8(" transferred into clipboard"))
		self.suchfeld.setFocus()
		
	def onCovergross(self):
		item = self.tableWidgetBilder.currentItem()
		column = self.tableWidgetBilder.column(item)
		row = self.tableWidgetBilder.row(item)
		index = int(row * self.columns + column + self.start_bilder)
		if self.aktuelles_res[index][5]:
			original = self.aktuelles_res[index][5].decode("utf-8")
		else:
			original = ""
		cover = self.verzeichnis_cover + os.sep + self.aktuelles_res[index][3].strip()
		if os.path.exists(cover):
			bilddialog = DarstellerAnzeigeGross(cover)
			bilddialog.exec_()
		self.suchfeld.setFocus()
		
	def onBildLoeschen(self):
		item = self.tableWidgetBilderAktuell.currentItem()
		text = str(item.text())
		bilddatei = self.verzeichnis +os.sep +text 
		try:
			os.remove(bilddatei)
		except:
			pass
		self.bilder_aktuell()
		self.suchfeld.setFocus()
		
	def onCover(self, datei = None):
		cover = []
		j = 0
		if not datei:
			dateiliste = os.listdir(self.verzeichnis_original)
			for i in dateiliste:
				if os.path.splitext(i)[-1].lower() == ".jpg" or os.path.splitext(i)[-1].lower() == ".jpeg" or os.path.splitext(i)[-1].lower() == ".png":
					cover.append(os.path.join(self.verzeichnis_original, i))
					j += 1
					if j == 2:    # es werden nur 2 Bilddateien akzeptiert
						break
		else:
			cover = datei
		if cover:
			dialog = Cover(cover, self.verzeichnis_original)
			dialog.exec_()
			self.onNeueingabe(cover_anlegen = 1)
		self.suchfeld.setFocus()
		
	def onDrucken(self):
		def paint_action():
			painter = QtGui.QPainter(self.printer)
			x = 30
			y = 0
			seite = 1
			if self.tabWidget.currentIndex() == 0:
				lese_func = DBLesen(self, self.letzter_select_komplett)
				res = DBLesen.get_data(lese_func)
				if self.actionCheckBoxDVDCover.isChecked():
					zw_res = []
					for i in res:
						dateiname = self.verzeichnis_cover +"/" +i[3].strip()
						if os.path.exists(dateiname):
							zw_res.append(i)
					res = zw_res
				painter.drawText(x + 300, y, "- " +str(seite) +" -")
				y += 15
				for i in res:
					if self.aktuelle_ausgabe == "Darsteller":
						sex = str(self.letzter_select_komplett)[str(self.letzter_select_komplett).find("sex") + 7]
						filename = self.verzeichnis_thumbs + os.sep + "darsteller_" + sex + os.sep + i[0].strip().lower().replace(" ", "_") + ".jpg"
					else:
						filename = self.verzeichnis_thumbs + os.sep + "cd" +str(i[2]) +os.sep +i[3].strip()
						if not os.path.exists(filename):
							filename = self.verzeichnis_cover +os.sep +i[3].strip()
					bild = QtGui.QPixmap(filename)
					if bild.height() > self.printer.pageRect().height() - 60 or bild.width() > self.printer.pageRect().width() - 60:
						bild = QtGui.QPixmap(bild).scaled(self.printer.pageRect().width() - 60, self.printer.pageRect().height() - 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
					if bild.width() > 270:
						randunten = 220
					else:
						randunten = 50
					if y + bild.height() + randunten > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
					painter.drawPixmap(x, y, bild)
					y += 12 + bild.height()
					if self.aktuelle_ausgabe == "Darsteller":
						painter.drawText(x, y, i[0])
						y += 15
						painter.drawText(x, y, self.trUtf8("Anzahl: ") +str(i[2]))
						y += 15
						if i[5]:
							painter.drawText(x, y, "Nation: " +i[5])
						else:
							painter.drawText(x, y, "Nation: n.a." )
						y += 15
						if i[6]:
							painter.drawText(x, y, "Tattoo: " +i[6])
						else:
							painter.drawText(x, y, "Tattoo: -" )
						y += 15
						painter.drawText(x, y, "Partner: " +str(i[8]))
					else:
						painter.drawText(x, y, self.trUtf8("Title: ") +i[0])
						y += 15
						painter.drawText(x, y, self.trUtf8("Actor: ") +i[1])
						y += 15
						painter.drawText(x, y, "CD: " +str(i[2]))
						y += 15
						painter.drawText(x, y, self.trUtf8("Image: ") +i[3])
						y += 15
						painter.drawText(x, y, self.trUtf8("only image: ") +i[4])
						y += 15
						if i[5]:
							painter.drawText(x, y, "Original: " +i[5].decode("utf-8"))
						else:
							painter.drawText(x, y, "Original: ")
						y += 15
						if i[6]:
							painter.drawText(x, y, "CS: " +i[6])
						else:
							painter.drawText(x, y, "CS: ")
						y += 15
						if i[7]:
							painter.drawText(x, y, self.trUtf8("available: ") +i[7])
						else:
							painter.drawText(x, y, self.trUtf8("available: "))
					y += 20
					painter.drawLine(x, y, x + 600, y)
					y += 20
				painter.end()
			elif self.tabWidget.currentIndex() == 1:
				name = str(self.labelDarsteller.text()).strip().lstrip("=")
				if name:
					painter.drawText(x + 300, y, "- " +str(seite) +" -")
					y += 15
					painter.drawText(x, y, name)
					y += 15
					filename = self.verzeichnis_thumbs + os.sep + "darsteller_w" + os.sep + name.strip().lower().replace(" ", "_") + ".jpg"
					if not os.path.exists(filename):
						filename = self.verzeichnis_thumbs + os.sep + "darsteller_m" + os.sep + name.strip().lower().replace(" ", "_") + ".jpg"
					bild = QtGui.QPixmap(filename)
					if bild.height() > self.printer.pageRect().height() - 60 or bild.width() > self.printer.pageRect().width() - 60:
						bild = QtGui.QPixmap(bild).scaled(self.printer.pageRect().width() - 60, self.printer.pageRect().height() - 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
					painter.drawPixmap(x, y, bild)
					y += 15 + bild.height()
					if y > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
					painter.drawLine(x, y, x + 600, y)
					y += 15
					if y + 15 > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
						
					painter.drawText(x, y, self.trUtf8("Statistics"))
					y += 10
					painter.drawLine(x, y, x + 60, y)
					for i in xrange(self.listWidgetStatistik.count()):
						y += 15
						if y > self.printer.pageRect().height():
							y = 0
							self.printer.newPage()
							seite += 1
							painter.drawText(x + 300, y, "- " +str(seite) +" -")
							y += 15
						texte = str(self.listWidgetStatistik.item(i).text()).split()
						if len(texte) == 3:
						  painter.drawText(x, y, texte[0].strip())
						  x += 100
						  painter.drawText(x, y, texte[1].strip())
						  x += 30
						  painter.drawText(x, y, texte[2].strip())
						  x = 30
						else:
						  painter.drawText(x, y, str(self.listWidgetStatistik.item(i).text()).strip())
					y += 15
					if y > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
					painter.drawLine(x, y, x + 600, y)
					y += 15
					if y + 15 > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
						
					painter.drawText(x, y, "Partner (" +str(len(self.paarung)) +")")
					y += 10
					painter.drawLine(x, y, x + 60, y)
					for i in xrange(self.listWidgetDarsteller.count()):
						y += 15
						if y > self.printer.pageRect().height():
							y = 0
							self.printer.newPage()
							seite += 1
							painter.drawText(x + 300, y, "- " +str(seite) +" -")
							y += 15
						painter.drawText(x, y, str(self.listWidgetDarsteller.item(i).text()).strip())
					y += 15
					if y > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
					painter.drawLine(x, y, x + 600, y)
					y += 15
					if y + 15 > self.printer.pageRect().height():
						y = 0
						self.printer.newPage()
						seite += 1
						painter.drawText(x + 300, y, "- " +str(seite) +" -")
						y += 15
						
					painter.drawText(x, y, self.trUtf8("Movies (") +str(self.listWidgetFilme.count()) +")")
					y += 10
					painter.drawLine(x, y, x + 60, y)
					for i in xrange(self.listWidgetFilme.count()):
						y += 15
						if y > self.printer.pageRect().height():
							y = 0
							self.printer.newPage()
							seite += 1
							painter.drawText(x + 300, y, "- " +str(seite) +" -")
							y += 15
						painter.drawText(x, y, unicode(self.listWidgetFilme.item(i).text()).strip())
					painter.end()
			elif self.tabWidget.currentIndex() == 2:
				painter.drawText(x + 100, y, "- " +str(seite) +" -")
				y += 15
				painter.drawText(x, y, self.trUtf8("Search term: ") +self.lineEditSuchen.text())
				y += 15
				painter.drawText(x, y, "In mpg_katalog: " +"_" *90)
				y += 15
				columns = self.tableWidget.columnCount()
				rows = self.tableWidget.rowCount()
				for i in xrange(rows):
					for j in xrange(columns):
						y += 15
						if y > self.printer.pageRect().height():
							y = 0
							self.printer.newPage()
							seite += 1
							painter.drawText(x + 100, y, "- " +str(seite) +" -")
							y += 15
						try:
							text = self.tableWidget.item(i, j).text()
						except:
							text = " "
						painter.drawText(x, y, text)
						
				y += 15
				painter.drawText(x, y, "In vid: " +"_" *90)
				y += 15
						
				columns = self.tableWidget1.columnCount()
				rows = self.tableWidget1.rowCount()
				for i in xrange(rows):
					for j in xrange(columns):
						y += 15
						if y > self.printer.pageRect().height():
							y = 0
							self.printer.newPage()
							seite += 1
							painter.drawText(x + 100, y, "- " +str(seite) +" -")
							y += 15
						try:
							text = self.tableWidget1.item(i, j).text()
						except:
							pass
						painter.drawText(x, y, text)
						
				app.restoreOverrideCursor()
				self.suchfeld.setFocus()
				painter.end()
				return
			elif self.tabWidget.currentIndex() == 3:
				painter.end()
				self.webView.print_(self.printer)
			else:
				app.restoreOverrideCursor()
				self.suchfeld.setFocus()
				return
		# end of paint_action
		
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		
		self.preview = QtGui.QPrintPreviewDialog(self.printer)
		self.connect(self.preview, QtCore.SIGNAL("paintRequested (QPrinter *)"), paint_action)
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		if not self.preview.exec_():
			return
		
	def onDarstellerGross(self):
		if self.tabWidget.currentIndex() == 0:
			self.onDarstellerUebernehmen()
		ein = self.eingabe_auswerten().lstrip("=")
		
		self.listWidgetDarsteller.clearSelection()
		if ein:
			bildname = ein.lower().strip().replace(" ", "_").replace("'", "_apostroph_")
			self.bilddarsteller = self.verzeichnis_thumbs +"/darsteller_w/" +bildname +".jpg"
			if not os.path.isfile(self.bilddarsteller):
				self.bilddarsteller = self.verzeichnis_thumbs +"/darsteller_w/" +bildname +".png"
				if not os.path.isfile(self.bilddarsteller):
					self.bilddarsteller = self.verzeichnis_thumbs +"/darsteller_m/" +bildname +".jpg"
					if not os.path.isfile(self.bilddarsteller):
						self.bilddarsteller = self.verzeichnis_thumbs +"/darsteller_m/" +bildname +".png"
						if not os.path.isfile(self.bilddarsteller):
							self.bilddarsteller = self.verzeichnis_thumbs +"/nichtvorhanden/nicht_vorhanden.jpg"
		bilddialog = DarstellerAnzeigeGross(self.bilddarsteller)
		bilddialog.exec_()
		self.suchfeld.setFocus()
		
	def onLand(self):
		bilddialog = LandBearbeiten(self.comboBoxNation, self.nation_fuellen)
		bilddialog.exec_()
		self.suchfeld.setFocus()
		
	def onSuchbegriffe(self):
		bilddialog = SuchbegriffeBearbeiten()
		bilddialog.exec_()
		self.suchbegriffe_lesen()
		self.suchfeld.setFocus()
		
	def onSucheVideo(self):
		self.video_anzeigen([])
		
	def video_anzeigen(self, titel):
		suchendialog = SucheVideo(app, titel)
		suchendialog.exec_()
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = suchendialog.zu_lesen
		if zu_lesen:
			self.start_bilder = 0
			self.ausgabe(zu_lesen, zu_lesen)
		app.restoreOverrideCursor()
		
	def onDarsteller(self):
		# Darsteller in pordb_vid suchen und anzeigen
		self.start_bilder = 0
		ein = str(self.suchfeld.currentText()).strip().title()
		if not ein:
			return
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		vorname = False
		if ein.find('=') == 0:
			vorname = True
			eingabe = ein.lstrip('=').title().replace("'", "''")
		else:
			eingabe = ein.title().replace("'", "''")
		if vorname:
			zu_lesen = "SELECT * FROM pordb_vid where (darsteller = '" +eingabe +"' or darsteller like '" +eingabe +",%' or darsteller like '%, " +eingabe +",%' or darsteller like '%, " +eingabe +"')"
			
		else:
			zu_lesen = "SELECT * FROM pordb_vid where darsteller like '%" +eingabe +"%'"
		if self.actionVid.isChecked():
			zu_lesen += " and vorhanden = 'x'"
			self.actionVid.toggle()
		self.letzter_select = zu_lesen
		zu_lesen += " order by cd, bild, darsteller"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(ein, zu_lesen)
		app.restoreOverrideCursor()

	def onCD(self):
		# CD in pordb_vid suchen und anzeigen
		self.start_bilder = 0
		try:
			ein = int(self.suchfeld.currentText())
		except:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("CD is not a number"))
			return
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = "SELECT * FROM pordb_vid where cd = " +str(ein)
		if self.actionVid.isChecked():
			zu_lesen += " and vorhanden = 'x'"
			self.actionVid.toggle()
		self.letzter_select = zu_lesen
		zu_lesen += " order by bild, darsteller"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(str(ein), zu_lesen)
		app.restoreOverrideCursor()
			
	def onTitel(self):
		# nach Titel in pordb_vid suchen und anzeigen
		self.start_bilder = 0
		ein = str(self.suchfeld.currentText()).replace("'", "''").lower()
		if not ein:
			return
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = "SELECT * FROM pordb_vid where lower(titel) like '%" +ein.replace(" ", "%") +"%'"
		if self.actionVid.isChecked():
			zu_lesen += " and vorhanden = 'x'"
			self.actionVid.toggle()
		self.letzter_select = zu_lesen
		zu_lesen += " order by cd, bild, darsteller"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(ein, zu_lesen)
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
			
	def onOriginal(self):
		# nach Originaltitel in pordb_vid suchen und anzeigen
		self.start_bilder = 0
		try:
			ein = unicode(self.suchfeld.currentText()).replace("'", "''").lower().strip().encode("utf-8")
		except:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8(u"Seems to be an invalid character in the search field"))
			return
		if not ein:
			return
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = "select * from pordb_original where lower(original) like '%" +ein.replace(" ", "%") +"%'"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		ein_gesplittet = ein.split()
		if len(ein_gesplittet) > 1:
			try:
				nummer = int(ein_gesplittet[-1].replace("#",""))
				zu_lesen = "select * from pordb_vid where lower(original) like '"
				for i in xrange(len(ein_gesplittet) -1):
					zu_lesen += "%" +ein_gesplittet[i]
				zu_lesen  += " " +ein_gesplittet[-1] +"%'"
			except:
				zu_lesen = "select * from pordb_vid where lower(original) like '%" +ein.replace(" ", "%") +"%'"
		else:
			zu_lesen = "select * from pordb_vid where lower(original) like '%" +ein.replace(" ", "%") +"%'"
		original_erweiterung = ""
		for i in res:
			original_erweiterung += " or primkey = " +str(i[2])
		if original_erweiterung:
			zu_lesen += original_erweiterung
		if self.actionVid.isChecked():
			zu_lesen += " and vorhanden = 'x'"
			self.actionVid.toggle()
		self.letzter_select = zu_lesen
		zu_lesen += " order by original, cd, bild, darsteller"
		self.letzter_select_komplett = zu_lesen
		self.ausgabe(ein, zu_lesen)
		app.restoreOverrideCursor()
		
	def onHelp(self):
		QtGui.QMessageBox.about(self, "About PorDB", """<b>PorDB</b> v %s <p>Copyright &copy; 2011 HWM</p> <p>GNU GENERAL PUBLIC LICENSE Version 3</p> <p>This is PorDB.</p> <p>Python %s - Qt %s - PyQt %s on %s""" % (__version__, platform.python_version(), QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR, platform.system()))
		
	def ausgabe(self, ein, zu_lesen):
		def vergleich(a, b):
			try:
				original_a = a[5].strip()
			except:
				original_a = " "
			try:
				original_b = b[5].strip()
			except:
				original_b = " "
			if not original_a.strip() and not original_b.strip():
				return 0
			if original_a[len(original_a) - 4 : len(original_a)] == " Wmv":
				wmv_abzug_a = 4
			else:
				wmv_abzug_a = 0
			if original_b[len(original_b) - 4 : len(original_b)] == " Wmv":
				wmv_abzug_b = 4
			else:
				wmv_abzug_b = 0
			if original_a and original_a[len(original_a) - 1 - wmv_abzug_a] == ")":
				wmv_abzug_a += 7
			if original_b and original_b[len(original_b) - 1 - wmv_abzug_b] == ")":
				wmv_abzug_b += 7
			original_a_list = original_a[0:len(original_a) - wmv_abzug_a].split()
			original_b_list = original_b[0:len(original_b) - wmv_abzug_b].split()
			if len(original_a_list) == len(original_b_list):
				ungleich = 0
				for i in range (len(original_a_list) - 1):
					if original_a_list[i] != original_b_list[i]:
						ungleich = 1
				if not ungleich:
					try:
						nr_a = int(original_a_list[len(original_a_list) - 1])
						nr_b = int(original_b_list[len(original_b_list) - 1])
					except:
						return 0
					if nr_a < nr_b:
						return -1
					else:
						return 1
				else:
					return 0
			else:
				return 0
		# end of vergleich
				
		lese_func = DBLesen(self, zu_lesen)
		self.aktuelles_res = DBLesen.get_data(lese_func)
		zw_res = []
		if "select * from pordb_vid where lower(original) like" in zu_lesen:
			ende = zu_lesen.find("primkey")
			if ende < 0:
				ende = zu_lesen.find("nurbild") - 6 # damit das "and" nicht in der where-Bedingung durch "&" ersetzt wird
			for i in self.suchbegriffe:
				suchbegriff = i.lower().strip()
				if suchbegriff and suchbegriff in zu_lesen[0:ende]:
					if ende > 0:
						zu_lesen2 = zu_lesen[0:ende - 3]
					else:
						zu_lesen2 = zu_lesen
					if suchbegriff == "-":
						zu_lesen2.replace(suchbegriff, " ")
					else:
						zu_lesen2 = zu_lesen2.replace(suchbegriff, self.suchbegriffe[i].lower().strip())
					if zu_lesen <> zu_lesen2:
						lese_func = DBLesen(self, zu_lesen2)
						res2 = DBLesen.get_data(lese_func)
						if res2:
							self.aktuelles_res.extend(res2)
			if self.actionCheckBoxDVDCover.isChecked():
				for i in self.aktuelles_res:
					dateiname = self.verzeichnis_cover +"/" +i[3].strip()
					if os.path.exists(dateiname):
						zw_res.append(i)
				self.aktuelles_res = zw_res
		if "order by original" in zu_lesen:
			self.aktuelles_res.sort(vergleich)
			
		# Delete duplicates which are created through table suchbegriffe
		liste_neu = []
		for i in self.aktuelles_res:
			if not i in liste_neu:
				liste_neu.append(i)
		self.aktuelles_res[:] = liste_neu
		
		self.ausgabe_in_table()
		befehl = zu_lesen.replace("'", '"')
		if len(befehl) < 5001:
			zu_erfassen = "INSERT into pordb_history values ('" +str(befehl).decode('utf-8') +"', DEFAULT)"
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
		self.statusBar.showMessage(self.trUtf8("Search was: ") +ein)
		if str(ein).lower().startswith("select "):
			pass
		else:
			self.suchhistorie(ein)
		self.suchfeld.setCurrentIndex(-1)
		self.tabWidget.setCurrentIndex(0)
		self.suchfeld.setFocus()
	# end of ausgabe
	
	def ausgabe_in_table(self):
		self.tableWidgetBilder.clear()
		zeile = 0
		spalte = -1
		res = self.aktuelles_res[int(self.start_bilder):int(self.start_bilder) + int(self.anzahl_bilder)]
		self.tableWidgetBilder.setRowCount(round(len(res) / self.columns + 0.4))
		if len(res) < self.columns:
			self.tableWidgetBilder.setColumnCount(len(res))
		else:
			self.tableWidgetBilder.setColumnCount(self.columns)
		for i in res:
			cover = ""
			dateiname = self.verzeichnis_thumbs +"/cd" +str(i[2]) +"/" +i[3].strip()
			if not os.path.exists(dateiname) or self.actionCheckBoxDVDCover.isChecked():
				dateiname = self.verzeichnis_cover +"/" +i[3].strip()
				if os.path.exists(dateiname):
					cover = "x"
			if os.path.exists(dateiname):
				bild = QtGui.QPixmap(dateiname)
				groesse = bild.size()
				bild = QtGui.QIcon(dateiname)
			else:
				bild = QtGui.QPixmap(self.verzeichnis_thumbs +"/nichtvorhanden/nicht_vorhanden.jpg")
				groesse = bild.size()
				bild = QtGui.QIcon(self.verzeichnis_thumbs +"/nichtvorhanden/nicht_vorhanden.jpg")
			cs = ""
			if i[9] != 0:
				cs += str(i[9]) +"f"
			if i[10] != 0:
				cs += str(i[10]) +"h"
			if i[11] != 0:
				cs += str(i[11]) +"t"
			if i[12] != 0:
				cs += str(i[12]) +"c"
			if i[13] != 0:
				cs += str(i[13]) +"x"
			if i[14] != 0:
				cs += str(i[14]) +"o"
			if i[15] != 0:
				cs += str(i[15]) +"v"
			if i[16] != 0:
				cs += str(i[16]) +"b"
			if i[17] != 0:
				cs += str(i[17]) +"a"
			if i[18] != 0:
				cs += str(i[18]) +"s"
			if i[19] != 0:
				cs += str(i[19]) +"k"
			ort = str(i[2]) +" " +cs
			if i[5] == None:
				original = ""
			else:
				original = i[5].decode("utf-8")
			text = ""
			if cover:
				text = "Cover (" +str(groesse.width()) +", " +str(groesse.height()) +")\n" 
			text += "------------------------------\n"
			darsteller = i[1].split(", ")
			geschlecht_alt = ""
			darsteller_ausgabe = ""
			for j in darsteller:
				if j:
					zu_lesen = "select sex from pordb_darsteller where darsteller = '" +j.replace("'", "''")  +"'"
					lese_func = DBLesen(self, zu_lesen)
					res = DBLesen.get_data(lese_func)
					if res:
						if geschlecht_alt != res[0][0]:
							if geschlecht_alt == "":
								darsteller_ausgabe += j
							else:
								darsteller_ausgabe += "\n--\n" + j 
							geschlecht_alt = res[0][0]
						else:
							darsteller_ausgabe += "\n" +j
			if len(original) > 30:
				original_liste = original.split()
				original = ""
				multiplikator = 1
			else:
				original_liste = []
			k = 0
			for j in original_liste:
				k += 1
				original += j +" "
				if len(original.strip()) > multiplikator * 30 and len(original_liste) > k:
					original = original.strip() + "\n"
					multiplikator += 1
			if original:
				text += original +"\n------------------------------\n"
			if darsteller_ausgabe:
				text += darsteller_ausgabe +"\n------------------------------\n" 
			text += "CD=" +ort +" "
			if i[4] != 'x':
				text += self.trUtf8("\nwatched")
			elif i[7] == 'x':
				text += self.trUtf8("\npresent")
			zu_lesen = "select * from pordb_original where foreign_key_pordb_vid = " +str(i[8])
			lese_func = DBLesen(self, zu_lesen)
			res2 = DBLesen.get_data(lese_func)
			if len(res2) > 0:
				text += "\n>>>>>"
			newitem = QtGui.QTableWidgetItem(bild, text)
			if i[4] == 'x' and i[7] != 'x':
				newitem.setTextColor(QtGui.QColor("red"))
			spalte += 1
			if spalte == self.columns:
				spalte = 0
				zeile += 1
			self.tableWidgetBilder.setItem(zeile, spalte, newitem)
		self.restarbeiten_bilder()
		self.aktuelle_ausgabe = "Bilder"

	# end of ausgabe_in_table	
		
	def suchhistorie(self, e):
		if not e or e == " ":
			return
		zu_lesen = "SELECT * FROM pordb_suche order by nr"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		vergleich = e + (200 - len(e)) * " " # Laenge des Vergleichsfeld auf 200 setzen
		zu_erfassen = []
		for i in res:
			if i[1] == vergleich:
				zu_erfassen.append("delete from pordb_suche where suche = '" +vergleich.replace("'", "''") +"'")
				break
		zu_erfassen.append("INSERT into pordb_suche (suche) VALUES ('" +e.decode('utf-8').replace("'", "''") +"')")
		if len(res) >= 20:
			zu_erfassen.append("delete from pordb_suche where nr = '" + str(res[0][0]) +"'")
			
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
	
		self.historie()
		
# end of suchhistorie

	def historie(self):
		self.suchfeld.clear()
		zu_lesen = "SELECT * FROM pordb_suche order by nr DESC"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		if res:
			for i in res:
				j = i[1].rstrip().decode("utf-8")
				self.suchfeld.addItem(j.replace("''", "'"))

	def onSuche(self):
		suche = Suchen(self)
		suche.lineEditDarsteller.setText(self.suche_darsteller)
		suche.lineEditDarsteller.setFocus()
		suche.lineEditCD.setText(self.suche_cd)
		suche.lineEditTitel.setText(self.suche_titel)
		suche.lineEditOriginal.setText(self.suche_original)
		suche.checkBoxVid.setChecked(self.video)
		try:
			suche.comboBoxCS.setCurrentIndex(suche.comboBoxCS.findText(self.suche_cs))
		except:
			pass
		if suche.exec_():
			self.suche_darsteller = suche.lineEditDarsteller.text()
			self.suche_cd = suche.lineEditCD.text()
			self.suche_titel = suche.lineEditTitel.text()
			self.suche_original = suche.lineEditOriginal.text()
			self.video = suche.checkBoxVid.isChecked()
			self.suche_cs = suche.comboBoxCS.currentText()
			# select-Anweisung aufbauen
			zu_lesen = "select * from pordb_vid where "
			argument = 0
			# Darsteller
			if self.suche_darsteller:
				argument = 1
				zu_lesen += "darsteller like '%" +str(self.suche_darsteller).title() +"%'"
		
			# CD
			if self.suche_cd:
				try:
					cd = int(self.suche_cd)
				except:
					message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("CD is not a number"))
					return
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "cd = " +str(cd)
	
			# Titel
			if self.suche_titel:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "titel like '%" +self.suche_titel +"%'"
	
			# Original 
			if self.suche_original:
				if argument == 1:
					zu_lesen += " and "	
				argument = 1
				zu_lesen += "original like '%" +str(self.suche_original).title() +"%'"
				
			# CS
			if self.suche_cs:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "cs" +str(self.suche_cs).split()[0] +"<> 0" 
			
			# Vid Button gesetzt
			if argument == 1 and self.video:
				zu_lesen += " and (nurbild != 'x' or nurbild is null)"
			
			zu_lesen += " order by cd, titel"
			app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.letzter_select_komplett = zu_lesen
			if argument != 0:
				self.start_bilder = 0
				self.ausgabe(zu_lesen, zu_lesen)
			app.restoreOverrideCursor()
		self.suchfeld.setFocus()
	# end of onSuche
				
	def onbildAnzeige(self):
		ein = self.eingabe_auswerten()
		if not ein:
			return
		res = self.darsteller_lesen(ein)
		if not res: 
			return
		for i in res:
			if i[1] == 'm' or i[1] == 'w': # not from pseudo_table
				name = i[0]
				bildname = i[0].lower().strip().replace(" ", "_").replace("'", "_apostroph_")
				self.bilddarsteller = self.verzeichnis_thumbs +"/darsteller_" +i[1] +"/" +bildname +".jpg"
				if not os.path.isfile(self.bilddarsteller):
					self.bilddarsteller = self.verzeichnis_thumbs +"/darsteller_" +i[1] +"/" +bildname +".png"
					if not os.path.isfile(self.bilddarsteller):
						self.bilddarsteller = self.verzeichnis_thumbs +"/nichtvorhanden/nicht_vorhanden.jpg"
				if i[11] and i[11] <> "0": # URL vorhanden
					self.pushButtonIAFDBackground.setEnabled(True)
				else:
					self.pushButtonIAFDBackground.setEnabled(False)
		self.bildSetzen()
		try:
			self.suchhistorie("=" +name)
		except:
			pass
		
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		self.onStatistik()
		self.onDarstellerFilme()
		self.onpaareSuchen()
		self.suchfeld.setCurrentIndex(-1)
		self.suchfeld.setFocus()
		self.listWidgetDarsteller.clearSelection()
		app.restoreOverrideCursor()
	# end of onbildAnzeige
	
	def bildSetzen(self):
		if self.bilddarsteller:
			# Multiplikation mit 0.05, da es eine Wechselwirkung mit dem Parent Frame gibt
			bild = QtGui.QPixmap(self.bilddarsteller).scaled(self.labelBildanzeige.parentWidget().width() - self.labelBildanzeige.parentWidget().width() * 0.05, self.labelBildanzeige.parentWidget().height() - self.labelBildanzeige.parentWidget().height() * 0.05, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			self.labelBildanzeige.setPixmap(bild)
			
	def onTabwechsel(self, tab):
		if tab == 4 or tab == 5:
			self.actionDrucken.setEnabled(False)
		else:
			self.actionDrucken.setEnabled(True)
		
	def onpaareSuchen(self):
		ein = self.eingabe_auswerten()
		if not ein:
			return
		res = self.darsteller_lesen(ein)
		if not res:
			return
		gesucht = res[0][0].strip().replace("'", "''")
		geschlecht = res[0][1]
		zu_lesen = "SELECT partner, cd, bild FROM pordb_partner where darsteller = '" +gesucht +"'"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		res2 = res[:]
		if self.comboBoxEthnicFilter.currentText():
			ethnic = str(self.comboBoxEthnicFilter.currentText())
			j = -1
			for i in res:
				j += 1
				zu_lesen = "select ethnic from pordb_darsteller where darsteller = '" +i[0].strip().replace("'", "''") +"'"
				lese_func = DBLesen(self, zu_lesen)
				res1 = DBLesen.get_data(lese_func)
				if res1[0][0] != ethnic:
					del res2[j]
					j -= 1
			self.comboBoxEthnicFilter.setCurrentIndex(-1)
			
		res = res2[:]
		if self.comboBoxCSFilter.currentText():
			cs = str(self.comboBoxCSFilter.currentText())[0:1]
			j = -1
			for i in res:
				j += 1
				zu_lesen = "select cs" +cs +" from pordb_vid where cd = " +str(i[1]) +" and bild = '" +i[2] +"'"
				lese_func = DBLesen(self, zu_lesen)
				res1 = DBLesen.get_data(lese_func)
				try:
					if res1[0][0] == 0:
						del res2[j]
						j -= 1
				except: 
					message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("There is something wrong with partners: ") +zu_lesen)
					return
			self.comboBoxCSFilter.setCurrentIndex(-1)
		
		self.paarung = []
		for i in res2:
			darsteller_liste = i[0].split(',')
			for j in darsteller_liste:
				if j.strip() != gesucht and j.strip() not in self.paarung:
					zu_lesen = "SELECT * FROM pordb_darsteller where darsteller = '" +j.strip().replace("'", "''") +"' order by darsteller"
					lese_func = DBLesen(self, zu_lesen)
					res = DBLesen.get_data(lese_func)
					try:
						if geschlecht != res[0][1] and res[0][1] != ' ':
							self.paarung.append(j.strip())
					except:
						message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("There is something wrong with partners: ") +j)
						return
		self.paarung.sort()
		self.listWidgetDarsteller.clear()
		self.listWidgetDarsteller.addItems(self.paarung)
		self.labelText.setText(self.trUtf8("has acted with: ") +str(len(self.paarung)))
		zu_erfassen = "update pordb_darsteller set partner = " +str(len(self.paarung)) +" where darsteller = '" +gesucht +"'"
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
	# end of onpaareSuchen
		
	def eingabe_auswerten(self):
		try:
			ein = str(self.suchfeld.currentText()).strip().title()
		except:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Illegal characters in search field"))
			return
		if not ein:
			selected = self.listWidgetDarsteller.selectedItems()
			if selected:
				ein = str(selected[0].text()).strip()
				ein = "=" +ein
		if not ein:
			ein = "=" +str(self.labelDarsteller.text()).strip().title()
		return ein
	
	def darsteller_lesen(self, ein):
		if ein[0] == '=':
			eingabe=ein.lstrip('=').replace("'", "''").title()
			zu_lesen = "SELECT * FROM pordb_darsteller where darsteller = '" +eingabe +"'"
			if self.comboBoxSex.currentText() == "Mann" or self.comboBoxSex.currentText() == "Male":
				zu_lesen += " and sex = 'm'"
			elif self.comboBoxSex.currentText() == "Frau" or self.comboBoxSex.currentText() == "Female":
				zu_lesen += " and sex = 'w'"
			zu_lesen += " order by darsteller"
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
		else:
			eingabe = ein.replace("'", "''").title()
			zu_lesen = "SELECT * FROM pordb_darsteller where darsteller like '%" +eingabe +"%'"
			if self.comboBoxSex.currentText() == "Mann" or self.comboBoxSex.currentText() == "Male":
				zu_lesen += " and sex = 'm'"
			elif self.comboBoxSex.currentText() == "Frau" or self.comboBoxSex.currentText() == "Female":
				zu_lesen += " and sex = 'w'"
			zu_lesen += " order by darsteller"
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			
			zu_lesen = "SELECT pseudo, darsteller FROM pordb_pseudo where pseudo like '%" +eingabe +"%'"
			zu_lesen += " order by darsteller"
			lese_func = DBLesen(self, zu_lesen)
			res1 = DBLesen.get_data(lese_func)
			if res1:
				for i in res1:
					zu_lesen = "SELECT * FROM pordb_darsteller where darsteller = '" +i[1].replace("'", "''") +"'"
					if self.comboBoxSex.currentText() == "Mann" or self.comboBoxSex.currentText() == "Male":
						zu_lesen += " and sex = 'm'"
					elif self.comboBoxSex.currentText() == "Frau" or self.comboBoxSex.currentText() == "Female":
						zu_lesen += " and sex = 'w'"

					lese_func = DBLesen(self, zu_lesen)
					res2 = DBLesen.get_data(lese_func)
					vorhanden = 0
					if res2:
						for j in res:
							if res2[0][0] == j[0]:
								vorhanden = 1
						if not vorhanden:
							res.extend(res2)
				res.sort()
			self.comboBoxSex.setCurrentIndex(0)
				
		self.comboBoxSex.setCurrentIndex(0)
		if len(res) > 1:
			self.listWidgetDarsteller.clear()
			for i in res:
				self.listWidgetDarsteller.addItem(i[0])
			self.labelText.setText("<font color=red>" +self.trUtf8("Please select:") +"</font>")
			self.suchfeld.setCurrentIndex(-1)
			return
		elif len(res) == 1:
			self.labelDarsteller.setText(res[0][0])
			if res[0][1] == "w":
				self.comboBoxGeschlecht.setCurrentIndex(0)
			else:
				self.comboBoxGeschlecht.setCurrentIndex(1)
			self.lineEditAnzahl.setText(str(res[0][2]))
			if res[0][4] != None:
				self.comboBoxHaarfarbe.setCurrentIndex(self.comboBoxHaarfarbe.findText(res[0][4].strip()))
			self.labelFehler.clear()
			if res[0][5] != None and res[0][5] != " " and res[0][5][0:1] != "-":
				if len(self.nationen) == 0:
					self.nation_fuellen()
				try:
					i = self.nationen.index(res[0][5])
					self.comboBoxNation.setCurrentIndex(i)
				except:
					self.comboBoxNation.setCurrentIndex(-1)
					self.labelFehler.setText("<font color=red>" +self.trUtf8("Data collection of actor seems to be not complete, nation: ") +res[0][5]  +"</font>")
			else:
				if res[0][5] and res[0][5][0:1] != "-":
					nation = res[0][5]
				else:
					nation = ""
					self.labelFehler.setText("<font color=red>" +self.trUtf8("Data collection of actor seems to be not complete, nation: ") +nation  +"</font>")
			if res[0][6] != None:
				self.lineEditTattoo.setText(res[0][6].decode("utf-8").strip())
			else:
				self.lineEditTattoo.setText("")
			if res[0][7] != None:
				self.comboBoxEthnic.setCurrentIndex(self.comboBoxEthnic.findText(res[0][7].strip()))
			if res[0][9] != None:
				geburtstag = (str(res[0][9])[0:10])
				self.lineEditGeboren.setText(str(res[0][9])[0:10])
				self.lineEditGeboren.setCursorPosition(0)
				if geburtstag != "0001-01-01":
					geboren = (str(res[0][9])[0:10]).split("-")
					jahr = int(geboren[0])
					monat = int(geboren[1])
					tag = int(geboren[2])
					alter = age((datetime.date(jahr, monat, tag)))
					self.labelAlter.setText(str(alter))
				else:
					self.labelAlter.clear()
			else:
				self.lineEditGeboren.setText("")
				self.labelAlter.clear()
			if res[0][10] != None:
				self.labelFilme.setText(str(res[0][10]))
			else:
				self.labelFilme.clear()
			aktiv = ""
			if res[0][12] != None:
				aktiv = str(res[0][12])
			if res[0][13] != None and res[0][13] != 0:
				aktiv += "-" +str(res[0][13])
			if res[0][14] != None:
				aktiv += " (" +str(res[0][14])[0:10] +")"
				#print "MONAT", str(res[0][14])[5:7]
			if aktiv:
				self.labelAktiv.setText(self.trUtf8("active : ") +aktiv)
				#self.labelText.setText("<font color=red>" +self.trUtf8("Actor not available") +"</font>")
			else:
				self.labelAktiv.clear()
		else:
			zu_lesen = "SELECT * FROM pordb_pseudo where pseudo = '" +eingabe +"'"
			if self.comboBoxSex.currentText() == self.trUtf8("Male"):
				zu_lesen += " and sex = 'm'"
			elif self.comboBoxSex.currentText() == self.trUtf8("Female"):
				zu_lesen += " and sex = 'w'"
			zu_lesen += " order by darsteller"
			lese_func = DBLesen(self, zu_lesen)
			res1 = DBLesen.get_data(lese_func)
			if res1:
				ein = res1[0][1].strip()
				res = self.darsteller_lesen(ein)
			else:
				self.labelText.setText("<font color=red>" +self.trUtf8("Actor not available") +"</font>")
				self.labelDarsteller.clear()
				self.labelAlter.clear()
				self.pushButtonIAFDBackground.setEnabled(False)
		self.letzter_select_komplett = zu_lesen
		self.suchfeld.setFocus()
		return res
	# end of darsteller_lesen
	
	def onDarstellerspeichern(self):
		name = str(self.labelDarsteller.text()).replace("'", "''")
		if not name:
			return
		try:
			ein = int(self.lineEditAnzahl.text())
		except:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Quantity is not a number"))
			self.lineEditAnzahl.setSelection(0, len(self.lineEditAnzahl.text()))
			return
		# update-Anweisung aufbauen
		if str(self.lineEditGeboren.text()):
			geboren = str(self.lineEditGeboren.text())
		else:
			geboren = "0001-01-01"
		datum = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(time.localtime()[2])
		zu_erfassen = unicode("update pordb_darsteller set anzahl = " +str(ein) +", haarfarbe = '" +str(self.comboBoxHaarfarbe.currentText()) +"', sex = '" +str(self.comboBoxGeschlecht.currentText()) +"', nation = '" +str(self.comboBoxNation.currentText())[0:2] +"', tattoo = '" +self.lineEditTattoo.text().replace("'", "''") +"', geboren = '" +geboren +"', ethnic = '" +str(self.comboBoxEthnic.currentText()) +"' where darsteller = '" +name +"'")
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		
		filename = self.verzeichnis_thumbs + os.sep + "darsteller_" +str(self.comboBoxGeschlecht.currentText()) + os.sep + name.strip().lower().replace(" ", "_") + ".jpg"
		if os.path.exists(filename):
			pass
		else:
			if str(self.comboBoxGeschlecht.currentText()) == "w":
				sex_alt = "m"
			else:
				sex_alt = "w"
			newfilename = self.verzeichnis_thumbs + os.sep + "darsteller_" +sex_alt + os.sep + name.strip().lower().replace(" ", "_") + ".jpg"
			if os.path.exists(newfilename):
				os.rename(newfilename, filename)
		
		self.labelFehler.clear()
		self.suchfeld.setFocus()
	# end of onDarstellerspeichern
	
	def onIAFD(self):
		ein = self.eingabe_auswerten()
		res = self.darsteller_lesen(ein)
		if res and res[0][11] and res[0][11] <> "0":
			app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			zaehler = 0
			while True:
				zaehler += 1
				try:
					seite = urllib2.urlopen(res[0][11]).read()
					bilddialog = DarstellerdatenAnzeigen(app, res[0][11], seite, self.verzeichnis_thumbs)
					app.restoreOverrideCursor()
					bilddialog.exec_()
					break
				except:
					pass
				if zaehler > 10:
					break
			app.restoreOverrideCursor()
			if zaehler > 10:
				message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Site of actor could not be found"))
				return
		else:
			clipboard = QtGui.QApplication.clipboard()
			clipboard.setText(ein.lstrip("="), mode=QtGui.QClipboard.Clipboard)
			self.tabWidget.setCurrentIndex(3)
			
	def onIAFDBackground(self):
		ein = self.eingabe_auswerten()
		res = self.darsteller_lesen(ein)
		if res[0][11]:
			monate = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12", }
			app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			zaehler = 0
			while True:
				zaehler += 1
				try:
					seite = urllib2.urlopen(res[0][11]).read()
					break
				except:
					pass
				if zaehler > 10:
					break
			if zaehler > 10:
				app.restoreOverrideCursor()
				message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Site of actor could not be found"))
				return
				
			# Darsteller Geboren
			anfang = seite.find('<b>Birthday')
			anfang = seite.find('">', anfang)
			ende = seite.find('</a>', anfang)
			try:
				geboren = seite[anfang+2:ende].decode("iso-8859-1")
				monat = monate.get(geboren[0:geboren.find(" ")], self.trUtf8("not available"))
			except:
				monat = self.trUtf8("not available")
			if monat != self.trUtf8("not available"):
				tag = geboren[geboren.find(" ")+1:geboren.find(",")]
				jahr = geboren[geboren.find(", ")+2:]
				geboren = jahr +"-" + monat + "-" + tag
			else:
				geboren = 0
				
			zu_erfassen = []
			if geboren == 0:
				if not res[0][9]:
					zu_erfassen.append("update pordb_darsteller set geboren = '0001-01-01' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			else:
				zu_erfassen.append("update pordb_darsteller set geboren = '" +str(geboren) +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			
			# Darsteller Anzahl Filme
			anfang = seite.find('moviecount">')
			if anfang > 0:
				ende = seite.find(' Title', anfang+1)
				filme = seite[anfang+12:ende].decode("iso-8859-1")
				try:
					filme = int(filme)
				except:
					pass
				if filme > 0:
					zu_erfassen.append("update pordb_darsteller set filme = '" +str(filme) +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
				
			# Darsteller aktiv von / bis
			anfang = seite.find('Years Active</b></td><td>')
			if anfang == -1:
				anfang = seite.find('Years Active as Performer</b></td><td>') 
				if anfang == -1:
					anfang = seite.find('Year Active</b></td><td>') + 24
				else:
					anfang += 38
			else:
				anfang += 25
			aktiv_von = seite[anfang:anfang + 4].decode("iso-8859-1")
			try:
				self.aktiv_von_int = int(aktiv_von)
			except:
				self.aktiv_von_int = 0
			aktiv_bis = seite[anfang + 5:anfang + 9].decode("iso-8859-1")
			try:
				self.aktiv_bis_int = int(aktiv_bis)
			except:
				self.aktiv_bis_int = 0

			if self.aktiv_von_int <> 0:
				zu_erfassen.append("update pordb_darsteller set aktivvon = '" +aktiv_von +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			if self.aktiv_bis_int <> 0:
				zu_erfassen.append("update pordb_darsteller set aktivbis = '" +aktiv_bis +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
					
			datum = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(time.localtime()[2])
			zu_erfassen.append("update pordb_darsteller set besuch = '" +datum +"' where darsteller = '" +res[0][0].replace("'", "''") +"'")
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
				
			self.onbildAnzeige()
				
			app.restoreOverrideCursor()
	
	def onDarstellerloeschen(self):
		name = str(self.labelDarsteller.text())
		if not name:
			return
		messageBox = QtGui.QMessageBox()
		messageBox.addButton(self.trUtf8("Yes"), QtGui.QMessageBox.AcceptRole)
		messageBox.addButton(self.trUtf8("No"), QtGui.QMessageBox.RejectRole)
		messageBox.setWindowTitle(self.trUtf8("Actor ") +name.strip() +self.trUtf8(" will be deleted now"))
		messageBox.setIcon(QtGui.QMessageBox.Question)
		messageBox.setText(self.trUtf8("Should the actor really be deleted?"))
		message = messageBox.exec_()
		if message == 0:
			zu_erfassen = []
			# delete-Anweisung aufbauen
			zu_erfassen.append("delete from pordb_pseudo where darsteller = '" +name.replace("'", "''") +"'")
			zu_erfassen.append("delete from pordb_darsteller where darsteller = '" +name.replace("'", "''") +"'")
			zu_erfassen.append("delete from pordb_partner where darsteller = '" +name.replace("'", "''") +"'")
			zu_erfassen.append("delete from pordb_partner where partner = '" +name.replace("'", "''") +"'")
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
			bildname = name.strip().lower().replace(" ", "_").replace("'", "_apostroph_")
			datei_alt = self.verzeichnis_thumbs +os.sep +"darsteller_" +self.comboBoxGeschlecht.currentText() +os.sep +bildname +".jpg"
			try:
				os.remove(datei_alt)
			except:
				pass
		self.labelFehler.clear()
		self.suchfeld.setFocus()
	# end of onDarstellerloeschen
	
	def onNeueingabe(self, undo = None, cover_anlegen = None, dateien = None):
		self.suchfeld.setFocus()
		if undo:
			dateiliste = os.listdir(self.verzeichnis_trash)
			if not dateiliste:
				return
			j = 0
			for i in dateiliste:
				if os.path.splitext(i)[-1] == ".txt":
					datei = file(self.verzeichnis_trash +"/" +i, "r")
					text = datei.readlines()
				elif os.path.splitext(i)[-1].lower() == ".jpg" or os.path.splitext(i)[-1].lower() == ".jpeg" or os.path.splitext(i)[-1].lower() == ".png":
					j += 1
					self.file = QtCore.QString(self.verzeichnis_trash +os.sep +i)
			titel = text[0].strip()
			darsteller = text[1].strip()
			cd = text[2].strip()
			bild = text[3].strip()
			nurbild = text[4].strip()
			original = text[5].strip().decode("utf-8")
			cs = []
			cs.append(text[9].strip() +'f')
			cs.append(text[10].strip() +'h')
			cs.append(text[11].strip() +'t')
			cs.append(text[12].strip() +'c')
			cs.append(text[13].strip() +'x')
			cs.append(text[14].strip() +'o')
			cs.append(text[15].strip() +'v')
			cs.append(text[16].strip() +'b')
			cs.append(text[17].strip() +'a')
			cs.append(text[18].strip() +'s')
			cs.append(text[19].strip() +'k')
			vorhanden = text[7].strip()
			if len(text) > 20 and text[20].strip() == "COVER":
				trash_cover = "x"
			else:
				trash_cover = None
			if j != 1:
				self.file = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8("Image files"), self.verzeichnis_trash, self.trUtf8("Image files (*.jpg *.jpeg *.png);;all files (*.*)"))
			eingabedialog = Neueingabe(self.verzeichnis, self.verzeichnis_original, self.verzeichnis_thumbs, self.verzeichnis_trash, self.verzeichnis_cover, self.file, titel, darsteller, cd, bild, nurbild, original, cs, 
				vorhanden, "", undo, original_cover=trash_cover)
		else:
			if dateien:
				self.file = dateien[0]
				if len(dateien) == 2:
					self.onCover(datei = dateien)
			else:
				try:
					dateiliste = os.listdir(self.verzeichnis)
				except:
					self.verzeichnis = self.verzeichnis_original
					dateiliste = os.listdir(self.verzeichnis)
				j = 0
				for i in dateiliste:
					if os.path.splitext(i)[-1].lower() == ".jpg" or os.path.splitext(i)[-1].lower() == ".jpeg" or os.path.splitext(i)[-1].lower() == ".png":
						j += 1
						self.file = QtCore.QString(self.verzeichnis +os.sep +i)
				if j != 1:
					#self.verzeichnis = os.path.dirname(str(self.file))
					self.file = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8("Image files"), self.verzeichnis, self.trUtf8("Image files (*.jpg *.jpeg *.png);;all files (*.*)"))
					if self.file:
						self.verzeichnis = os.path.dirname(str(self.file))
			eingabedialog = Neueingabe(self.verzeichnis, self.verzeichnis_original, self.verzeichnis_thumbs, self.verzeichnis_trash, self.verzeichnis_cover, self.file, cover_anlegen = cover_anlegen)
		if not self.file:
			return
		
		if not undo:
			self.verzeichnis = os.path.dirname(str(self.file))
		
		eingabedialog.exec_()
		zu_lesen = "select * from pordb_vid_neu"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		self.spinBoxAktuell.setValue(res[0][2])
		self.statusBar.showMessage("ins:CD" +str(res[0][2]) +" Title:" +res[0][0].strip() +" Act:" +res[0][1].strip())
	# end onNeueingabe
		
	def onKorrektur(self, zeile, spalte):
		item = self.tableWidgetBilder.currentItem()
		column = self.tableWidgetBilder.column(item)
		row = self.tableWidgetBilder.row(item)
		index = int(row * self.columns + column + self.start_bilder)
		if item:
			if self.aktuelle_ausgabe == "Darsteller":
				self.onDarstellerUebernehmen()
				self.onbildAnzeige()
				self.changeTab("F3")
				return
			#if len(text) == 1:
			if 1 == 2:
				items = self.tableWidgetBilder.selectedItems()
				dateien = []
				for i in items:
					dateien.append(str(self.verzeichnis +os.sep +i.text()))
				self.onNeueingabe(dateien=dateien)
			else:
				cd = self.aktuelles_res[index][2]
				titel = self.aktuelles_res[index][0]
				darsteller = self.aktuelles_res[index][1]
				bild = self.aktuelles_res[index][3]
				nurbild = self.aktuelles_res[index][4]
				if self.aktuelles_res[index][5]:
					original = self.aktuelles_res[index][5].decode("utf-8")
				else:
					original = ""
				cs = []
				cs.append(str(self.aktuelles_res[index][9]) +'f')
				cs.append(str(self.aktuelles_res[index][10]) +'h')
				cs.append(str(self.aktuelles_res[index][11]) +'t')
				cs.append(str(self.aktuelles_res[index][12]) +'c')
				cs.append(str(self.aktuelles_res[index][13]) +'x')
				cs.append(str(self.aktuelles_res[index][14]) +'o')
				cs.append(str(self.aktuelles_res[index][15]) +'v')
				cs.append(str(self.aktuelles_res[index][16]) +'b')
				cs.append(str(self.aktuelles_res[index][17]) +'a')
				cs.append(str(self.aktuelles_res[index][18]) +'s')
				cs.append(str(self.aktuelles_res[index][19]) +'k')
				if self.aktuelles_res[index][7]:
					vorhanden = self.aktuelles_res[index][7]
				else:
					vorhanden = ""
				self.file = str(self.verzeichnis_thumbs +os.sep +"cd" +str(cd) +os.sep +self.aktuelles_res[index][3]).strip()
				cover = False
				if not os.path.exists(self.file):
					self.file = str(self.verzeichnis_cover +os.sep +self.aktuelles_res[index][3]).strip()
					cover = True
				zu_lesen = "select * from pordb_original where foreign_key_pordb_vid = " +str(self.aktuelles_res[index][8])
				lese_func = DBLesen(self, zu_lesen)
				res2 = DBLesen.get_data(lese_func)
				original_weitere = []
				for i in res2:
					original_weitere.append(i[1])
				eingabedialog = Neueingabe(self.verzeichnis, self.verzeichnis_original, self.verzeichnis_thumbs, self.verzeichnis_trash, self.verzeichnis_cover, self.file, titel, darsteller, cd, bild, nurbild, original, cs, vorhanden, cover, None, None, original_weitere)
				if eingabedialog.exec_():
					self.statusBar.showMessage("upd:CD" +str(self.aktuelles_res[index][2]) +" Title:" +self.aktuelles_res[index][0].strip() +" Act:" +self.aktuelles_res[index][1].strip())
		self.suchfeld.setFocus()
	# end of onKorrektur
		
	def onDarstellerSuchen(self):
		suche = DarstellerSuchen()
		
		if suche.exec_():
			app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			self.sucheD_darsteller = suche.lineEditDarstellerSuche.text()
			self.sucheD_geschlecht = suche.comboBoxDarstellerSucheGeschlecht.currentText()
			self.sucheD_ab = suche.dateEditDarstellerSucheAb.date().toString("yyyy-MM-dd")
			self.sucheD_bis = suche.dateEditDarstellerSucheBis.date().toString("yyyy-MM-dd")
			self.sucheD_haar = suche.comboBoxDarstellerSucheHaar.currentText()
			self.sucheD_nation = suche.comboBoxDarstellerSucheNation.currentText()
			self.sucheD_tattoo = suche.comboBoxDarstellerSucheTattoo.currentText()
			self.sucheD_etattoo = suche.lineEditDarstellerSucheTattoo.text()
			self.sucheD_ethnic = suche.comboBoxDarstellerSucheEthnic.currentText()
		# select-Anweisung aufbauen
			zu_lesen = "select * from pordb_darsteller where "
			argument = 0
			#Name
			if self.sucheD_darsteller:
				argument = 1
				zu_lesen += "darsteller like '%" +self.sucheD_darsteller +"%'"
	
			# Geschlecht
			if self.sucheD_geschlecht:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "sex = '" +self.sucheD_geschlecht +"'"
	
			# Datum >=
			if argument == 1:
				zu_lesen += " and "
			argument = 1
			zu_lesen += "datum >= '" +self.sucheD_ab +"'"
	
			# Datum_bis <=
			if argument == 1:
				zu_lesen += " and "
			argument = 1
			zu_lesen += "datum <= '" +self.sucheD_bis +"'"
	
			# Haarfarbe
			if self.sucheD_haar:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "haarfarbe = '" +self.sucheD_haar +"'"
	
			# Nation
			if self.sucheD_nation:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "nation = '" +self.sucheD_nation[0:2] +"'"
	
			# Tattoo
			if self.sucheD_tattoo == self.trUtf8("yes"):
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "tattoo is not null and tattoo != '-'"
			elif self.sucheD_tattoo == self.trUtf8("no"):
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "(tattoo = '' or tattoo = '-')"
			if self.sucheD_etattoo:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "tattoo like '%" +self.sucheD_etattoo +"%'"
	
			# Ethnic
			if self.sucheD_ethnic:
				if argument == 1:
					zu_lesen += " and "
				argument = 1
				zu_lesen += "ethnic = '" +self.sucheD_ethnic +"'"
	
			zu_lesen += " order by darsteller"
			
			self.letzter_select_komplett = zu_lesen
	
			if argument != 0:
				lese_func = DBLesen(self, zu_lesen)
				self.aktuelles_res = DBLesen.get_data(lese_func)
				self.start_bilder = 0
				self.ausgabedarsteller()
			app.restoreOverrideCursor()
	# enf of onDarstellerSuchen

	def ausgabedarsteller(self):
		self.tableWidgetBilder.clear()
		res = self.aktuelles_res[int(self.start_bilder):int(self.start_bilder) + int(self.anzahl_bilder)]
		self.tableWidgetBilder.setRowCount(round(len(res) / self.columns + 0.4))
		if len(res) < self.columns:
			self.tableWidgetBilder.setColumnCount(len(res))
		else:
			self.tableWidgetBilder.setColumnCount(self.columns)
		zeile = 0
		spalte = -1
		for i in res:
			if len(i[0]) == 1:
				bildname = i.lower().strip().replace(" ", "_").replace("'", "_apostroph_")
				text = i
				if os.path.exists(self.verzeichnis_thumbs +"/darsteller_w/" +bildname +".jpg"):
					dateiname = self.verzeichnis_thumbs +"/darsteller_w/" +bildname +".jpg"
				elif os.path.exists(self.verzeichnis_thumbs +"/darsteller_w/" +bildname +".png"):
					dateiname = self.verzeichnis_thumbs +"/darsteller_w/" +bildname +".png"
				elif os.path.exists(self.verzeichnis_thumbs +"/darsteller_m/" +bildname +".jpg"):
					dateiname = self.verzeichnis_thumbs +"/darsteller_m/" +bildname +".jpg"
				else:
					dateiname = self.verzeichnis_thumbs +"/darsteller_m/" +bildname +".png"
			else:
				bildname = i[0].lower().strip().replace(" ", "_").replace("'", "_apostroph_")
				text = i[0]
				if os.path.exists(self.verzeichnis_thumbs +"/darsteller_" +i[1] +"/" +bildname +".jpg"):
					dateiname = self.verzeichnis_thumbs +"/darsteller_" +i[1] +"/" +bildname +".jpg"
				else:
					dateiname = self.verzeichnis_thumbs +"/darsteller_" +i[1] +"/" +bildname +".png"
			bild = QtGui.QIcon(dateiname)
			newitem = QtGui.QTableWidgetItem(bild, text)
			spalte += 1
			if spalte == self.columns:
				spalte = 0
				zeile += 1
			self.tableWidgetBilder.setItem(zeile, spalte, newitem)
		self.restarbeiten_bilder()
		self.suchfeld.setCurrentIndex(-1)
		self.suchfeld.setFocus()
		self.tabWidget.setCurrentIndex(0)
		self.aktuelle_ausgabe = "Darsteller"
	# end of ausgabedarsteller
	
	def restarbeiten_bilder(self):
		self.tableWidgetBilder.scrollToTop()
		vertical_header = range(int(round(self.start_bilder / self.columns + 0.4)), int(round((self.start_bilder + self.anzahl_bilder) / self.columns + 0.4))) 
		for i in range(len(vertical_header)):
			vertical_header[i] = str(vertical_header[i] + 1)
		self.tableWidgetBilder.setVerticalHeaderLabels(vertical_header)
		self.tableWidgetBilder.resizeRowsToContents()
		self.tableWidgetBilder.resizeColumnsToContents()
		self.anzahl.setText(self.trUtf8("Quantity: ") +str(len(self.aktuelles_res)))
		seite_von = int(round(self.start_bilder / self.anzahl_bilder + 1))
		seite_bis = int(round(len(self.aktuelles_res) / float(self.anzahl_bilder) + 0.499999))
		self.labelSeite.setText(self.trUtf8("Page ") +str(seite_von) + self.trUtf8(" of ") +str(seite_bis))
		if seite_von == 1:
			self.actionFirst.setEnabled(False)
			self.actionPrev.setEnabled(False)
		else:
			self.actionFirst.setEnabled(True)
			self.actionPrev.setEnabled(True)
			self.suchfeld.setFocus()
		if seite_von == seite_bis:
			self.actionLast.setEnabled(False)
			self.actionNext.setEnabled(False)
		else:
			self.actionLast.setEnabled(True)
			self.actionNext.setEnabled(True)
			self.suchfeld.setFocus()
			
		if seite_von < seite_bis:
			horizontal_header = range(int(self.columns))
			for i in range(len(horizontal_header)):
				horizontal_header[i] = str(horizontal_header[i] + 1) +"  >>>>>>>>>>>>>>>>>"
			self.tableWidgetBilder.setHorizontalHeaderLabels(horizontal_header)
	
	def onUndo(self):
		self.onNeueingabe(undo = 1)
		
	def onStatistik(self):
		ein = self.eingabe_auswerten()
		if not ein:
			return
		if ein[0] == '=':
			zu_lesen = "SELECT * FROM pordb_vid where darsteller = '"+ein.replace("'", "''").strip("=") +"' or darsteller like '" +ein.replace("'", "''").strip("=") +",%' or darsteller like '%, " +ein.replace("'", "''").strip("=") +",%' or darsteller like '%, " +ein.replace("'", "''").strip("=") + "'"
		else:
			zu_lesen = "SELECT * FROM pordb_vid where darsteller like '%" +ein.replace("'", "''") +"%'"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		sum_f = sum_h = sum_t = sum_c = sum_x = sum_o = sum_v = sum_b = sum_a = sum_s = 0
		cs = []
		for i in res:
			sum_f += i[9]
			sum_h += i[10]
			sum_t += i[11]
			sum_c += i[12]
			sum_x += i[13]
			sum_o += i[14]
			sum_v += i[15]
			sum_b += i[16]
			sum_a += i[17]
			sum_s += i[18]
		cs.append(sum_f)
		cs.append(sum_h)
		cs.append(sum_t)
		cs.append(sum_c)
		cs.append(sum_x)
		cs.append(sum_o)
		cs.append(sum_v)
		cs.append(sum_b)
		cs.append(sum_a)
		cs.append(sum_s)
		cs_summe = sum_f + sum_h + sum_t + sum_c + sum_x + sum_o + sum_v + sum_b + sum_a + sum_s
		cs.append(cs_summe)
		stats = []
		k = -1
		for i in ["Facial......", "Handjob.....", self.trUtf8("Tits........"), "Creampie....", "Analcreampie", "Oralcreampie", self.trUtf8("Cunt........"), self.trUtf8("Belly......."), self.trUtf8("Ass........."), self.trUtf8("Others......"), self.trUtf8("Summary.....")]:
			k += 1
			if i == self.trUtf8("Summary....."):
				stats.append("________________________")
				stats.append("")
			try:
				prozent = cs[k] * 100.0 / cs_summe
			except:
				prozent = 0
			stats.append(("%-13.28s %3.4s %6.2f") % (i, cs[k], prozent))
		self.listWidgetStatistik.clear()
		self.listWidgetStatistik.addItems(stats)
	# end of onStatistik
		
	def onDarstellerUmbenennen(self):
		ein = self.eingabe_auswerten()
		vorname = ""
		if ein.find('=') == 0:
			vorname = "X"
			eingabe = ein.lstrip('=').title().replace("'", "''")
		else:
			eingabe = ein.title().replace("'", "''")
		if not ein:
			return
		umbenennen = DarstellerUmbenennen(ein)
		if umbenennen.exec_():
			app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
			neuer_name = umbenennen.lineEditNeuerName.text()
			if neuer_name:
				neuer_name = str(neuer_name).strip()
				zu_lesen = "select * from pordb_pseudo where pseudo = '" +neuer_name.replace("'", "''") +"'"
				lese_func = DBLesen(self, zu_lesen)
				res = DBLesen.get_data(lese_func)
				if res:
					app.restoreOverrideCursor()
					message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("New name already exists as alias, please first edit/delete the aliases"))
					return
				if vorname:
					zu_lesen = "SELECT * FROM pordb_vid where (darsteller = '" +eingabe +"' or darsteller like '" +eingabe +",%' or darsteller like '%, " +eingabe +",%' or darsteller like '%, " +eingabe +"')"
					
				else:
					zu_lesen = "SELECT * FROM pordb_vid where darsteller like '%" +eingabe +"%'"
				lese_func = DBLesen(self, zu_lesen)
				res = DBLesen.get_data(lese_func)
				res1 = []
				darsteller_liste = []
				for i in res:
					darsteller_liste = i[1].split(',')
					for j in range(len(darsteller_liste)):
						darsteller_liste[j] = darsteller_liste[j].strip().replace("'", "''")
					res1.append([i[2], i[3], darsteller_liste])
				k = -1
				res2 = res1[:]
				for i in res1:
					k += 1
					if eingabe not in i[2]:
						del res2[k]
						k -=1
				zu_lesen = "select * from pordb_darsteller where darsteller = '" +eingabe +"'"
				lese_func = DBLesen(self, zu_lesen)
				res = DBLesen.get_data(lese_func)
				if res[0][3] == None:
					res[0][3] = '2000-01-01'
				if res[0][9]:
					geboren = str(res[0][9])
				else:
					geboren = "0001-01-01"
				if res[0][11]:
					url = res[0][11]
				else:
					url = 0
				if res[0][12]:
					aktivvon = res[0][12]
				else:
					aktivvon = 0
				if res[0][13]:
					aktivbis = res[0][13]
				else:
					aktivbis = 0
				if res[0][14]:
					besucht = str(res[0][14])
				else:
					besucht = "0001-01-01"
					
					
				zu_erfassen = []
				zu_lesen = "select darsteller from pordb_darsteller where darsteller = '" +neuer_name.replace("'", "''") +"'"
				lese_func = DBLesen(self, zu_lesen)
				res3 = DBLesen.get_data(lese_func)
				if res3:
					zu_erfassen.append("update pordb_darsteller set anzahl = anzahl + " +str(len(res2)) +" where darsteller = '" +neuer_name.replace("'", "''") +"'")
				else:
					zu_erfassen.append("insert into pordb_darsteller values ('" +neuer_name.title().replace("'", "''").lstrip("=") +"', '" +res[0][1] +"', " +str(res[0][2]) +", '" +str(res[0][3]) +"', '" +res[0][4] +"', '" +res[0][5] +"', '" +res[0][6].replace("'", "''") +"', '" +res[0][7] +"', '" +str(res[0][8]) +"', '" +str(geboren) +"', '" +str(res[0][10]) +"', '" 
					+str(url).replace("'", "''") +"', '" +str(aktivvon) +"', '" +str(aktivbis) +"', '" +str(besucht) +"')")

				
				zu_erfassen.append("update pordb_pseudo set darsteller = '" +neuer_name.title().replace("'", "''").lstrip("=") +"' where darsteller = '" +eingabe +"'")
				zu_erfassen.append("delete from pordb_darsteller where darsteller = '" +eingabe +"'")
				l = -1
				bildname = eingabe.lower().replace(" ", "_").replace("''", "_apostroph_")
				datei_alt = self.verzeichnis_thumbs +"/darsteller_" +res[0][1] +"/" +bildname +".jpg"
				bildname = neuer_name.lower().strip().replace("'", "''").lstrip("=").replace(" ", "_").replace("''", "_apostroph_")
				datei_neu = self.verzeichnis_thumbs +"/darsteller_" +res[0][1] +"/" +bildname +".jpg"
				sortier = Neueingabe(self.verzeichnis, self.verzeichnis_original, self.verzeichnis_thumbs, self.verzeichnis_trash, self.verzeichnis_cover, datei_alt)
				for i in res2:
					l += 1
					k = -1
					for j in i[2]:
						k += 1
						if j == eingabe:
							res2[l][2][k] = str(eingabe).title().lstrip("=")
					darsteller_liste = sortier.darsteller_sortieren(res2[l][2])
					darsteller_liste2 = [neuer_name.title().replace("'", "''") if x==eingabe.title().lstrip("=") else x for x in darsteller_liste]
					zu_erfassen.append("update pordb_vid set darsteller = '" +", ".join(darsteller_liste2) +"' where cd = " +str(i[0]) +" and bild = '" +i[1] +"'")
				if os.path.exists(datei_alt) and os.path.exists(datei_neu) and datei_alt <> datei_neu:
					messageBox = QtGui.QMessageBox()
					messageBox.addButton(datei_alt, QtGui.QMessageBox.AcceptRole)
					messageBox.addButton(datei_neu, QtGui.QMessageBox.AcceptRole)
					messageBox.setWindowTitle(self.trUtf8("Select an image of the actor"))
					messageBox.setIcon(QtGui.QMessageBox.Question)
					messageBox.setText(self.trUtf8("Which image of the actor should be taken?"))
					message = messageBox.exec_()
					if message == 0:
						try:
							os.remove(datei_neu)
							os.rename(datei_alt, datei_neu)
						except:
							message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Image file could not be renamed"))
					else:
						try:
							os.remove(datei_alt)
						except:
							message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Image file could not be renamed"))
				else:
					try:
						os.rename(datei_alt, datei_neu)
					except:
						message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Image file could not be renamed"))
				self.statusBar.showMessage(str(len(res2)) + self.trUtf8(" lines changed"))
				
				zu_lesen = "select * from pordb_partner where darsteller = '" +eingabe +"'"
				lese_func = DBLesen(self, zu_lesen)
				res = DBLesen.get_data(lese_func)
				for i in res:
					zu_erfassen.append("insert into pordb_partner values ('" +neuer_name.title().replace("'", "''") +"', '" +str(i[1]).replace("'", "''") +"'," +str(i[2]) +",'" +str(i[3]) +"')")
					zu_erfassen.append("delete from pordb_partner where darsteller = '" +eingabe +"'")
					
				zu_lesen = "select * from pordb_partner where partner = '" +eingabe +"'"
				lese_func = DBLesen(self, zu_lesen)
				res = DBLesen.get_data(lese_func)
				for i in res:
					zu_erfassen.append("insert into pordb_partner values ('" +str(i[0]).replace("'", "''") +"', '" +neuer_name.title().replace("'", "''") +"'," +str(i[2]) +",'" +str(i[3]) +"')")
					zu_erfassen.append("delete from pordb_partner where partner = '" +eingabe +"'")
					
				update_func = DBUpdate(self, zu_erfassen)
				DBUpdate.update_data(update_func)
					
		try:
			self.labelDarsteller.setText(neuer_name.replace("''", "'").title())
		except:
			pass
		app.restoreOverrideCursor()
		self.suchfeld.setCurrentIndex(-1)
		self.suchfeld.setFocus()
	# end of onDarstellerUmbenennen
	
	def onDarstellerBild(self):
		name = str(self.labelDarsteller.text()).strip().lstrip("=")
		self.file = QtGui.QFileDialog.getOpenFileName(self, self.trUtf8("Image of the actor: " +name +(", please select")), self.verzeichnis, self.trUtf8("Image files (*.jpg *.jpeg *.png);;all files (*.*)"))
		if self.file:
			bild = QtGui.QImage(self.file)
			if bild.width() > size_darsteller.width() or bild.height() > size_darsteller.height():
				message = QtGui.QMessageBox.warning(self, self.trUtf8("Caution! "), self.trUtf8("Image of the actor is very big"))
			zu_lesen = "select sex from pordb_darsteller where darsteller = '" +name.replace("'", "''")  +"'"
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			extension = os.path.splitext(str(self.file))[-1].lower()
			if extension == '.jpeg':
				extension = '.jpg'
			try:
				sex = res[0][0]
				newfilename = self.verzeichnis_thumbs +os.sep +"darsteller_" +sex +os.sep +name.replace(" ", "_").replace("'", "_apostroph_").lower() + extension
				os.rename(self.file, newfilename)
			except:
				pass
			self.onbildAnzeige()
	# end of onDarstellerBild
		
	def onDarstellerFilme(self):
		ein = self.eingabe_auswerten()
		if not ein:
			return
		res = self.darsteller_lesen(ein)
		if not res:
			return
		geschlecht = res[0][1]
		if ein[0] == '=':
			zu_lesen = "SELECT distinct on (original) original FROM pordb_vid where darsteller = '"+ein.replace("'", "''").strip("=") +"' or darsteller like '" +ein.replace("'", "''").strip("=") +",%' or darsteller like '%, " +ein.replace("'", "''").strip("=") +",%' or darsteller like '%, " +ein.replace("'", "''").strip("=") + "'"
		else:
			zu_lesen = "SELECT distinct on (original) original FROM pordb_vid where darsteller like '%" +ein.replace("'", "''") +"%'"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		filme = []
		for i in res:
			if i[0] and i[0].strip() > " " and i[0].strip() != "Wmv":
				filme.append(str(i[0]).strip().decode("utf-8"))
		self.listWidgetFilme.clear()
		self.listWidgetFilme.addItems(filme)
		self.pushButtonSort.setText(QtGui.QApplication.translate("Dialog", "Year", None, QtGui.QApplication.UnicodeUTF8))
	# end of onDarstellerFilme
		
	def onFilmeSortieren(self):
		def vergleich(a, b):
			if a[len(a) - 4 : len(a)] == " Wmv":
				wmv_abzug_a = 4
			else:
				wmv_abzug_a = 0
			if b[len(b) - 4 : len(b)] == " Wmv":
				wmv_abzug_b = 4
			else:
				wmv_abzug_b = 0
			if a[len(a) - 1 - wmv_abzug_a] == ")":
				if len (b) and b[len(b) - 1 - wmv_abzug_b] == ")": #beide Filme haben Jahr: direkter Vergleich
					wert1 = a[len(a) - 5 - wmv_abzug_a : len(a) - 1 - wmv_abzug_a]
					wert2 = b[len(b) - 5 - wmv_abzug_b : len(b) - 1 - wmv_abzug_b]
					if wert1 < wert2:
						return -1
					else:
						return 0
				else:			# anderenfalls: a gewinnt
					return 1
			else:
				if len (b) and b[len(b) - 1 - wmv_abzug_b] == ")": # hat nur b das Jahr: b gewinnt
					return -1
				else:			# haben beide kein Jahr: egal
					return 0
				
		text = self.pushButtonSort.text()
		if text == self.trUtf8("Jahr"):
			items = []
			for i in xrange(self.listWidgetFilme.count()):
				items.append(unicode(self.listWidgetFilme.item(i).text()).strip())
			items.sort(vergleich)
			self.listWidgetFilme.clear()
			self.listWidgetFilme.addItems(items)
			self.pushButtonSort.setText(QtGui.QApplication.translate("Dialog", "Title", None, QtGui.QApplication.UnicodeUTF8))
		else:
			self.listWidgetFilme.sortItems()
			self.pushButtonSort.setText(QtGui.QApplication.translate("Dialog", "Year", None, QtGui.QApplication.UnicodeUTF8))
		self.suchfeld.setFocus()
	# end of onFilmeSortieren

	def onPartnerZeigen(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		self.start_bilder = 0
		self.aktuelles_res = []
		for i in xrange(self.listWidgetDarsteller.count()):
			self.aktuelles_res.append(str(self.listWidgetDarsteller.item(i).text()).strip())
		
		self.ausgabedarsteller()
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
	# end of onPartnerZeigen
	
	def onPseudo(self):
		ein = self.eingabe_auswerten()
		if not ein:
			return
		zu_lesen = "select pseudo from pordb_pseudo where darsteller = '" +ein.lstrip('=').replace("'", "''") +"' order by pseudo"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		bilddialog = PseudonymeBearbeiten(ein, res)
		bilddialog.exec_()
		self.suchfeld.setFocus()
	# end of onPseudo
	
	def onSuchen(self):
		import locale
		locale.setlocale(locale.LC_ALL, '')
		ein = unicode(self.lineEditSuchen.text()).strip().replace(".", " ").encode("utf-8")
		if not ein:
			self.lineEditSuchen.setFocus()
			return
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		self.lineEditSuchen.setText(ein.decode("utf-8"))
		zu_lesen = "select * from pordb_mpg_katalog where lower(file) like '%" +ein.replace("'", "''").lower().replace(" ", "%") +"%' order by file"
		lese_func = DBLesen(self, zu_lesen)
		rows = DBLesen.get_data(lese_func)
		self.tableWidget.setSortingEnabled(False)
		self.tableWidget.clear()
		self.tableWidget.setRowCount(len(rows))
		zeilen = []
		if len(rows) == 0:
			self.tableWidget.setColumnCount(0)
		else:
			self.tableWidget.setColumnCount(len(rows[0]) +1)
			for i in xrange(len(rows)):
				zeile = list(rows[i])
				if rows[i][4]:
					zeile.append(round(rows[i][4] / 1024.0 / 1024.0, 2))
				zeilen.append(zeile)
		self.tableWidget.setAlternatingRowColors(True)
		self.tableWidget.setHorizontalHeaderLabels(self.fieldnames_mpg)
		for i in xrange(len(zeilen)):
			for j in xrange(len(zeilen[i])):
				mb = 0
				try:	# fieldtype is char
					newitem = QtGui.QTableWidgetItem(zeilen[i][j].strip().decode("utf-8"))
				except:
					try:	# fieldtype is int
						newitem = QtGui.QTableWidgetItem()
						if type(zeilen[i][j]) == long:
							wert = locale.format("%d", zeilen[i][j], grouping=True)
							newitem.setData(0, wert)
						elif type(zeilen[i][j]) == float:
							wert = locale.format("%.2f", zeilen[i][j], grouping=True)
							newitem.setData(0, wert)
						else:
							newitem.setData(0, QtCore.QVariant(int(zeilen[i][j])))
					except:	# fieldtype is None
						newitem = QtGui.QTableWidgetItem(" ")
				self.tableWidget.setItem(i, j, newitem)
		try:
			self.tableWidget.resizeColumnsToContents()
			self.tableWidget.resizeRowsToContents()
			self.tableWidget.setSortingEnabled(True)
		except:
			pass
		self.tableWidget.scrollToTop()
		zeilen = len(rows)
		self.labelMpgGefunden.setText(str(zeilen) +self.trUtf8(" found"))
			
		zu_lesen = "select * from pordb_original where lower(original) like '%" +ein.lower().replace("'", "''") +"%'"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		original_erweiterung = ""
		for i in res:
			original_erweiterung += " or primkey = " +str(i[2])
		zu_lesen = "SELECT * FROM pordb_vid where lower(original) like '%" +ein.lower().replace("'", "''") +"%'"
		if original_erweiterung:
			zu_lesen += original_erweiterung
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		
		self.tableWidget1.setSortingEnabled(False)
		self.tableWidget1.clear()
		self.tableWidget1.setRowCount(len(res))
		if len(res) == 0:
			self.tableWidget1.setColumnCount(0)
		else:
			self.tableWidget1.setColumnCount(len(res[0]))
		self.tableWidget1.setAlternatingRowColors(True)
		self.tableWidget1.setHorizontalHeaderLabels(self.fieldnames_vid)
		for i in xrange(len(res)):
			for j in xrange(len(res[0])):
				try:	# fieldtype is char
					newitem = QtGui.QTableWidgetItem(res[i][j].strip().decode("utf-8"))
				except:
					try:	# fieldtype is int
						newitem = QtGui.QTableWidgetItem(str(res[i][j]))
					except:	# fieldtype is None
						newitem = QtGui.QTableWidgetItem(" ")
				self.tableWidget1.setItem(i, j, newitem)
		try:
			self.tableWidget1.resizeColumnsToContents()
			self.tableWidget1.resizeRowsToContents()
			self.tableWidget1.setSortingEnabled(True)
		except:
			pass
		self.tableWidget1.scrollToTop()
		zeilen = len(res)
		self.labelVidGefunden.setText(str(zeilen) +self.trUtf8(" found"))
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
	# end of onSuchen
	
	def onClear(self):
		self.lineEditSuchen.clear()
		self.lineEditSuchen.setFocus()
		
	def onDateinamenUebernehmen(self):
		self.suchfeld.insertItem(0, self.lineEditSuchen.text())
		self.suchfeld.setCurrentIndex(0)
		self.suchfeld.setFocus()
		
	def onLoadStarted(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		
	def onLoadFinished(self, arg):
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		
	def onVideoSuchen(self):
		#Logik:
		#1. Suchen nach 'class="moviecount">'
		#2. dann bis zum nächsten Blank: dazwischen ist Anzahl Movies
		#3. Suchen nach "tr class"
		#4. dann Suchen nach '.htm">'
		#5. dann Suchen nach dem nächsten "<": dazwischen ist der Titel
		#6. weiter bei 3.
		
		text = str(self.webView.page().mainFrame().toHtml().toUtf8())
		anfang = text.find('class="moviecount">')
		ende = text.find(' ', anfang)
		anzahl = 0
		try:
			anzahl = int(text[anfang+19:ende])
		except:
			pass
		titel = []
		if anzahl:
			for i in xrange(anzahl):
				anfang = text.find("tr class", ende)
				anfang2 = text.find('.htm">', anfang)
				ende = text.find("<", anfang2)
				titel.append(text[anfang2+6:ende].strip().decode("utf-8"))
		if titel:
			self.video_anzeigen(titel)
			
	def onIAFDSeite(self):
		self.webView.load(QtCore.QUrl("http://www.iafd.com/"))
		
	def onDarstellerdatenAbholen(self):
		url = self.webView.url().toString()
		text = str(self.webView.page().mainFrame().toHtml().toUtf8())
		bilddialog = DarstellerdatenAnzeigen(app, url, text, self.verzeichnis_thumbs)
		fehler = False
		try:
			geschlecht = bilddialog.ethnic
		except:
			fehler = True
		if not fehler:
			bilddialog.exec_()
		self.suchfeld.setFocus()
		
	def onLinkClicked(self, url):
		self.webView.load(QtCore.QUrl(url))
		
	def onUrlChanged(self, url):
		self.statusBar.showMessage(str(url).strip("PyQt4.QtCore.QUrl(u'").rstrip("/')"))
		
	def onCopyintoClipboard(self):
		clipboard = QtGui.QApplication.clipboard()
		clipboard.setText(self.webView.selectedText(), mode=QtGui.QClipboard.Clipboard)
		
	def GetWebsite(self):
		if str(self.lineEditURL.text()).startswith("http://"):
			url = self.lineEditURL.text()
		else:
			url = "http://" + self.lineEditURL.text()
		self.webView.load(QtCore.QUrl(url))
		self.statusBar.showMessage(url)
		
	def onUrlVerwalten(self):
		if str(self.lineEditURL.text()):
			if str(self.lineEditURL.text()).startswith("http://"):
				url = self.lineEditURL.text()
			else:
				url = "http://" + self.lineEditURL.text()
		else:
			url = "http://www.iafd.com/"
		bookmarks = Bookmarks(url)
		bookmarks.exec_()
		neue_url = None
		try:
			neue_url = bookmarks.neue_url
		except:
			pass
		if neue_url:
			self.lineEditURL.setText(neue_url)
			self.lineEditURL.setFocus()
		    
	def onStatistikCS(self):
		self.tableWidgetStatistik.setSortingEnabled(False)
		self.tableWidgetStatistik.clear()
		self.tableWidgetStatistik.setRowCount(len(self.cumshots) + 1)
		self.tableWidgetStatistik.setColumnCount(2)
		self.tableWidgetStatistik.setAlternatingRowColors(True)
		j = -1
		gesamt = 0
		for i in self.cumshots.keys():
			zu_lesen = "select sum(cs" +i +") from pordb_vid" 
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			if res[0][0]:
				gesamt += res[0][0]
			newitem = QtGui.QTableWidgetItem(self.cumshots[i])
			j += 1
			self.tableWidgetStatistik.setItem(j, 0, newitem)
			newitem = QtGui.QTableWidgetItem()
			if res[0][0]:
				newitem.setData(0, QtCore.QVariant(int(res[0][0])))
			else:
				newitem.setData(0, QtCore.QVariant(0))
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, 1, newitem)
		newitem = QtGui.QTableWidgetItem(self.trUtf8("Summary"))
		j += 1
		self.tableWidgetStatistik.setItem(j, 0, newitem)
		newitem = QtGui.QTableWidgetItem()
		newitem.setData(0, QtCore.QVariant(int(gesamt)))
		newitem.setTextAlignment(QtCore.Qt.AlignRight)
		self.tableWidgetStatistik.setItem(j, 1, newitem)
		self.tableWidgetStatistik.resizeColumnsToContents()
		self.tableWidgetStatistik.resizeRowsToContents()
		self.tableWidgetStatistik.setSortingEnabled(True)
		self.tableWidgetStatistik.sortItems(1)
		self.suchfeld.setFocus()
		
	def onStatistikDarstellerW(self):
		try:
			anzahl = int(self.lineEditAnzahlW.text())
		except:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Quantity is not a number"))
			return
		zu_erfassen = "update pordb_vid_neu set partnerw = " +str(anzahl) 
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		self.onStatistikDarsteller("w", anzahl)
		
	def onStatistikDarstellerM(self):
		try:
			anzahl = int(self.lineEditAnzahlM.text())
		except:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Quantity is not a number"))
			return
		zu_erfassen = "update pordb_vid_neu set partnerm = " +str(anzahl) 
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		self.onStatistikDarsteller("m", anzahl)
		
	def onStatistikDarsteller(self, sex, anzahl):
		zu_lesen = "select darsteller, anzahl, partner, nation, geboren, filme from pordb_darsteller where sex = '" +sex +"' and partner >" +str(anzahl) +"order by partner, darsteller"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		self.tableWidgetStatistik.setSortingEnabled(False)
		self.tableWidgetStatistik.clear()
		self.tableWidgetStatistik.setRowCount(len(res))
		self.tableWidgetStatistik.setColumnCount(6)
		self.tableWidgetStatistik.setAlternatingRowColors(True)
		j = -1
		for i in res:
			newitem = QtGui.QTableWidgetItem(i[0])
			j += 1
			self.tableWidgetStatistik.setItem(j, 0, newitem)
			newitem = QtGui.QTableWidgetItem()
			newitem.setData(0, QtCore.QVariant(int(i[1])))
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, 1, newitem)
			newitem = QtGui.QTableWidgetItem()
			newitem.setData(0, QtCore.QVariant(int(i[2])))
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, 2, newitem)
			if i[3]:
				newitem = QtGui.QTableWidgetItem(i[3])
			else:
				newitem = QtGui.QTableWidgetItem("")
			self.tableWidgetStatistik.setItem(j, 3, newitem)
			try:
				geboren = (str(i[4])[0:10]).split("-")
				jahr = int(geboren[0])
				monat = int(geboren[1])
				tag = int(geboren[2])
				if jahr <> 1:
					alter = age((datetime.date(jahr, monat, tag)))
					newitem = QtGui.QTableWidgetItem(str(alter))
				else:
					newitem = QtGui.QTableWidgetItem()
			except:
				newitem = QtGui.QTableWidgetItem()
			self.tableWidgetStatistik.setItem(j, 4, newitem)
			newitem = QtGui.QTableWidgetItem()
			if i[5]:
				newitem.setData(0, QtCore.QVariant(int(i[5])))
			else:
				newitem.setData(0, QtCore.QVariant(int(0)))
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, 5, newitem)
		self.tableWidgetStatistik.setHorizontalHeaderLabels([self.trUtf8("Actor"), self.trUtf8("Quantity"), self.trUtf8("Partner"), self.trUtf8("Nation"), self.trUtf8("Age"), self.trUtf8("Movies")])
		self.tableWidgetStatistik.resizeColumnsToContents()
		self.tableWidgetStatistik.resizeRowsToContents()
		self.tableWidgetStatistik.setSortingEnabled(True)
		self.tableWidgetStatistik.sortItems(2, 1)
		self.tableWidgetStatistik.scrollToTop()
		self.suchfeld.setFocus()
		
	def onStatistikAnzahlClips(self):
		zu_lesen = "select count (*) from pordb_vid"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		try:
			QtGui.QMessageBox.information(self, "PorDB", self.trUtf8("Quantity of movies: ") +str(res[0][0]))
		except:
			pass
		self.suchfeld.setFocus()
		
	def onStatistikAnzahlClipsJahr(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_lesen = "select distinct original from pordb_vid"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		
		jahre = {}
		gesamt = 0
		for i in res:
			if i[0] and i[0].strip() and i[0].strip()[-1] == ")":
				original = i[0].strip()
				jahr = original[-5:-1]
				if jahr.isdigit():
					if jahr in jahre:
						jahre[jahr] = jahre[jahr] +1
					else:
						jahre[jahr] = 1
					gesamt += 1
					
		s = jahre.keys()
		if not s:
			app.restoreOverrideCursor()
			return
		s.sort()
		jahr_min = s[0]
		jahr_max = s[-1]
		jahre_titel = range(int(jahr_min), int(jahr_max) +1)
		j = -1
		for i in jahre_titel:
			j += 1
			jahre_titel[j] = str(i)

		datum_akt = str(time.localtime()[0]) + '-' + str(time.localtime()[1]) + '-' + str(time.localtime()[2])
		akt_jahr = datum_akt[0:4]
		
		self.tableWidgetStatistik.setSortingEnabled(False)
		self.tableWidgetStatistik.clear()
		self.tableWidgetStatistik.setRowCount(len(jahre_titel))
		self.tableWidgetStatistik.setColumnCount(2)
		self.tableWidgetStatistik.setAlternatingRowColors(True)
		j = -1
		datum_alt = "1900-01-01"
		gesamt = 0
		datum = []
		for i in jahre_titel:
			j += 1
			k = 0
			newitem = QtGui.QTableWidgetItem()
			newitem.setData(0, QtCore.QVariant(i))
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, k, newitem)
			k = 1
			newitem = QtGui.QTableWidgetItem()
			try:
				newitem.setData(0, QtCore.QVariant(jahre[i]))
			except:
				newitem.setData(0, 0)
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, k, newitem)
			try:
				gesamt += jahre[i]
			except:
				pass
		if datum_alt <> "1900-01-01":
			k += 1
			newitem = QtGui.QTableWidgetItem()
			newitem.setData(0, QtCore.QVariant(str(gesamt)))
			newitem.setTextAlignment(QtCore.Qt.AlignRight)
			self.tableWidgetStatistik.setItem(j, k, newitem)
		self.tableWidgetStatistik.setHorizontalHeaderLabels([self.trUtf8("Year"), self.trUtf8("Quantity")])
		self.tableWidgetStatistik.resizeColumnsToContents()
		self.tableWidgetStatistik.resizeRowsToContents()
		self.tableWidgetStatistik.setSortingEnabled(True)
		self.tableWidgetStatistik.sortItems(0)
		self.tableWidgetStatistik.scrollToBottom()
		
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		
	def onBackup(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		import tarfile
		# Backup database
		if self.checkBoxDatabase.isChecked():
			zu_lesen = "select * from information_schema.tables where table_schema = 'public' and table_name not like 'pga_%' and table_name like 'pordb%' order by table_name"
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			db_host="localhost"
			try:
				self.conn = psycopg2.connect(database=dbname, host=db_host)
			except Exception, e:
				message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Connection to database failed"))
				return
			self.cur = self.conn.cursor()
			for i in res:
				datei = file(self.verzeichnis +os.sep +i[2] +".txt", "w")
				try:
					self.cur.copy_to(datei, i[2], sep='|')
				except Exception, e:
					message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Copy to file failed"))
					return
				datei.close()
				
		# Backup picture directory
		if self.checkBoxPictures.isChecked():
			tar = tarfile.open(self.verzeichnis +os.sep +"archive.tar.gz", "w:gz")
			tar.add(self.verzeichnis_thumbs)
			tar.close()
			
			datei = open(self.verzeichnis +os.sep +"archive.tar.gz", "rb")
			partnum = 0
			while True:
				chunk = datei.read(100000000)
				if not chunk:
					break
				partnum += 1
				filename = os.path.join(self.verzeichnis_original, ("pordb_part%04d" % partnum))
				fileobj = open(filename, "wb")
				fileobj.write(chunk)
				fileobj.close()
			
			datei.close()
			os.remove(self.verzeichnis +os.sep +"archive.tar.gz")
		
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		message = QtGui.QMessageBox(self)
		message.setText(self.trUtf8("Backup in directory ") +self.verzeichnis + self.trUtf8(" created"))
		message.exec_()
		
	def onRestore(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		import tarfile
		
		# Restore the database
		db_host='localhost'
		try:
			self.conn = psycopg2.connect(database=dbname, host=db_host)
		except Exception, e:
			message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Connection to database failed"))
			return
		self.cur = self.conn.cursor()
		dateiliste = os.listdir(self.verzeichnis)
		dateien_gefunden = False
		for i in dateiliste:
			if i.startswith("pordb_") and i.endswith(".txt"):
				tabelle = i.rstrip(".txt")
				datei = file(self.verzeichnis +os.sep +i, "r")
				try:
					delete = "truncate " +tabelle +" CASCADE"
					self.cur.execute(delete)
					self.cur.copy_from(datei, tabelle, sep='|')
					dateien_gefunden = True
				except Exception, e:
					app.restoreOverrideCursor()
					message = QtGui.QMessageBox.critical(self, self.trUtf8("Error "), self.trUtf8("Copy from file " +i +" failed"))
					return
		self.conn.commit()

		# Restore the picture directory
		parts = os.listdir(self.verzeichnis)
		parts.sort()
		output = open(self.verzeichnis +os.sep +"archive.tar.gz", "wb")
		for filename in parts:
			if filename.startswith("pordb_part"):
				filepath = os.path.join(self.verzeichnis, filename)
				fileobj = open(filepath, "rb")
				while True:
					filebytes = fileobj.read(100000000)
					if not filebytes:
						break
					output.write(filebytes)
				fileobj.close()
		output.close()
		if os.path.isfile(self.verzeichnis +os.sep +"archive.tar.gz") and os.path.getsize(self.verzeichnis +os.sep +"archive.tar.gz") == 0:
			os.remove(self.verzeichnis +os.sep +"archive.tar.gz")
		if os.path.isfile(self.verzeichnis +os.sep +"archive.tar.gz"):
			tar = tarfile.open(self.verzeichnis +os.sep +"archive.tar.gz")
			try:
				tar.extractall(path=self.verzeichnis)
			except:
				self.suchfeld.setFocus()
				message = QtGui.QMessageBox(self)
				message.setText(self.trUtf8("Backup in directory ") +self.verzeichnis + self.trUtf8(" failed. In most cases there is a file with an invalid creation/change date."))
				message.exec_()
				app.restoreOverrideCursor()
				return
			tar.close()
		else:
			self.suchfeld.setFocus()
			app.restoreOverrideCursor()
			message = QtGui.QMessageBox(self)
			message.setText(self.trUtf8("Backup in directory ") +self.verzeichnis + self.trUtf8(" failed. No backup files found."))
			message.exec_()
			return
		#os.remove(self.verzeichnis +os.sep +"thumbs")

		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		message = QtGui.QMessageBox(self)
		message.setText(self.trUtf8("Backup in directory ") +self.verzeichnis + self.trUtf8(" restored. You can now copy the complete directory to its origin place."))
		message.exec_()
		
		
	def onWartung(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		befehl = "/usr/bin/vacuumdb --analyze por"
		os.system(befehl)
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		message = QtGui.QMessageBox(self)
		message.setText(self.trUtf8("Maintenance executed"))
		message.exec_()
		
	def device_fuellen(self):
		zu_lesen = "select * from pordb_mpg_verzeichnisse order by dir"
		lese_func = DBLesen(self, zu_lesen)
		res = DBLesen.get_data(lese_func)
		self.comboBoxDevice.clear()
		if res:
			for i in res:
				self.comboBoxDevice.addItem(i[0])
		self.comboBoxDevice.setCurrentIndex(-1)
		self.suchfeld.setFocus()
		
	def onDevicesVerwalten(self):
		bilddialog = Devices(self.device_fuellen)
		bilddialog.exec_()
		self.suchfeld.setFocus()
			
	def onStartScan(self):
		if not self.comboBoxDevice.currentText():
			message = QtGui.QMessageBox(self)
			message.setText(self.trUtf8("Select device"))
			message.exec_()
			return
			
		self.verzeichnis_tools = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8("Select directory"), "/")
		if self.verzeichnis_tools:
			dateien = os.listdir(self.verzeichnis_tools)
		else:
			return
		for i in dateien:
			if len(i) > 256:
				message = QtGui.QMessageBox(self)
				message.setText(self.trUtf8("Error, filename ") +i +self.trUtf8(" to long"))
				message.exec_()
				return
				
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		res_alle = []
		zu_erfassen = []
		for i in dateien:
			zu_lesen = "SELECT * from pordb_mpg_katalog where file = '" + i.replace("'", "''") + "' or groesse = " + str(os.path.getsize(self.verzeichnis_tools +os.sep +i.strip()))
			lese_func = DBLesen(self, zu_lesen)
			res = DBLesen.get_data(lese_func)
			in_datenbank = True
			for j in res:
				if j[0].strip() == str(self.comboBoxDevice.currentText()).strip() and j[1].strip() == os.path.basename(str(self.verzeichnis_tools)) and j[2].strip() == i.replace("'", "''").strip():
					in_datenbank = False
			
			if in_datenbank:
				for j in res:
					# put only in duplicate list, when actual directory is another one than that in database
					if j[1].strip() <> os.path.basename(str(self.verzeichnis_tools).strip()): 
						a = list(j)
						a.append(i)
						a.append(long(os.path.getsize(self.verzeichnis_tools +os.sep +i.strip())))
						res_alle.append(a)
				try:
					zu_erfassen.append("INSERT into pordb_mpg_katalog VALUES ('" +str(self.comboBoxDevice.currentText()) +"', '" +os.path.basename(str(self.verzeichnis_tools)) +"', '" +i.replace("'", "''") +"', '" +" " +"', '" +str(os.path.getsize(self.verzeichnis_tools +os.sep +i.replace("'", "''"))) +"')")
				except:
					message = QtGui.QMessageBox(self)
					message.setText(self.trUtf8("Error, filename '") +i +self.trUtf8("' is wrong (special characters)"))
					message.exec_()
					app.restoreOverrideCursor()
					return
						
		update_func = DBUpdate(self, zu_erfassen)
		DBUpdate.update_data(update_func)
		
		# jetzt die Dubletten in Tabelle ausgeben
		self.row = 0
		self.column = 0
		self.tableWidgetDubletten.clear()
		self.tableWidgetDubletten.setAlternatingRowColors(True)
		self.tableWidgetDubletten.setColumnCount(7)
		self.tableWidgetDubletten.setRowCount(len(res_alle))
		counter = 0
		for j in res_alle:
			# Checkbox
			newitem = QtGui.QTableWidgetItem()
			newitem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
			if self.verzeichnis_tools +os.sep +j[5].strip() == j[2].strip() and str(j[4]) == str(os.path.getsize(self.verzeichnis_tools +os.sep +j[5].strip())):
				newitem.setCheckState(QtCore.Qt.Checked)
				counter += 1
			else:
				newitem.setCheckState(QtCore.Qt.Unchecked)
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.column += 1
			newitem = QtGui.QTableWidgetItem(j[2].strip()) 	# Filename
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.column += 1
			newitem = QtGui.QTableWidgetItem(j[0].strip())		# Device
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.column += 1
			newitem = QtGui.QTableWidgetItem(j[1].strip())		# Directory
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.column += 1
			newitem = QtGui.QTableWidgetItem(str(j[4]))	# Size in database
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.column += 1
			newitem = QtGui.QTableWidgetItem(j[5].strip()) 	# new Filename
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.column += 1
			newitem = QtGui.QTableWidgetItem(str(j[6]))	# Size of new file
			self.tableWidgetDubletten.setItem(self.row, self.column, newitem)
			self.row += 1
			self.column = 0
			
		self.tableWidgetDubletten.setHorizontalHeaderLabels([self.trUtf8("delete"), self.trUtf8("File in database"), self.trUtf8("Device"), self.trUtf8("Directory"), self.trUtf8("Size in database"), self.trUtf8("new file"), self.trUtf8("Size of new file")])
		self.tableWidgetDubletten.resizeColumnsToContents()
		self.tableWidgetDubletten.resizeRowsToContents()
		
		message = str(len(zu_erfassen)) + self.trUtf8(" File(s) collected")
		if len(res_alle) > 0:
			self.pushButtonDeleteDuplicates.setEnabled(True)
			self.pushButtonDeselect.setEnabled(True)
			if counter > 0:
				message += ", " +str(counter) +self.trUtf8(" Duplicate(s) found") 
			else:
				message += ", " +str(len(res_alle)) +self.trUtf8(" Duplicate(s) found, but some of them only in relation to file size")
		
		self.statusBar.showMessage(message)
		
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		
	def onDeleteDuplicates(self):
		app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		zu_erfassen = []
		counter = 0
		for i in xrange(self.tableWidgetDubletten.rowCount()):
			if self.tableWidgetDubletten.item(i, 0).checkState():
				zu_erfassen.append("delete from pordb_mpg_katalog where device = '" +str(self.comboBoxDevice.currentText()).strip() +"' and dir = '" +os.path.basename(str(self.verzeichnis_tools)) +"' and file = '" +str(self.tableWidgetDubletten.item(i, 5).text()).strip() +"'")
				try:
					os.remove(self.verzeichnis_tools +os.sep +str(self.tableWidgetDubletten.item(i, 5).text()).strip())
					counter += 1
				except:
					pass
		if counter > 0:
			update_func = DBUpdate(self, zu_erfassen)
			DBUpdate.update_data(update_func)
			message = str(counter) +self.trUtf8(" File(s) deleted")
		else:
			message = ""
		self.statusBar.showMessage(message)
		app.restoreOverrideCursor()
		self.suchfeld.setFocus()
		
	def onDeselect(self):
		for i in xrange(self.tableWidgetDubletten.rowCount()):
			self.tableWidgetDubletten.item(i, 0).setCheckState(QtCore.Qt.Unchecked)
		self.suchfeld.setFocus()
		
app = QtGui.QApplication(sys.argv)
locale = QtCore.QLocale.system().name()
#locale = "en_EN"
appTranslator = QtCore.QTranslator()
if appTranslator.load("pordb_" + locale, os.getcwd()):
	app.installTranslator(appTranslator)
dialog = MeinDialog()
dialog.show()
sys.exit(app.exec_())
