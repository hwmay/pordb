# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_bookmarks.ui'
#
# Created: Sat Nov  2 20:03:49 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(675, 622)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pypordb/8027068_splash.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.horizontalLayout_3 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonSpeichern = QtGui.QPushButton(self.frame)
        self.pushButtonSpeichern.setObjectName(_fromUtf8("pushButtonSpeichern"))
        self.horizontalLayout.addWidget(self.pushButtonSpeichern)
        self.pushButtonAnzeigen = QtGui.QPushButton(self.frame)
        self.pushButtonAnzeigen.setObjectName(_fromUtf8("pushButtonAnzeigen"))
        self.horizontalLayout.addWidget(self.pushButtonAnzeigen)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.pushButtonLoeschen = QtGui.QPushButton(self.frame)
        self.pushButtonLoeschen.setObjectName(_fromUtf8("pushButtonLoeschen"))
        self.horizontalLayout_2.addWidget(self.pushButtonLoeschen)
        self.verticalLayout.addWidget(self.frame)
        self.tableWidgetBookmarks = QtGui.QTableWidget(Dialog)
        self.tableWidgetBookmarks.setObjectName(_fromUtf8("tableWidgetBookmarks"))
        self.tableWidgetBookmarks.setColumnCount(0)
        self.tableWidgetBookmarks.setRowCount(0)
        self.tableWidgetBookmarks.horizontalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.tableWidgetBookmarks)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Bookmarks", None))
        self.pushButtonSpeichern.setText(_translate("Dialog", "Save actual site in bookmarks", None))
        self.pushButtonAnzeigen.setText(_translate("Dialog", "Show selected site", None))
        self.pushButtonLoeschen.setText(_translate("Dialog", "Delete site from bookmarks", None))
        self.tableWidgetBookmarks.setSortingEnabled(True)

