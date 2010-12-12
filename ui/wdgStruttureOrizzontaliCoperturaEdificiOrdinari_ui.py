# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgStruttureOrizzontaliCoperturaEdificiOrdinari.ui'
#
# Created: Wed Nov 24 15:49:43 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 144)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_14 = QtGui.QLabel(Form)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 0, 0, 1, 1)
        self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID.sizePolicy().hasHeightForWidth())
        self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID.setSizePolicy(sizePolicy)
        self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID.setObjectName("ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID")
        self.gridLayout.addWidget(self.ZZ_TIPOLOGIA_COSTRUTTIVA_COPERTURA_EDIFICI_ORDINARIID, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(Form)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)
        self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID.sizePolicy().hasHeightForWidth())
        self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID.setSizePolicy(sizePolicy)
        self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID.setObjectName("ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID")
        self.gridLayout.addWidget(self.ZZ_COMPORTAMENTO_STRUTTURALE_COPERTURAID, 1, 1, 1, 1)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID.sizePolicy().hasHeightForWidth())
        self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID.setSizePolicy(sizePolicy)
        self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID.setObjectName("ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID")
        self.gridLayout.addWidget(self.ZZ_STATO_CONSERVAZIONE_COPERTURA_EDIFICI_ORDINARIID, 2, 1, 1, 1)
        self.label_15 = QtGui.QLabel(Form)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 3, 0, 1, 1)
        self.ZZ_QUALITA_INFORMAZIONEID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_QUALITA_INFORMAZIONEID.sizePolicy().hasHeightForWidth())
        self.ZZ_QUALITA_INFORMAZIONEID.setSizePolicy(sizePolicy)
        self.ZZ_QUALITA_INFORMAZIONEID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_QUALITA_INFORMAZIONEID.setObjectName("ZZ_QUALITA_INFORMAZIONEID")
        self.gridLayout.addWidget(self.ZZ_QUALITA_INFORMAZIONEID, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Form", "Tipologia costruttiva", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Form", "Comportamento strutturale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "Stato di conservazione", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Form", "Qualità dell\'informazione", None, QtGui.QApplication.UnicodeUTF8))

