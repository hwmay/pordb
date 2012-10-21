# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_land.ui'
#
# Created: Tue Mar 13 22:32:21 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Landdialog(object):
    def setupUi(self, Landdialog):
        Landdialog.setObjectName("Landdialog")
        Landdialog.resize(735, 905)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pypordb/8027068_splash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Landdialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Landdialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(Landdialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidgetLaender = QtGui.QTableWidget(self.frame)
        self.tableWidgetLaender.setObjectName("tableWidgetLaender")
        self.tableWidgetLaender.setColumnCount(4)
        self.tableWidgetLaender.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetLaender.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetLaender.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetLaender.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetLaender.setHorizontalHeaderItem(3, item)
        self.horizontalLayout_2.addWidget(self.tableWidgetLaender)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonLandSpeichern = QtGui.QPushButton(Landdialog)
        self.pushButtonLandSpeichern.setObjectName("pushButtonLandSpeichern")
        self.horizontalLayout.addWidget(self.pushButtonLandSpeichern)
        self.pushButtonLandAbbrechen = QtGui.QPushButton(Landdialog)
        self.pushButtonLandAbbrechen.setObjectName("pushButtonLandAbbrechen")
        self.horizontalLayout.addWidget(self.pushButtonLandAbbrechen)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Landdialog)
        QtCore.QMetaObject.connectSlotsByName(Landdialog)

    def retranslateUi(self, Landdialog):
        Landdialog.setWindowTitle(QtGui.QApplication.translate("Landdialog", "Edit table of countries", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetLaender.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Landdialog", "ISO Code", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetLaender.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Landdialog", "Country", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetLaender.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Landdialog", "active", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetLaender.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Landdialog", "Nationality", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLandSpeichern.setText(QtGui.QApplication.translate("Landdialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLandAbbrechen.setText(QtGui.QApplication.translate("Landdialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

