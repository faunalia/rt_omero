# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgUnisci2Db.ui'
#
# Created: Mon Aug  5 12:16:14 2013
#      by: PyQt4 UI code generator 4.9.3
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
        Dialog.resize(411, 112)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.indb1Edit = QtGui.QLineEdit(Dialog)
        self.indb1Edit.setObjectName(_fromUtf8("indb1Edit"))
        self.gridLayout.addWidget(self.indb1Edit, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.indb2Edit = QtGui.QLineEdit(Dialog)
        self.indb2Edit.setObjectName(_fromUtf8("indb2Edit"))
        self.gridLayout.addWidget(self.indb2Edit, 1, 1, 1, 1)
        self.inBrowse2Btn = QtGui.QToolButton(Dialog)
        self.inBrowse2Btn.setObjectName(_fromUtf8("inBrowse2Btn"))
        self.gridLayout.addWidget(self.inBrowse2Btn, 1, 2, 1, 1)
        self.inBrowse1Btn = QtGui.QToolButton(Dialog)
        self.inBrowse1Btn.setObjectName(_fromUtf8("inBrowse1Btn"))
        self.gridLayout.addWidget(self.inBrowse1Btn, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Unisci 2 database", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "DB di input #2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "DB di input #1", None, QtGui.QApplication.UnicodeUTF8))
        self.inBrowse2Btn.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.inBrowse1Btn.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))

