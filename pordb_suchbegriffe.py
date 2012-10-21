# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_suchbegriffe.ui'
#
# Created: Tue Mar 13 22:32:21 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Suchbegriffedialog(object):
    def setupUi(self, Suchbegriffedialog):
        Suchbegriffedialog.setObjectName("Suchbegriffedialog")
        Suchbegriffedialog.resize(735, 905)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pypordb/8027068_splash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Suchbegriffedialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Suchbegriffedialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(Suchbegriffedialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidgetSuche = QtGui.QTableWidget(self.frame)
        self.tableWidgetSuche.setObjectName("tableWidgetSuche")
        self.tableWidgetSuche.setColumnCount(2)
        self.tableWidgetSuche.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetSuche.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetSuche.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_2.addWidget(self.tableWidgetSuche)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonLandSpeichern = QtGui.QPushButton(Suchbegriffedialog)
        self.pushButtonLandSpeichern.setObjectName("pushButtonLandSpeichern")
        self.horizontalLayout.addWidget(self.pushButtonLandSpeichern)
        self.pushButtonLandAbbrechen = QtGui.QPushButton(Suchbegriffedialog)
        self.pushButtonLandAbbrechen.setObjectName("pushButtonLandAbbrechen")
        self.horizontalLayout.addWidget(self.pushButtonLandAbbrechen)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Suchbegriffedialog)
        QtCore.QMetaObject.connectSlotsByName(Suchbegriffedialog)

    def retranslateUi(self, Suchbegriffedialog):
        Suchbegriffedialog.setWindowTitle(QtGui.QApplication.translate("Suchbegriffedialog", "Edit search items", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetSuche.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Suchbegriffedialog", "search item", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetSuche.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Suchbegriffedialog", "Alternative", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLandSpeichern.setText(QtGui.QApplication.translate("Suchbegriffedialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLandAbbrechen.setText(QtGui.QApplication.translate("Suchbegriffedialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

