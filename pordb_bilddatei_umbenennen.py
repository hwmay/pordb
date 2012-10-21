# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_bilddatei_umbenennen.ui'
#
# Created: Tue Mar 13 22:32:20 2012
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1035, 472)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pypordb/8027068_splash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_4 = QtGui.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetDateinamen = QtGui.QListWidget(self.groupBox)
        self.listWidgetDateinamen.setObjectName("listWidgetDateinamen")
        self.gridLayout.addWidget(self.listWidgetDateinamen, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEditDateiname = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditDateiname.setObjectName("lineEditDateiname")
        self.gridLayout_2.addWidget(self.lineEditDateiname, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.pushButtonUmbenennen = QtGui.QPushButton(Dialog)
        self.pushButtonUmbenennen.setObjectName("pushButtonUmbenennen")
        self.gridLayout_3.addWidget(self.pushButtonUmbenennen, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 2, 2)
        self.labelDateiname = QtGui.QLabel(Dialog)
        self.labelDateiname.setText("")
        self.labelDateiname.setObjectName("labelDateiname")
        self.gridLayout_4.addWidget(self.labelDateiname, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edit filename", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Filename already exists or has more than 50 characters or has an apostrophe", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Similar files in directory", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "New filename", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUmbenennen.setText(QtGui.QApplication.translate("Dialog", "Rename file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUmbenennen.setShortcut(QtGui.QApplication.translate("Dialog", "Return", None, QtGui.QApplication.UnicodeUTF8))

