# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgSezCaratteristicheStrutturali.ui'
#
# Created: Wed Nov 24 15:49:42 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(381, 248)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.STRUTTURE_PORTANTI_VERTICALIID = WdgStrutturePortantiVerticali()
        self.STRUTTURE_PORTANTI_VERTICALIID.setObjectName("STRUTTURE_PORTANTI_VERTICALIID")
        self.tabWidget.addTab(self.STRUTTURE_PORTANTI_VERTICALIID, "")
        self.STRUTTURE_ORIZZONTALI_SOLAI = MultiTabStruttureOrizzontaliSolai()
        self.STRUTTURE_ORIZZONTALI_SOLAI.setObjectName("STRUTTURE_ORIZZONTALI_SOLAI")
        self.tabWidget.addTab(self.STRUTTURE_ORIZZONTALI_SOLAI, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.STRUTTURE_PORTANTI_VERTICALIID), QtGui.QApplication.translate("Form", "Strutture portanti verticali", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.STRUTTURE_ORIZZONTALI_SOLAI), QtGui.QApplication.translate("Form", "Strutture orizzontali - Solai", None, QtGui.QApplication.UnicodeUTF8))

from ..MultiTabStruttureOrizzontaliSolai import MultiTabStruttureOrizzontaliSolai
from ..WdgStrutturePortantiVerticali import WdgStrutturePortantiVerticali
