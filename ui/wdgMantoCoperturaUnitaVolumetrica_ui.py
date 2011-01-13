# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgMantoCoperturaUnitaVolumetrica.ui'
#
# Created: Thu Jan 13 14:09:44 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 242)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.ZZ_TIPO_MANTO_COPERTURAID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_TIPO_MANTO_COPERTURAID.sizePolicy().hasHeightForWidth())
        self.ZZ_TIPO_MANTO_COPERTURAID.setSizePolicy(sizePolicy)
        self.ZZ_TIPO_MANTO_COPERTURAID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_TIPO_MANTO_COPERTURAID.setObjectName("ZZ_TIPO_MANTO_COPERTURAID")
        self.gridLayout_2.addWidget(self.ZZ_TIPO_MANTO_COPERTURAID, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setIndent(20)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.ALTRO_MANTO_COPERTURA = QtGui.QLineEdit(Form)
        self.ALTRO_MANTO_COPERTURA.setObjectName("ALTRO_MANTO_COPERTURA")
        self.gridLayout_2.addWidget(self.ALTRO_MANTO_COPERTURA, 1, 1, 1, 1)
        self.PRESENZA_INCONGRUENZE = QtGui.QGroupBox(Form)
        self.PRESENZA_INCONGRUENZE.setCheckable(True)
        self.PRESENZA_INCONGRUENZE.setChecked(False)
        self.PRESENZA_INCONGRUENZE.setObjectName("PRESENZA_INCONGRUENZE")
        self.gridLayout = QtGui.QGridLayout(self.PRESENZA_INCONGRUENZE)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtGui.QLabel(self.PRESENZA_INCONGRUENZE)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.DESCRIZIONE_INCONGRUENZA = QtGui.QPlainTextEdit(self.PRESENZA_INCONGRUENZE)
        self.DESCRIZIONE_INCONGRUENZA.setObjectName("DESCRIZIONE_INCONGRUENZA")
        self.gridLayout.addWidget(self.DESCRIZIONE_INCONGRUENZA, 0, 1, 2, 1)
        spacerItem = QtGui.QSpacerItem(20, 75, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.PRESENZA_INCONGRUENZE, 2, 0, 1, 2)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.ZZ_STATO_CONSERVAZIONE_MANTOID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_STATO_CONSERVAZIONE_MANTOID.sizePolicy().hasHeightForWidth())
        self.ZZ_STATO_CONSERVAZIONE_MANTOID.setSizePolicy(sizePolicy)
        self.ZZ_STATO_CONSERVAZIONE_MANTOID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_STATO_CONSERVAZIONE_MANTOID.setObjectName("ZZ_STATO_CONSERVAZIONE_MANTOID")
        self.gridLayout_2.addWidget(self.ZZ_STATO_CONSERVAZIONE_MANTOID, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Tipo di manto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "altro tipo (specificare)", None, QtGui.QApplication.UnicodeUTF8))
        self.PRESENZA_INCONGRUENZE.setTitle(QtGui.QApplication.translate("Form", "Presenza incongruenze", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Descrizione", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Stato di conservazione", None, QtGui.QApplication.UnicodeUTF8))

