# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgCaratteristicheArchitettonicheChild.ui'
#
# Created: Wed Nov 24 15:49:41 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(382, 302)
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_7 = QtGui.QGroupBox(Form)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_21 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.label_16 = QtGui.QLabel(self.groupBox_7)
        self.label_16.setIndent(25)
        self.label_16.setObjectName("label_16")
        self.gridLayout_21.addWidget(self.label_16, 1, 0, 1, 1)
        self.ALTRO = QtGui.QLineEdit(self.groupBox_7)
        self.ALTRO.setObjectName("ALTRO")
        self.gridLayout_21.addWidget(self.ALTRO, 1, 1, 1, 1)
        self.ZZ_TIPO = MultipleChoiseCheckList(self.groupBox_7)
        self.ZZ_TIPO.setObjectName("ZZ_TIPO")
        self.gridLayout_21.addWidget(self.ZZ_TIPO, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_7, 0, 0, 1, 2)
        self.label_17 = QtGui.QLabel(Form)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 1, 0, 1, 1)
        self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID.sizePolicy().hasHeightForWidth())
        self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID.setSizePolicy(sizePolicy)
        self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID.setObjectName("ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID")
        self.gridLayout_3.addWidget(self.ZZ_STATO_CONSERVAZIONE_ARCHITETTONICOID, 1, 1, 1, 1)
        self.incongruenzeInfo = QtGui.QWidget(Form)
        self.incongruenzeInfo.setObjectName("incongruenzeInfo")
        self.gridLayout_2 = QtGui.QGridLayout(self.incongruenzeInfo)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.PRESENZA_INCONGRUENZE = QtGui.QGroupBox(self.incongruenzeInfo)
        self.PRESENZA_INCONGRUENZE.setCheckable(True)
        self.PRESENZA_INCONGRUENZE.setChecked(False)
        self.PRESENZA_INCONGRUENZE.setObjectName("PRESENZA_INCONGRUENZE")
        self.gridLayout = QtGui.QGridLayout(self.PRESENZA_INCONGRUENZE)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.PRESENZA_INCONGRUENZE)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.DESCRIZIONI_INCONGRUENZE = QtGui.QPlainTextEdit(self.PRESENZA_INCONGRUENZE)
        self.DESCRIZIONI_INCONGRUENZE.setObjectName("DESCRIZIONI_INCONGRUENZE")
        self.gridLayout.addWidget(self.DESCRIZIONI_INCONGRUENZE, 0, 1, 2, 1)
        spacerItem = QtGui.QSpacerItem(20, 75, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.PRESENZA_INCONGRUENZE, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.incongruenzeInfo, 2, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_7.setTitle(QtGui.QApplication.translate("Form", "Tipologia", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("Form", "altro (specificare)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("Form", "Stato conservazione", None, QtGui.QApplication.UnicodeUTF8))
        self.PRESENZA_INCONGRUENZE.setTitle(QtGui.QApplication.translate("Form", "Presenza incongruenze", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Descrizione", None, QtGui.QApplication.UnicodeUTF8))

from ..MultipleChoiseCheckList import MultipleChoiseCheckList
