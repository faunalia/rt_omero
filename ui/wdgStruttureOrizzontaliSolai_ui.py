# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgStruttureOrizzontaliSolai.ui'
#
# Created: Wed Nov 24 15:49:43 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 241)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID = MultipleChoiseTipologiaCostruttivaOrizzontale(self.groupBox)
        self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID.setObjectName("ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID")
        self.gridLayout_3.addWidget(self.ZZ_TIPOLOGIA_COSTRUTTIVA_ORIZZONTALE_PREVALENTEID, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.ZZ_QUALITA_INFORMAZIONEID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_QUALITA_INFORMAZIONEID.sizePolicy().hasHeightForWidth())
        self.ZZ_QUALITA_INFORMAZIONEID.setSizePolicy(sizePolicy)
        self.ZZ_QUALITA_INFORMAZIONEID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_QUALITA_INFORMAZIONEID.setObjectName("ZZ_QUALITA_INFORMAZIONEID")
        self.gridLayout.addWidget(self.ZZ_QUALITA_INFORMAZIONEID, 1, 1, 1, 1)
        self.label_18 = QtGui.QLabel(Form)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 0, 1, 1)
        self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.sizePolicy().hasHeightForWidth())
        self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.setSizePolicy(sizePolicy)
        self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID.setObjectName("ZZ_STATO_CONSERVAZIONE_STRUTTURALEID")
        self.gridLayout.addWidget(self.ZZ_STATO_CONSERVAZIONE_STRUTTURALEID, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 22, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.SCHEDA_EDIFICIOID = QtGui.QLineEdit(Form)
        self.SCHEDA_EDIFICIOID.setObjectName("SCHEDA_EDIFICIOID")
        self.gridLayout.addWidget(self.SCHEDA_EDIFICIOID, 4, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Tipologia costruttiva orizzontale prevalente", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Qualità informazione", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("Form", "Stato conservazione strutturale", None, QtGui.QApplication.UnicodeUTF8))

from ..MultipleChoiseTipologiaCostruttivaOrizzontale import MultipleChoiseTipologiaCostruttivaOrizzontale
