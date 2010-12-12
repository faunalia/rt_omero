# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgLocalizzazioneIndirizzi.ui'
#
# Created: Wed Nov 24 15:49:42 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(408, 189)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.ZZ_PROVINCEISTATPROV = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_PROVINCEISTATPROV.sizePolicy().hasHeightForWidth())
        self.ZZ_PROVINCEISTATPROV.setSizePolicy(sizePolicy)
        self.ZZ_PROVINCEISTATPROV.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_PROVINCEISTATPROV.setObjectName("ZZ_PROVINCEISTATPROV")
        self.gridLayout_2.addWidget(self.ZZ_PROVINCEISTATPROV, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.ZZ_COMUNIISTATCOM = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_COMUNIISTATCOM.sizePolicy().hasHeightForWidth())
        self.ZZ_COMUNIISTATCOM.setSizePolicy(sizePolicy)
        self.ZZ_COMUNIISTATCOM.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_COMUNIISTATCOM.setObjectName("ZZ_COMUNIISTATCOM")
        self.gridLayout_2.addWidget(self.ZZ_COMUNIISTATCOM, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.VIA = QtGui.QComboBox(Form)
        self.VIA.setEditable(True)
        self.VIA.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.VIA.setObjectName("VIA")
        self.gridLayout_2.addWidget(self.VIA, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.NUMERI_CIVICI = WdgNumeriCivici(Form)
        self.NUMERI_CIVICI.setMaximumSize(QtCore.QSize(16777215, 150))
        self.NUMERI_CIVICI.setObjectName("NUMERI_CIVICI")
        self.gridLayout_2.addWidget(self.NUMERI_CIVICI, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 42, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "Provincia", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Comune", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Via/Piazza/..", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Numeri civici", None, QtGui.QApplication.UnicodeUTF8))

from ..WdgNumeriCivici import WdgNumeriCivici
