# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgSceltaRilevatore.ui'
#
# Created: Wed Nov 24 15:49:41 2010
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
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.comuneCombo = QtGui.QComboBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comuneCombo.sizePolicy().hasHeightForWidth())
        self.comuneCombo.setSizePolicy(sizePolicy)
        self.comuneCombo.setObjectName("comuneCombo")
        self.gridLayout_3.addWidget(self.comuneCombo, 1, 0, 1, 2)
        self.nuovoRilevatoreGroup = QtGui.QGroupBox(Dialog)
        self.nuovoRilevatoreGroup.setObjectName("nuovoRilevatoreGroup")
        self.gridLayout = QtGui.QGridLayout(self.nuovoRilevatoreGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(self.nuovoRilevatoreGroup)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.cognomeEdit = QtGui.QLineEdit(self.nuovoRilevatoreGroup)
        self.cognomeEdit.setObjectName("cognomeEdit")
        self.gridLayout.addWidget(self.cognomeEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.nuovoRilevatoreGroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.nomeEdit = QtGui.QLineEdit(self.nuovoRilevatoreGroup)
        self.nomeEdit.setObjectName("nomeEdit")
        self.gridLayout.addWidget(self.nomeEdit, 1, 1, 1, 1)
        self.addRilevatoreBtn = QtGui.QPushButton(self.nuovoRilevatoreGroup)
        self.addRilevatoreBtn.setObjectName("addRilevatoreBtn")
        self.gridLayout.addWidget(self.addRilevatoreBtn, 2, 1, 1, 1)
        self.gridLayout_3.addWidget(self.nuovoRilevatoreGroup, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 4, 0, 1, 1)
        self.listaRilevatoriGroup = QtGui.QGroupBox(Dialog)
        self.listaRilevatoriGroup.setObjectName("listaRilevatoriGroup")
        self.gridLayout_2 = QtGui.QGridLayout(self.listaRilevatoriGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.delRilevatoreBtn = QtGui.QPushButton(self.listaRilevatoriGroup)
        self.delRilevatoreBtn.setObjectName("delRilevatoreBtn")
        self.gridLayout_2.addWidget(self.delRilevatoreBtn, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.rilevatoriTable = QtGui.QTableView(self.listaRilevatoriGroup)
        self.rilevatoriTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.rilevatoriTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.rilevatoriTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.rilevatoriTable.setObjectName("rilevatoriTable")
        self.gridLayout_2.addWidget(self.rilevatoriTable, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.listaRilevatoriGroup, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Seleziona comune e rilevatore", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Comune", None, QtGui.QApplication.UnicodeUTF8))
        self.nuovoRilevatoreGroup.setTitle(QtGui.QApplication.translate("Dialog", "Nuovo rilevatore", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Cognome", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Nome", None, QtGui.QApplication.UnicodeUTF8))
        self.addRilevatoreBtn.setText(QtGui.QApplication.translate("Dialog", "Aggiungi alla lista rilevatori", None, QtGui.QApplication.UnicodeUTF8))
        self.listaRilevatoriGroup.setTitle(QtGui.QApplication.translate("Dialog", "Lista rilevatori", None, QtGui.QApplication.UnicodeUTF8))
        self.delRilevatoreBtn.setText(QtGui.QApplication.translate("Dialog", "Rimuovi dalla lista", None, QtGui.QApplication.UnicodeUTF8))

