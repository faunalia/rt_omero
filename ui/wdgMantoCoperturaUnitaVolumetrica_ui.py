# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgMantoCoperturaUnitaVolumetrica.ui'
#
# Created: Sat Sep 25 19:37:09 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName("GroupBox")
        GroupBox.resize(400, 160)
        self.gridLayout = QtGui.QGridLayout(GroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(GroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.ZZ_TIPO_MANTO_COPERTURAID = QtGui.QComboBox(GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_TIPO_MANTO_COPERTURAID.sizePolicy().hasHeightForWidth())
        self.ZZ_TIPO_MANTO_COPERTURAID.setSizePolicy(sizePolicy)
        self.ZZ_TIPO_MANTO_COPERTURAID.setObjectName("ZZ_TIPO_MANTO_COPERTURAID")
        self.gridLayout.addWidget(self.ZZ_TIPO_MANTO_COPERTURAID, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(GroupBox)
        self.label_3.setIndent(20)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.ALTRO_MANTO_COPERTURA = QtGui.QLineEdit(GroupBox)
        self.ALTRO_MANTO_COPERTURA.setObjectName("ALTRO_MANTO_COPERTURA")
        self.gridLayout.addWidget(self.ALTRO_MANTO_COPERTURA, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(GroupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.DESCRIZIONE_INCONGRUENZA = QtGui.QLineEdit(GroupBox)
        self.DESCRIZIONE_INCONGRUENZA.setObjectName("DESCRIZIONE_INCONGRUENZA")
        self.gridLayout.addWidget(self.DESCRIZIONE_INCONGRUENZA, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(GroupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.ZZ_STATO_CONSERVAZIONE_MANTOID = QtGui.QComboBox(GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ZZ_STATO_CONSERVAZIONE_MANTOID.sizePolicy().hasHeightForWidth())
        self.ZZ_STATO_CONSERVAZIONE_MANTOID.setSizePolicy(sizePolicy)
        self.ZZ_STATO_CONSERVAZIONE_MANTOID.setObjectName("ZZ_STATO_CONSERVAZIONE_MANTOID")
        self.gridLayout.addWidget(self.ZZ_STATO_CONSERVAZIONE_MANTOID, 3, 1, 1, 1)

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        GroupBox.setTitle(QtGui.QApplication.translate("GroupBox", "Manto di copertura", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GroupBox", "Tipo di manto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("GroupBox", "altro tipo (specificare)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("GroupBox", "Descrizione incongruenza", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("GroupBox", "Stato di conservazione", None, QtGui.QApplication.UnicodeUTF8))

