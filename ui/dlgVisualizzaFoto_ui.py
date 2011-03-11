# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgVisualizzaFoto.ui'
#
# Created: Thu Mar 10 10:00:25 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(578, 178)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.listaFoto = QtGui.QWidget(self.scrollArea)
        self.listaFoto.setGeometry(QtCore.QRect(0, 0, 558, 158))
        self.listaFoto.setObjectName("listaFoto")
        self.scrollArea.setWidget(self.listaFoto)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Visualizza foto", None, QtGui.QApplication.UnicodeUTF8))

