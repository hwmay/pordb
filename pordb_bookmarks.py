# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_bookmarks.ui'
#
# Created: Tue Mar 13 22:32:22 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(675, 622)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pypordb/8027068_splash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonSpeichern = QtGui.QPushButton(self.frame)
        self.pushButtonSpeichern.setObjectName("pushButtonSpeichern")
        self.horizontalLayout.addWidget(self.pushButtonSpeichern)
        self.pushButtonAnzeigen = QtGui.QPushButton(self.frame)
        self.pushButtonAnzeigen.setObjectName("pushButtonAnzeigen")
        self.horizontalLayout.addWidget(self.pushButtonAnzeigen)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.pushButtonLoeschen = QtGui.QPushButton(self.frame)
        self.pushButtonLoeschen.setObjectName("pushButtonLoeschen")
        self.horizontalLayout_2.addWidget(self.pushButtonLoeschen)
        self.verticalLayout.addWidget(self.frame)
        self.tableWidgetBookmarks = QtGui.QTableWidget(Dialog)
        self.tableWidgetBookmarks.setObjectName("tableWidgetBookmarks")
        self.tableWidgetBookmarks.setColumnCount(0)
        self.tableWidgetBookmarks.setRowCount(0)
        self.tableWidgetBookmarks.horizontalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.tableWidgetBookmarks)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSpeichern.setText(QtGui.QApplication.translate("Dialog", "Save actual site in bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAnzeigen.setText(QtGui.QApplication.translate("Dialog", "Show selected site", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLoeschen.setText(QtGui.QApplication.translate("Dialog", "Delete site from bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetBookmarks.setSortingEnabled(True)

