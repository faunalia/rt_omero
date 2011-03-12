# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgRiepilogoSchede.ui'
#
# Created: Sat Mar 12 19:38:39 2011
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
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.listaSchedeGroup = QtGui.QGroupBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listaSchedeGroup.sizePolicy().hasHeightForWidth())
        self.listaSchedeGroup.setSizePolicy(sizePolicy)
        self.listaSchedeGroup.setObjectName("listaSchedeGroup")
        self.gridLayout = QtGui.QGridLayout(self.listaSchedeGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.listaSchedeGroup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.apriBtn = QtGui.QPushButton(self.listaSchedeGroup)
        self.apriBtn.setObjectName("apriBtn")
        self.gridLayout.addWidget(self.apriBtn, 2, 0, 1, 1)
        self.centraBtn = QtGui.QPushButton(self.listaSchedeGroup)
        self.centraBtn.setObjectName("centraBtn")
        self.gridLayout.addWidget(self.centraBtn, 2, 1, 1, 1)
        self.stampaBtn = QtGui.QPushButton(self.listaSchedeGroup)
        self.stampaBtn.setObjectName("stampaBtn")
        self.gridLayout.addWidget(self.stampaBtn, 2, 2, 1, 1)
        self.eliminaBtn = QtGui.QPushButton(self.listaSchedeGroup)
        self.eliminaBtn.setObjectName("eliminaBtn")
        self.gridLayout.addWidget(self.eliminaBtn, 3, 0, 1, 1)
        self.schedeList = QtGui.QListWidget(self.listaSchedeGroup)
        self.schedeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.schedeList.setObjectName("schedeList")
        self.gridLayout.addWidget(self.schedeList, 1, 0, 1, 3)
        self.gridLayout_3.addWidget(self.listaSchedeGroup, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Riepilogo schede", None, QtGui.QApplication.UnicodeUTF8))
        self.listaSchedeGroup.setTitle(QtGui.QApplication.translate("Dialog", "Lista schede edificio", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Indirizzo, N.ro Civico - Comune (Provincia)", None, QtGui.QApplication.UnicodeUTF8))
        self.apriBtn.setText(QtGui.QApplication.translate("Dialog", "Apri scheda", None, QtGui.QApplication.UnicodeUTF8))
        self.centraBtn.setText(QtGui.QApplication.translate("Dialog", "Vai a...", None, QtGui.QApplication.UnicodeUTF8))
        self.stampaBtn.setText(QtGui.QApplication.translate("Dialog", "Stampa selezionate", None, QtGui.QApplication.UnicodeUTF8))
        self.eliminaBtn.setText(QtGui.QApplication.translate("Dialog", "Elimina scheda", None, QtGui.QApplication.UnicodeUTF8))

