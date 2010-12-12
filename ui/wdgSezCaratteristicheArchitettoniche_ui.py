# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgSezCaratteristicheArchitettoniche.ui'
#
# Created: Wed Nov 24 15:49:42 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(507, 172)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.ZZ_PROSPETTO_PREVALENTEID = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_PROSPETTO_PREVALENTEID.sizePolicy().hasHeightForWidth())
        self.ZZ_PROSPETTO_PREVALENTEID.setSizePolicy(sizePolicy)
        self.ZZ_PROSPETTO_PREVALENTEID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_PROSPETTO_PREVALENTEID.setObjectName("ZZ_PROSPETTO_PREVALENTEID")
        self.gridLayout.addWidget(self.ZZ_PROSPETTO_PREVALENTEID, 0, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.PARAMENTIID = WdgCaratteristicheArchitettonicheParamenti()
        self.PARAMENTIID.setObjectName("PARAMENTIID")
        self.tabWidget.addTab(self.PARAMENTIID, "")
        self.BALCONIID = WdgCaratteristicheArchitettonicheBalconi()
        self.BALCONIID.setObjectName("BALCONIID")
        self.tabWidget.addTab(self.BALCONIID, "")
        self.INFISSIID = WdgCaratteristicheArchitettonicheInfissi()
        self.INFISSIID.setObjectName("INFISSIID")
        self.tabWidget.addTab(self.INFISSIID, "")
        self.OSCURAMENTIID = WdgCaratteristicheArchitettonicheOscuramenti()
        self.OSCURAMENTIID.setObjectName("OSCURAMENTIID")
        self.tabWidget.addTab(self.OSCURAMENTIID, "")
        self.GRONDAID = WdgCaratteristicheArchitettonicheGronda()
        self.GRONDAID.setObjectName("GRONDAID")
        self.tabWidget.addTab(self.GRONDAID, "")
        self.ELEMENTI_DECORATIVIID = WdgCaratteristicheArchitettonicheElemDecorativi()
        self.ELEMENTI_DECORATIVIID.setObjectName("ELEMENTI_DECORATIVIID")
        self.tabWidget.addTab(self.ELEMENTI_DECORATIVIID, "")
        self.SUPERFETAZIONI_INCONGRUENZEID = WdgCaratteristicheArchitettonicheSuperfetazioni()
        self.SUPERFETAZIONI_INCONGRUENZEID.setObjectName("SUPERFETAZIONI_INCONGRUENZEID")
        self.tabWidget.addTab(self.SUPERFETAZIONI_INCONGRUENZEID, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 2)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Prospetto prevalente", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PARAMENTIID), QtGui.QApplication.translate("Form", "Paramenti", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.BALCONIID), QtGui.QApplication.translate("Form", "Balconi", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.INFISSIID), QtGui.QApplication.translate("Form", "Infissi", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.OSCURAMENTIID), QtGui.QApplication.translate("Form", "Oscuramenti", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.GRONDAID), QtGui.QApplication.translate("Form", "Gronda", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ELEMENTI_DECORATIVIID), QtGui.QApplication.translate("Form", "Elem. decorativi", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SUPERFETAZIONI_INCONGRUENZEID), QtGui.QApplication.translate("Form", "Superfetazioni ed incongruenze", None, QtGui.QApplication.UnicodeUTF8))

from ..WdgCaratteristicheArchitettonicheElemDecorativi import WdgCaratteristicheArchitettonicheElemDecorativi
from ..WdgCaratteristicheArchitettonicheBalconi import WdgCaratteristicheArchitettonicheBalconi
from ..WdgCaratteristicheArchitettonicheParamenti import WdgCaratteristicheArchitettonicheParamenti
from ..WdgCaratteristicheArchitettonicheInfissi import WdgCaratteristicheArchitettonicheInfissi
from ..WdgCaratteristicheArchitettonicheOscuramenti import WdgCaratteristicheArchitettonicheOscuramenti
from ..WdgCaratteristicheArchitettonicheGronda import WdgCaratteristicheArchitettonicheGronda
from ..WdgCaratteristicheArchitettonicheSuperfetazioni import WdgCaratteristicheArchitettonicheSuperfetazioni
