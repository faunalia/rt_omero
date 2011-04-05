# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgStradario.ui'
#
# Created: Sat Mar 26 14:52:18 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(486, 479)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.delViaBtn = QtGui.QPushButton(self.groupBox)
        self.delViaBtn.setObjectName("delViaBtn")
        self.gridLayout_2.addWidget(self.delViaBtn, 1, 1, 1, 1)
        self.nuovaViaGroup = QtGui.QGroupBox(self.groupBox)
        self.nuovaViaGroup.setObjectName("nuovaViaGroup")
        self.gridLayout = QtGui.QGridLayout(self.nuovaViaGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(self.nuovaViaGroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.viaEdit = QtGui.QLineEdit(self.nuovaViaGroup)
        self.viaEdit.setObjectName("viaEdit")
        self.gridLayout.addWidget(self.viaEdit, 2, 1, 1, 1)
        self.addViaBtn = QtGui.QPushButton(self.nuovaViaGroup)
        self.addViaBtn.setObjectName("addViaBtn")
        self.gridLayout.addWidget(self.addViaBtn, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.nuovaViaGroup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comuneCombo = QtGui.QComboBox(self.nuovaViaGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comuneCombo.sizePolicy().hasHeightForWidth())
        self.comuneCombo.setSizePolicy(sizePolicy)
        self.comuneCombo.setObjectName("comuneCombo")
        self.gridLayout.addWidget(self.comuneCombo, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.nuovaViaGroup, 2, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.vieTable = QtGui.QTableWidget(self.groupBox)
        self.vieTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.vieTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.vieTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.vieTable.setObjectName("vieTable")
        self.vieTable.setColumnCount(0)
        self.vieTable.setRowCount(0)
        self.vieTable.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.vieTable, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Stradario", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Lista", None, QtGui.QApplication.UnicodeUTF8))
        self.delViaBtn.setText(QtGui.QApplication.translate("Dialog", "Elimina", None, QtGui.QApplication.UnicodeUTF8))
        self.nuovaViaGroup.setTitle(QtGui.QApplication.translate("Dialog", "Modifica", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Via/Piazza", None, QtGui.QApplication.UnicodeUTF8))
        self.addViaBtn.setText(QtGui.QApplication.translate("Dialog", "Salva", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Comune", None, QtGui.QApplication.UnicodeUTF8))
        self.vieTable.setSortingEnabled(True)

