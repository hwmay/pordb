# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pordb_neu.ui'
#
# Created: Mon Dec 24 23:56:20 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1107, 516)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pypordb/8027068_splash.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_1 = QtGui.QLabel(Dialog)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.lineEditNeuTitel = QtGui.QLineEdit(Dialog)
        self.lineEditNeuTitel.setObjectName(_fromUtf8("lineEditNeuTitel"))
        self.gridLayout.addWidget(self.lineEditNeuTitel, 0, 1, 1, 1)
        self.labelTitel = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(86)
        sizePolicy.setVerticalStretch(18)
        sizePolicy.setHeightForWidth(self.labelTitel.sizePolicy().hasHeightForWidth())
        self.labelTitel.setSizePolicy(sizePolicy)
        self.labelTitel.setMinimumSize(QtCore.QSize(86, 18))
        self.labelTitel.setText(_fromUtf8(""))
        self.labelTitel.setObjectName(_fromUtf8("labelTitel"))
        self.gridLayout.addWidget(self.labelTitel, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEditNeuDarsteller = QtGui.QLineEdit(Dialog)
        self.lineEditNeuDarsteller.setToolTip(_fromUtf8(""))
        self.lineEditNeuDarsteller.setObjectName(_fromUtf8("lineEditNeuDarsteller"))
        self.gridLayout.addWidget(self.lineEditNeuDarsteller, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEditNeuCD = QtGui.QLineEdit(Dialog)
        self.lineEditNeuCD.setObjectName(_fromUtf8("lineEditNeuCD"))
        self.gridLayout.addWidget(self.lineEditNeuCD, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEditNeuBild = QtGui.QLineEdit(Dialog)
        self.lineEditNeuBild.setObjectName(_fromUtf8("lineEditNeuBild"))
        self.gridLayout.addWidget(self.lineEditNeuBild, 3, 1, 1, 1)
        self.labelBild = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(86)
        sizePolicy.setVerticalStretch(18)
        sizePolicy.setHeightForWidth(self.labelBild.sizePolicy().hasHeightForWidth())
        self.labelBild.setSizePolicy(sizePolicy)
        self.labelBild.setMinimumSize(QtCore.QSize(86, 18))
        self.labelBild.setText(_fromUtf8(""))
        self.labelBild.setObjectName(_fromUtf8("labelBild"))
        self.gridLayout.addWidget(self.labelBild, 3, 3, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.lineEditNeuOriginal = QtGui.QLineEdit(Dialog)
        self.lineEditNeuOriginal.setObjectName(_fromUtf8("lineEditNeuOriginal"))
        self.gridLayout.addWidget(self.lineEditNeuOriginal, 4, 1, 1, 1)
        self.pushButtonOriginalAlt = QtGui.QPushButton(Dialog)
        self.pushButtonOriginalAlt.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pypordb/appointment-recurring.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButtonOriginalAlt.setIcon(icon1)
        self.pushButtonOriginalAlt.setAutoDefault(True)
        self.pushButtonOriginalAlt.setObjectName(_fromUtf8("pushButtonOriginalAlt"))
        self.gridLayout.addWidget(self.pushButtonOriginalAlt, 4, 2, 1, 1)
        self.pushButtonOriginal = QtGui.QPushButton(Dialog)
        self.pushButtonOriginal.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("pypordb/go-next.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOriginal.setIcon(icon2)
        self.pushButtonOriginal.setObjectName(_fromUtf8("pushButtonOriginal"))
        self.gridLayout.addWidget(self.pushButtonOriginal, 4, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setMinimumSize(QtCore.QSize(130, 59))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radioButtonVorhandenJa = QtGui.QRadioButton(self.groupBox_4)
        self.radioButtonVorhandenJa.setObjectName(_fromUtf8("radioButtonVorhandenJa"))
        self.horizontalLayout_3.addWidget(self.radioButtonVorhandenJa)
        self.radioButtonVorhandenNein = QtGui.QRadioButton(self.groupBox_4)
        self.radioButtonVorhandenNein.setObjectName(_fromUtf8("radioButtonVorhandenNein"))
        self.horizontalLayout_3.addWidget(self.radioButtonVorhandenNein)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.LabelRole, self.horizontalLayout_3)
        self.horizontalLayout_11.addWidget(self.groupBox_4)
        self.groupBox_5 = QtGui.QGroupBox(Dialog)
        self.groupBox_5.setMinimumSize(QtCore.QSize(130, 59))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_5)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.radioButtonNurbildJa = QtGui.QRadioButton(self.groupBox_5)
        self.radioButtonNurbildJa.setObjectName(_fromUtf8("radioButtonNurbildJa"))
        self.horizontalLayout_4.addWidget(self.radioButtonNurbildJa)
        self.radioButtonNurbildNein = QtGui.QRadioButton(self.groupBox_5)
        self.radioButtonNurbildNein.setObjectName(_fromUtf8("radioButtonNurbildNein"))
        self.horizontalLayout_4.addWidget(self.radioButtonNurbildNein)
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.LabelRole, self.horizontalLayout_4)
        self.horizontalLayout_11.addWidget(self.groupBox_5)
        self.groupBox_6 = QtGui.QGroupBox(Dialog)
        self.groupBox_6.setMinimumSize(QtCore.QSize(130, 59))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.formLayout_4 = QtGui.QFormLayout(self.groupBox_6)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.radioButtonCoverJa = QtGui.QRadioButton(self.groupBox_6)
        self.radioButtonCoverJa.setObjectName(_fromUtf8("radioButtonCoverJa"))
        self.horizontalLayout_6.addWidget(self.radioButtonCoverJa)
        self.radioButtonCoverNein = QtGui.QRadioButton(self.groupBox_6)
        self.radioButtonCoverNein.setObjectName(_fromUtf8("radioButtonCoverNein"))
        self.horizontalLayout_6.addWidget(self.radioButtonCoverNein)
        self.formLayout_4.setLayout(0, QtGui.QFormLayout.LabelRole, self.horizontalLayout_6)
        self.horizontalLayout_11.addWidget(self.groupBox_6)
        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_13.addWidget(self.label_8)
        self.labelOriginal = QtGui.QLabel(Dialog)
        self.labelOriginal.setText(_fromUtf8(""))
        self.labelOriginal.setObjectName(_fromUtf8("labelOriginal"))
        self.horizontalLayout_13.addWidget(self.labelOriginal)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.checkBoxUninteressant = QtGui.QCheckBox(Dialog)
        self.checkBoxUninteressant.setObjectName(_fromUtf8("checkBoxUninteressant"))
        self.horizontalLayout_7.addWidget(self.checkBoxUninteressant)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.label_17 = QtGui.QLabel(Dialog)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_7.addWidget(self.label_17)
        self.comboBoxDefinition = QtGui.QComboBox(Dialog)
        self.comboBoxDefinition.setObjectName(_fromUtf8("comboBoxDefinition"))
        self.comboBoxDefinition.addItem(_fromUtf8(""))
        self.comboBoxDefinition.setItemText(0, _fromUtf8(""))
        self.comboBoxDefinition.addItem(_fromUtf8(""))
        self.comboBoxDefinition.addItem(_fromUtf8(""))
        self.comboBoxDefinition.addItem(_fromUtf8(""))
        self.comboBoxDefinition.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.comboBoxDefinition)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_7)
        spacerItem2 = QtGui.QSpacerItem(358, 22, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_12.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.spinBoxF = QtGui.QSpinBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxF.sizePolicy().hasHeightForWidth())
        self.spinBoxF.setSizePolicy(sizePolicy)
        self.spinBoxF.setObjectName(_fromUtf8("spinBoxF"))
        self.horizontalLayout_5.addWidget(self.spinBoxF)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.spinBoxH = QtGui.QSpinBox(Dialog)
        self.spinBoxH.setObjectName(_fromUtf8("spinBoxH"))
        self.horizontalLayout_5.addWidget(self.spinBoxH)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_5.addWidget(self.label_7)
        self.spinBoxT = QtGui.QSpinBox(Dialog)
        self.spinBoxT.setObjectName(_fromUtf8("spinBoxT"))
        self.horizontalLayout_5.addWidget(self.spinBoxT)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_5.addWidget(self.label_9)
        self.spinBoxC = QtGui.QSpinBox(Dialog)
        self.spinBoxC.setObjectName(_fromUtf8("spinBoxC"))
        self.horizontalLayout_5.addWidget(self.spinBoxC)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_5.addWidget(self.label_10)
        self.spinBoxX = QtGui.QSpinBox(Dialog)
        self.spinBoxX.setObjectName(_fromUtf8("spinBoxX"))
        self.horizontalLayout_5.addWidget(self.spinBoxX)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_5.addWidget(self.label_11)
        self.spinBoxO = QtGui.QSpinBox(Dialog)
        self.spinBoxO.setObjectName(_fromUtf8("spinBoxO"))
        self.horizontalLayout_5.addWidget(self.spinBoxO)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_5.addWidget(self.label_12)
        self.spinBoxV = QtGui.QSpinBox(Dialog)
        self.spinBoxV.setObjectName(_fromUtf8("spinBoxV"))
        self.horizontalLayout_5.addWidget(self.spinBoxV)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_5.addWidget(self.label_13)
        self.spinBoxB = QtGui.QSpinBox(Dialog)
        self.spinBoxB.setObjectName(_fromUtf8("spinBoxB"))
        self.horizontalLayout_5.addWidget(self.spinBoxB)
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_5.addWidget(self.label_14)
        self.spinBoxA = QtGui.QSpinBox(Dialog)
        self.spinBoxA.setObjectName(_fromUtf8("spinBoxA"))
        self.horizontalLayout_5.addWidget(self.spinBoxA)
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_5.addWidget(self.label_15)
        self.spinBoxS = QtGui.QSpinBox(Dialog)
        self.spinBoxS.setObjectName(_fromUtf8("spinBoxS"))
        self.horizontalLayout_5.addWidget(self.spinBoxS)
        self.label_16 = QtGui.QLabel(Dialog)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_5.addWidget(self.label_16)
        self.spinBoxK = QtGui.QSpinBox(Dialog)
        self.spinBoxK.setObjectName(_fromUtf8("spinBoxK"))
        self.horizontalLayout_5.addWidget(self.spinBoxK)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButtonNeuDarstelleruebernehmen = QtGui.QPushButton(Dialog)
        self.pushButtonNeuDarstelleruebernehmen.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("pypordb/go-up.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonNeuDarstelleruebernehmen.setIcon(icon3)
        self.pushButtonNeuDarstelleruebernehmen.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonNeuDarstelleruebernehmen.setCheckable(False)
        self.pushButtonNeuDarstelleruebernehmen.setObjectName(_fromUtf8("pushButtonNeuDarstelleruebernehmen"))
        self.verticalLayout_3.addWidget(self.pushButtonNeuDarstelleruebernehmen)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.listWidgetW = QtGui.QListWidget(Dialog)
        self.listWidgetW.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetW.setObjectName(_fromUtf8("listWidgetW"))
        self.horizontalLayout_8.addWidget(self.listWidgetW)
        self.listWidgetM = QtGui.QListWidget(Dialog)
        self.listWidgetM.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetM.setObjectName(_fromUtf8("listWidgetM"))
        self.horizontalLayout_8.addWidget(self.listWidgetM)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9.addLayout(self.verticalLayout_3)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setMinimumSize(QtCore.QSize(500, 200))
        self.groupBox_2.setMaximumSize(QtCore.QSize(541, 491))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelNeuBildanzeige = QtGui.QLabel(self.groupBox_2)
        self.labelNeuBildanzeige.setText(_fromUtf8(""))
        self.labelNeuBildanzeige.setObjectName(_fromUtf8("labelNeuBildanzeige"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelNeuBildanzeige)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonBildbeschneiden = QtGui.QPushButton(Dialog)
        self.pushButtonBildbeschneiden.setObjectName(_fromUtf8("pushButtonBildbeschneiden"))
        self.horizontalLayout.addWidget(self.pushButtonBildbeschneiden)
        self.pushButtonBildloeschen = QtGui.QPushButton(Dialog)
        self.pushButtonBildloeschen.setObjectName(_fromUtf8("pushButtonBildloeschen"))
        self.horizontalLayout.addWidget(self.pushButtonBildloeschen)
        self.pushButtonVerz = QtGui.QPushButton(Dialog)
        self.pushButtonVerz.setObjectName(_fromUtf8("pushButtonVerz"))
        self.horizontalLayout.addWidget(self.pushButtonVerz)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonNeuOK = QtGui.QPushButton(Dialog)
        self.pushButtonNeuOK.setAutoDefault(False)
        self.pushButtonNeuOK.setDefault(True)
        self.pushButtonNeuOK.setObjectName(_fromUtf8("pushButtonNeuOK"))
        self.horizontalLayout_2.addWidget(self.pushButtonNeuOK)
        self.pushButtonNeuCancel = QtGui.QPushButton(Dialog)
        self.pushButtonNeuCancel.setObjectName(_fromUtf8("pushButtonNeuCancel"))
        self.horizontalLayout_2.addWidget(self.pushButtonNeuCancel)
        self.pushButtonNeuDelete = QtGui.QPushButton(Dialog)
        self.pushButtonNeuDelete.setObjectName(_fromUtf8("pushButtonNeuDelete"))
        self.horizontalLayout_2.addWidget(self.pushButtonNeuDelete)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_9.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "New / Change / Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label_1.setText(QtGui.QApplication.translate("Dialog", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNeuTitel.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter file name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Actor", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNeuDarsteller.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter the list of actors, separated by comma", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "CD", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNeuCD.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNeuBild.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter file name of image file", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Original", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNeuOriginal.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter original title of the movie. For adding more titles, please press the button on the right side.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOriginalAlt.setToolTip(QtGui.QApplication.translate("Dialog", "<html><head/><body><p>Reuse last entered original title, Ctrl+Y</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOriginalAlt.setWhatsThis(QtGui.QApplication.translate("Dialog", "Reuse last entered original title", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOriginalAlt.setShortcut(QtGui.QApplication.translate("Dialog", "Ctrl+Y", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOriginal.setToolTip(QtGui.QApplication.translate("Dialog", "Enter more movie titles", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOriginal.setWhatsThis(QtGui.QApplication.translate("Dialog", "Enter more movie titles", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Dialog", "present", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonVorhandenJa.setText(QtGui.QApplication.translate("Dialog", "yes", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonVorhandenNein.setText(QtGui.QApplication.translate("Dialog", "no", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("Dialog", "only image", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonNurbildJa.setText(QtGui.QApplication.translate("Dialog", "yes", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonNurbildNein.setText(QtGui.QApplication.translate("Dialog", "no", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("Dialog", "Cover", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonCoverJa.setText(QtGui.QApplication.translate("Dialog", "yes", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonCoverNein.setText(QtGui.QApplication.translate("Dialog", "no", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Title in clipboard:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxUninteressant.setWhatsThis(QtGui.QApplication.translate("Dialog", "Check this box, if you did not like the movie", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxUninteressant.setText(QtGui.QApplication.translate("Dialog", "Not interesting", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("Dialog", "Resolution:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDefinition.setItemText(1, QtGui.QApplication.translate("Dialog", "SD", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDefinition.setItemText(2, QtGui.QApplication.translate("Dialog", "HD 720p", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDefinition.setItemText(3, QtGui.QApplication.translate("Dialog", "HD 1080p", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxDefinition.setItemText(4, QtGui.QApplication.translate("Dialog", "Unknown", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Facial", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Handjob", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Tits", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Cmp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Analcmp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "Oralcmp", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Cunt", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Dialog", "Belly", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "Ass", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Dialog", "Others", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("Dialog", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuDarstelleruebernehmen.setToolTip(QtGui.QApplication.translate("Dialog", "Adopt actor", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuDarstelleruebernehmen.setWhatsThis(QtGui.QApplication.translate("Dialog", "Copy the marked actors to the actors field", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetW.setWhatsThis(QtGui.QApplication.translate("Dialog", "Last used female actors", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetM.setWhatsThis(QtGui.QApplication.translate("Dialog", "Last used male actors", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Image", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNeuBildanzeige.setWhatsThis(QtGui.QApplication.translate("Dialog", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBildbeschneiden.setWhatsThis(QtGui.QApplication.translate("Dialog", "Crop image.\n"
"\n"
"How does cropping work?\n"
"\n"
"First click with the left mouse button in the left top corner, then click with the right mouse button at the bottom right.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBildbeschneiden.setText(QtGui.QApplication.translate("Dialog", "Crop image", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBildloeschen.setWhatsThis(QtGui.QApplication.translate("Dialog", "Delete image file in working directory", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonBildloeschen.setText(QtGui.QApplication.translate("Dialog", "Delete image file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonVerz.setWhatsThis(QtGui.QApplication.translate("Dialog", "Change the working directory", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonVerz.setText(QtGui.QApplication.translate("Dialog", "Change directory", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuOK.setWhatsThis(QtGui.QApplication.translate("Dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuOK.setText(QtGui.QApplication.translate("Dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuOK.setShortcut(QtGui.QApplication.translate("Dialog", "Enter, Return", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuCancel.setWhatsThis(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuCancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuDelete.setWhatsThis(QtGui.QApplication.translate("Dialog", "Entry in database will be deleted, inclusive image file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonNeuDelete.setText(QtGui.QApplication.translate("Dialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

