# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/grpEpocaCostruttiva.ui'
#
# Created: Mon Oct 29 19:34:00 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName(_fromUtf8("GroupBox"))
        GroupBox.resize(582, 96)
        self.gridLayout = QtGui.QGridLayout(GroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID = QtGui.QComboBox(GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.sizePolicy().hasHeightForWidth())
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.setSizePolicy(sizePolicy)
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID.setObjectName(_fromUtf8("ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID"))
        self.gridLayout.addWidget(self.ZZ_QUALITA_INFORMAZIONE_EPOCA_COSTRUTTIVAID, 2, 1, 1, 5)
        self.label = QtGui.QLabel(GroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.INIZIO_EPOCA_COSTRUTTIVA_check = QtGui.QCheckBox(GroupBox)
        self.INIZIO_EPOCA_COSTRUTTIVA_check.setChecked(True)
        self.INIZIO_EPOCA_COSTRUTTIVA_check.setObjectName(_fromUtf8("INIZIO_EPOCA_COSTRUTTIVA_check"))
        self.gridLayout.addWidget(self.INIZIO_EPOCA_COSTRUTTIVA_check, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.INIZIO_EPOCA_COSTRUTTIVA = QtGui.QSpinBox(GroupBox)
        self.INIZIO_EPOCA_COSTRUTTIVA.setMinimum(1000)
        self.INIZIO_EPOCA_COSTRUTTIVA.setMaximum(2100)
        self.INIZIO_EPOCA_COSTRUTTIVA.setProperty(_fromUtf8("value"), 2000)
        self.INIZIO_EPOCA_COSTRUTTIVA.setObjectName(_fromUtf8("INIZIO_EPOCA_COSTRUTTIVA"))
        self.gridLayout.addWidget(self.INIZIO_EPOCA_COSTRUTTIVA, 0, 1, 1, 1)
        self.FINE_EPOCA_COSTRUTTIVA_check = QtGui.QCheckBox(GroupBox)
        self.FINE_EPOCA_COSTRUTTIVA_check.setChecked(True)
        self.FINE_EPOCA_COSTRUTTIVA_check.setObjectName(_fromUtf8("FINE_EPOCA_COSTRUTTIVA_check"))
        self.gridLayout.addWidget(self.FINE_EPOCA_COSTRUTTIVA_check, 0, 3, 1, 1)
        self.FINE_EPOCA_COSTRUTTIVA = QtGui.QSpinBox(GroupBox)
        self.FINE_EPOCA_COSTRUTTIVA.setMinimum(1000)
        self.FINE_EPOCA_COSTRUTTIVA.setMaximum(2100)
        self.FINE_EPOCA_COSTRUTTIVA.setProperty(_fromUtf8("value"), 2000)
        self.FINE_EPOCA_COSTRUTTIVA.setObjectName(_fromUtf8("FINE_EPOCA_COSTRUTTIVA"))
        self.gridLayout.addWidget(self.FINE_EPOCA_COSTRUTTIVA, 0, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)

        self.retranslateUi(GroupBox)
        QtCore.QObject.connect(self.INIZIO_EPOCA_COSTRUTTIVA_check, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.INIZIO_EPOCA_COSTRUTTIVA.setEnabled)
        QtCore.QObject.connect(self.FINE_EPOCA_COSTRUTTIVA_check, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.FINE_EPOCA_COSTRUTTIVA.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(QtGui.QApplication.translate("GroupBox", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        GroupBox.setTitle(QtGui.QApplication.translate("GroupBox", "Periodo di impianto", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GroupBox", "Qualità informazione", None, QtGui.QApplication.UnicodeUTF8))
        self.INIZIO_EPOCA_COSTRUTTIVA_check.setText(QtGui.QApplication.translate("GroupBox", "Inizio della costruzione", None, QtGui.QApplication.UnicodeUTF8))
        self.FINE_EPOCA_COSTRUTTIVA_check.setText(QtGui.QApplication.translate("GroupBox", "Fine della costruzione", None, QtGui.QApplication.UnicodeUTF8))

