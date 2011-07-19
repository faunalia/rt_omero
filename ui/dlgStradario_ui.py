# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgStradario.ui'
#
# Created: Tue Jul 19 16:58:39 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(486, 479)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.delViaBtn = QtGui.QPushButton(self.groupBox)
        self.delViaBtn.setObjectName(_fromUtf8("delViaBtn"))
        self.gridLayout_2.addWidget(self.delViaBtn, 1, 1, 1, 1)
        self.nuovaViaGroup = QtGui.QGroupBox(self.groupBox)
        self.nuovaViaGroup.setObjectName(_fromUtf8("nuovaViaGroup"))
        self.gridLayout = QtGui.QGridLayout(self.nuovaViaGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.nuovaViaGroup)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.viaEdit = QtGui.QLineEdit(self.nuovaViaGroup)
        self.viaEdit.setObjectName(_fromUtf8("viaEdit"))
        self.gridLayout.addWidget(self.viaEdit, 2, 1, 1, 1)
        self.addViaBtn = QtGui.QPushButton(self.nuovaViaGroup)
        self.addViaBtn.setObjectName(_fromUtf8("addViaBtn"))
        self.gridLayout.addWidget(self.addViaBtn, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.nuovaViaGroup)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comuneCombo = QtGui.QComboBox(self.nuovaViaGroup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comuneCombo.sizePolicy().hasHeightForWidth())
        self.comuneCombo.setSizePolicy(sizePolicy)
        self.comuneCombo.setObjectName(_fromUtf8("comuneCombo"))
        self.gridLayout.addWidget(self.comuneCombo, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.nuovaViaGroup, 2, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.vieTable = QtGui.QTableView(self.groupBox)
        self.vieTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.vieTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.vieTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.vieTable.setSortingEnabled(True)
        self.vieTable.setObjectName(_fromUtf8("vieTable"))
        self.vieTable.horizontalHeader().setStretchLastSection(True)
        self.vieTable.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout_2.addWidget(self.vieTable, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Stradario", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Lista", None, QtGui.QApplication.UnicodeUTF8))
        self.delViaBtn.setText(QtGui.QApplication.translate("Dialog", "Elimina", None, QtGui.QApplication.UnicodeUTF8))
        self.nuovaViaGroup.setTitle(QtGui.QApplication.translate("Dialog", "Modifica", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Via/Piazza", None, QtGui.QApplication.UnicodeUTF8))
        self.addViaBtn.setText(QtGui.QApplication.translate("Dialog", "Salva", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Comune", None, QtGui.QApplication.UnicodeUTF8))

