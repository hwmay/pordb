# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from pordb_show_iafd_data import Ui_Dialog as pordb_show_iafd_data
from pypordb_dblesen import DBLesen
import os

class ShowIafdData(QtGui.QDialog, pordb_show_iafd_data):
	def __init__(self, verzeichnis, video):
		
		QtGui.QDialog.__init__(self)
		self.setupUi(self)
		
		self.verzeichnis = verzeichnis
		self.video = video
		
		self.connect(self.pushButtonCancel, QtCore.SIGNAL("clicked()"), self.close)
		self.connect(self.pushButtonOK, QtCore.SIGNAL("clicked()"), self.accept)
		
		self.imagesize = 200
		self.complete_size = QtCore.QSize(self.imagesize, self.imagesize)
		self.verzeichnis_thumbs = os.path.expanduser("~") +os.sep +"thumbs_sammlung"
		
		settings = QtCore.QSettings()
		window_size = settings.value("ShowIafdData/Size", QtCore.QVariant(QtCore.QSize(600, 500))).toSize()
		self.resize(window_size)
		window_position = settings.value("ShowIafdData/Position", QtCore.QVariant(QtCore.QPoint(0, 0))).toPoint()
		self.move(window_position)
		
		self.graphicsView.setAlignment(QtCore.Qt.AlignLeft)
		self.scene = QtGui.QGraphicsScene()
		self.left_margin = 20
		
		x_pos = self.left_margin
		y_pos = 0
		font = QtGui.QFont()
		
		# get imagefiles from working directory
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
		
		# set imagefiles from working directory
		if dateiliste_bereinigt:
			textitem = QtGui.QGraphicsTextItem(self.trUtf8("Clips to add:"))
			font.setPointSize(16)
			font.setWeight(75)
			font.setBold(True)
			textitem.setFont(font)
			textitem.setPos(0, y_pos)
			self.scene.addItem(textitem)
			y_pos += 30
			max_height = 0
			for i in dateiliste_bereinigt:
				bilddatei = self.verzeichnis + os.sep + i
				pixmap = QtGui.QPixmap(bilddatei).scaled(QtCore.QSize(self.complete_size),QtCore.Qt.KeepAspectRatio)
				if pixmap.height() > max_height:
					max_height = pixmap.height()
				pixmapitem = QtGui.QGraphicsPixmapItem(pixmap)
				pixmapitem.setPos(0, 20)
				textitem = QtGui.QGraphicsTextItem(i)
				itemgroup = self.scene.createItemGroup([textitem, pixmapitem])
				itemgroup.setPos(x_pos, y_pos)
				itemgroup.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
				x_pos += self.imagesize + 20
			x_pos = self.left_margin
			y_pos += max_height + 50
		
		# set original title
		font.setBold(True)
		textitem = QtGui.QGraphicsTextItem(self.video[0])
		textitem.setPos(0, y_pos)
		textitem.setFont(font)
		self.scene.addItem(textitem)
		y_pos += 40
		
		# set alternate titles
		for i, wert in enumerate(self.video[1]): 
			textitem = QtGui.QGraphicsTextItem(wert)
			textitem.setPos(x_pos, y_pos)
			self.scene.addItem(textitem)
			y_pos += 30
			
		# set scene and actors
		for i, wert in enumerate(self.video[2]): 
			for j, wert1 in enumerate(wert):
				darsteller_liste = wert1.split(", ")
				image_shown = False
				max_height = 0
				for k, wert2 in enumerate(darsteller_liste):
					textitem = QtGui.QGraphicsTextItem(wert2)
					if wert1.startswith("Scene "):
						font.setBold(True)
						textitem.setFont(font)
						textitem.setPos(x_pos, y_pos)
						self.scene.addItem(textitem)
						y_pos += 30
					else:
						zu_lesen = "SELECT * from pordb_darsteller where darsteller = '" +wert2.replace("'", "''").title() +"'"
						lese_func = DBLesen(self, zu_lesen)
						res = DBLesen.get_data(lese_func)
						if res:
							bilddatei = self.verzeichnis_thumbs +os.sep +"darsteller_" +res[0][1] +os.sep +res[0][0].lower().strip().replace(" ", "_").replace("''", "_apostroph_") +".jpg"
							if os.path.exists(bilddatei):
								pixmap = QtGui.QPixmap(bilddatei).scaled(QtCore.QSize(self.complete_size),QtCore.Qt.KeepAspectRatio)
							else:
								pixmap = QtGui.QPixmap(self.verzeichnis_thumbs +os.sep +"nichtvorhanden" +os.sep +"nicht_vorhanden.jpg").scaled(QtCore.QSize(self.complete_size),QtCore.Qt.KeepAspectRatio)
						else:
							pixmap = QtGui.QPixmap(self.verzeichnis_thumbs +os.sep +"nichtvorhanden" +os.sep +"nicht_vorhanden.jpg").scaled(QtCore.QSize(self.complete_size),QtCore.Qt.KeepAspectRatio)
						if pixmap.height() > max_height:
							max_height = pixmap.height()
						pixmapitem = QtGui.QGraphicsPixmapItem(pixmap)
						pixmapitem.setPos(0, 20)
						itemgroup = self.scene.createItemGroup([textitem, pixmapitem])
						itemgroup.setPos(x_pos, y_pos)
						itemgroup.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
						x_pos += self.imagesize + 20
						image_shown = True
				x_pos = self.left_margin
				if image_shown:
					y_pos += max_height + 20
			
		self.graphicsView.setScene(self.scene)
		self.graphicsView.centerOn(0, 0)
		
	def accept(self):
		self.close()
		
	def closeEvent(self, event):
		settings = QtCore.QSettings()
		settings.setValue("ShowIafdData/Size", QtCore.QVariant(self.size()))
		settings.setValue("ShowIafdData/Position", QtCore.QVariant(self.pos()))
