# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_darsteller_suchen.ui'
#
# Created: Mon Nov 18 23:39:00 2013
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

class Ui_DarstellerSuche(object):
    def setupUi(self, DarstellerSuche):
        DarstellerSuche.setObjectName(_fromUtf8("DarstellerSuche"))
        DarstellerSuche.resize(867, 336)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pypordb/8027068_splash.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DarstellerSuche.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(DarstellerSuche)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(DarstellerSuche)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBoxDarstellerSucheGeschlecht = QtGui.QComboBox(self.groupBox)
        self.comboBoxDarstellerSucheGeschlecht.setObjectName(_fromUtf8("comboBoxDarstellerSucheGeschlecht"))
        self.comboBoxDarstellerSucheGeschlecht.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheGeschlecht.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxDarstellerSucheGeschlecht, 1, 1, 1, 1)
        self.dateEditDarstellerSucheAb = QtGui.QDateEdit(self.groupBox)
        self.dateEditDarstellerSucheAb.setMinimumDate(QtCore.QDate(1752, 9, 14))
        self.dateEditDarstellerSucheAb.setCalendarPopup(True)
        self.dateEditDarstellerSucheAb.setObjectName(_fromUtf8("dateEditDarstellerSucheAb"))
        self.gridLayout.addWidget(self.dateEditDarstellerSucheAb, 3, 1, 1, 2)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(661, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 2)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.comboBoxDarstellerSucheNation = QtGui.QComboBox(self.groupBox)
        self.comboBoxDarstellerSucheNation.setObjectName(_fromUtf8("comboBoxDarstellerSucheNation"))
        self.gridLayout.addWidget(self.comboBoxDarstellerSucheNation, 6, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(631, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.comboBoxDarstellerSucheEthnic = QtGui.QComboBox(self.groupBox)
        self.comboBoxDarstellerSucheEthnic.setObjectName(_fromUtf8("comboBoxDarstellerSucheEthnic"))
        self.comboBoxDarstellerSucheEthnic.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheEthnic.setItemText(0, _fromUtf8(""))
        self.comboBoxDarstellerSucheEthnic.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheEthnic.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheEthnic.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheEthnic.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxDarstellerSucheEthnic, 8, 1, 1, 1)
        self.lineEditDarstellerSuche = QtGui.QLineEdit(self.groupBox)
        self.lineEditDarstellerSuche.setObjectName(_fromUtf8("lineEditDarstellerSuche"))
        self.gridLayout.addWidget(self.lineEditDarstellerSuche, 0, 1, 1, 3)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(631, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 3, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)
        self.comboBoxDarstellerSucheTattoo = QtGui.QComboBox(self.groupBox)
        self.comboBoxDarstellerSucheTattoo.setObjectName(_fromUtf8("comboBoxDarstellerSucheTattoo"))
        self.comboBoxDarstellerSucheTattoo.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheTattoo.setItemText(0, _fromUtf8(""))
        self.comboBoxDarstellerSucheTattoo.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheTattoo.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxDarstellerSucheTattoo, 7, 1, 1, 1)
        self.lineEditDarstellerSucheTattoo = QtGui.QLineEdit(self.groupBox)
        self.lineEditDarstellerSucheTattoo.setObjectName(_fromUtf8("lineEditDarstellerSucheTattoo"))
        self.gridLayout.addWidget(self.lineEditDarstellerSucheTattoo, 7, 2, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(661, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 5, 2, 1, 2)
        spacerItem4 = QtGui.QSpacerItem(491, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 8, 2, 1, 2)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.comboBoxDarstellerSucheHaar = QtGui.QComboBox(self.groupBox)
        self.comboBoxDarstellerSucheHaar.setObjectName(_fromUtf8("comboBoxDarstellerSucheHaar"))
        self.comboBoxDarstellerSucheHaar.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheHaar.setItemText(0, _fromUtf8(""))
        self.comboBoxDarstellerSucheHaar.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheHaar.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheHaar.addItem(_fromUtf8(""))
        self.comboBoxDarstellerSucheHaar.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxDarstellerSucheHaar, 5, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dateEditDarstellerSucheBis = QtGui.QDateEdit(self.groupBox)
        self.dateEditDarstellerSucheBis.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEditDarstellerSucheBis.setCalendarPopup(True)
        self.dateEditDarstellerSucheBis.setObjectName(_fromUtf8("dateEditDarstellerSucheBis"))
        self.gridLayout.addWidget(self.dateEditDarstellerSucheBis, 4, 1, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditActor1 = QtGui.QLineEdit(self.groupBox)
        self.lineEditActor1.setObjectName(_fromUtf8("lineEditActor1"))
        self.horizontalLayout.addWidget(self.lineEditActor1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout.addWidget(self.label_10)
        self.lineEditActor2 = QtGui.QLineEdit(self.groupBox)
        self.lineEditActor2.setObjectName(_fromUtf8("lineEditActor2"))
        self.horizontalLayout.addWidget(self.lineEditActor2)
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout.addWidget(self.label_11)
        self.lineEditActor3 = QtGui.QLineEdit(self.groupBox)
        self.lineEditActor3.setObjectName(_fromUtf8("lineEditActor3"))
        self.horizontalLayout.addWidget(self.lineEditActor3)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 3)
        self.verticalLayout.addWidget(self.groupBox)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.pushButtonSuchen = QtGui.QPushButton(DarstellerSuche)
        self.pushButtonSuchen.setObjectName(_fromUtf8("pushButtonSuchen"))
        self.hboxlayout.addWidget(self.pushButtonSuchen)
        self.pushButtonRefresh = QtGui.QPushButton(DarstellerSuche)
        self.pushButtonRefresh.setObjectName(_fromUtf8("pushButtonRefresh"))
        self.hboxlayout.addWidget(self.pushButtonRefresh)
        self.pushButtonCancel = QtGui.QPushButton(DarstellerSuche)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.hboxlayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(DarstellerSuche)
        QtCore.QMetaObject.connectSlotsByName(DarstellerSuche)
        DarstellerSuche.setTabOrder(self.lineEditDarstellerSuche, self.comboBoxDarstellerSucheNation)
        DarstellerSuche.setTabOrder(self.comboBoxDarstellerSucheNation, self.pushButtonSuchen)
        DarstellerSuche.setTabOrder(self.pushButtonSuchen, self.pushButtonRefresh)
        DarstellerSuche.setTabOrder(self.pushButtonRefresh, self.pushButtonCancel)

    def retranslateUi(self, DarstellerSuche):
        DarstellerSuche.setWindowTitle(_translate("DarstellerSuche", "Search actor", None))
        self.groupBox.setTitle(_translate("DarstellerSuche", "Search criteria", None))
        self.label_2.setText(_translate("DarstellerSuche", "Gender", None))
        self.comboBoxDarstellerSucheGeschlecht.setItemText(0, _translate("DarstellerSuche", "w", None))
        self.comboBoxDarstellerSucheGeschlecht.setItemText(1, _translate("DarstellerSuche", "m", None))
        self.dateEditDarstellerSucheAb.setWhatsThis(_translate("DarstellerSuche", "Date when the actor has been added to the PorDB database", None))
        self.dateEditDarstellerSucheAb.setDisplayFormat(_translate("DarstellerSuche", "dd.MM.yyyy", None))
        self.label_9.setText(_translate("DarstellerSuche", "Has acted with", None))
        self.label_3.setText(_translate("DarstellerSuche", "Date from", None))
        self.comboBoxDarstellerSucheEthnic.setItemText(1, _translate("DarstellerSuche", "w", None))
        self.comboBoxDarstellerSucheEthnic.setItemText(2, _translate("DarstellerSuche", "a", None))
        self.comboBoxDarstellerSucheEthnic.setItemText(3, _translate("DarstellerSuche", "s", None))
        self.comboBoxDarstellerSucheEthnic.setItemText(4, _translate("DarstellerSuche", "l", None))
        self.label_5.setText(_translate("DarstellerSuche", "Hair color", None))
        self.label_4.setText(_translate("DarstellerSuche", "Date to", None))
        self.label_7.setText(_translate("DarstellerSuche", "Tattoo", None))
        self.comboBoxDarstellerSucheTattoo.setItemText(1, _translate("DarstellerSuche", "yes", None))
        self.comboBoxDarstellerSucheTattoo.setItemText(2, _translate("DarstellerSuche", "no", None))
        self.label_8.setText(_translate("DarstellerSuche", "Ethnic", None))
        self.label_6.setText(_translate("DarstellerSuche", "Nation", None))
        self.comboBoxDarstellerSucheHaar.setItemText(1, _translate("DarstellerSuche", "bl", None))
        self.comboBoxDarstellerSucheHaar.setItemText(2, _translate("DarstellerSuche", "br", None))
        self.comboBoxDarstellerSucheHaar.setItemText(3, _translate("DarstellerSuche", "r", None))
        self.comboBoxDarstellerSucheHaar.setItemText(4, _translate("DarstellerSuche", "s", None))
        self.label.setText(_translate("DarstellerSuche", "Name", None))
        self.dateEditDarstellerSucheBis.setWhatsThis(_translate("DarstellerSuche", "Date when the actor has been added to the PorDB database", None))
        self.dateEditDarstellerSucheBis.setDisplayFormat(_translate("DarstellerSuche", "dd.MM.yyyy", None))
        self.label_10.setText(_translate("DarstellerSuche", "and", None))
        self.label_11.setText(_translate("DarstellerSuche", "and", None))
        self.pushButtonSuchen.setText(_translate("DarstellerSuche", "Search", None))
        self.pushButtonSuchen.setShortcut(_translate("DarstellerSuche", "Enter", None))
        self.pushButtonRefresh.setText(_translate("DarstellerSuche", "Clear all search fields, alt+L", None))
        self.pushButtonRefresh.setShortcut(_translate("DarstellerSuche", "Alt+L", None))
        self.pushButtonCancel.setText(_translate("DarstellerSuche", "Cancel", None))

