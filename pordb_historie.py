# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_historie.ui'
#
# Created: Tue Mar 13 22:32:22 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(903, 754)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pypordb/8027068_splash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidgetHistory = QtGui.QTableWidget(Dialog)
        self.tableWidgetHistory.setObjectName("tableWidgetHistory")
        self.tableWidgetHistory.setColumnCount(3)
        self.tableWidgetHistory.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetHistory.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetHistory.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetHistory.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tableWidgetHistory)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(668, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonGo = QtGui.QPushButton(Dialog)
        self.pushButtonGo.setObjectName("pushButtonGo")
        self.horizontalLayout.addWidget(self.pushButtonGo)
        self.pushButtonAbbrechen = QtGui.QPushButton(Dialog)
        self.pushButtonAbbrechen.setObjectName("pushButtonAbbrechen")
        self.horizontalLayout.addWidget(self.pushButtonAbbrechen)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "History", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetHistory.setSortingEnabled(True)
        self.tableWidgetHistory.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetHistory.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetHistory.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Dialog", "Timestamp", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGo.setText(QtGui.QApplication.translate("Dialog", "Execute", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAbbrechen.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

