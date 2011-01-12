# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/grpEpocaCostruttiva.ui'
#
# Created: Wed Jan 12 21:29:14 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName("GroupBox")
        GroupBox.resize(515, 95)
        self.gridLayout = QtGui.QGridLayout(GroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtGui.QLabel(GroupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.INIZIO_EPOCA_COSTRUTTIVA = QtGui.QDateEdit(GroupBox)
        self.INIZIO_EPOCA_COSTRUTTIVA.setObjectName("INIZIO_EPOCA_COSTRUTTIVA")
        self.gridLayout.addWidget(self.INIZIO_EPOCA_COSTRUTTIVA, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(GroupBox)
        self.label_8.setIndent(40)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 2, 1, 1)
        self.FINE_EPOCA_COSTRUTTIVA = QtGui.QDateEdit(GroupBox)
        self.FINE_EPOCA_COSTRUTTIVA.setObjectName("FINE_EPOCA_COSTRUTTIVA")
        self.gridLayout.addWidget(self.FINE_EPOCA_COSTRUTTIVA, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(33, 23, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID = QtGui.QComboBox(GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.sizePolicy().hasHeightForWidth())
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.setSizePolicy(sizePolicy)
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.setObjectName("ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID")
        self.gridLayout.addWidget(self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID, 1, 2, 1, 3)
        self.label = QtGui.QLabel(GroupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(QtGui.QApplication.translate("GroupBox", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        GroupBox.setTitle(QtGui.QApplication.translate("GroupBox", "Periodo di impianto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("GroupBox", "Inizio della costruzione", None, QtGui.QApplication.UnicodeUTF8))
        self.INIZIO_EPOCA_COSTRUTTIVA.setDisplayFormat(QtGui.QApplication.translate("GroupBox", "yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("GroupBox", "Fine della costruzione", None, QtGui.QApplication.UnicodeUTF8))
        self.FINE_EPOCA_COSTRUTTIVA.setDisplayFormat(QtGui.QApplication.translate("GroupBox", "yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GroupBox", "Qualità informazione", None, QtGui.QApplication.UnicodeUTF8))

