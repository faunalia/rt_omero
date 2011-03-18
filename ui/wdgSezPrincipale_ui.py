# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgSezPrincipale.ui'
#
# Created: Fri Mar 18 12:56:25 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 288)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.DATA_COMPILAZIONE_SCHEDA = QtGui.QDateEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DATA_COMPILAZIONE_SCHEDA.sizePolicy().hasHeightForWidth())
        self.DATA_COMPILAZIONE_SCHEDA.setSizePolicy(sizePolicy)
        self.DATA_COMPILAZIONE_SCHEDA.setDateTime(QtCore.QDateTime(QtCore.QDate(2010, 9, 1), QtCore.QTime(0, 0, 0)))
        self.DATA_COMPILAZIONE_SCHEDA.setCalendarPopup(True)
        self.DATA_COMPILAZIONE_SCHEDA.setObjectName("DATA_COMPILAZIONE_SCHEDA")
        self.gridLayout_2.addWidget(self.DATA_COMPILAZIONE_SCHEDA, 0, 1, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.RILEVATOREID = QtGui.QTableView(self.groupBox_2)
        self.RILEVATOREID.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.RILEVATOREID.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.RILEVATOREID.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.RILEVATOREID.setObjectName("RILEVATOREID")
        self.gridLayout.addWidget(self.RILEVATOREID, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.printBtn = QtGui.QPushButton(Form)
        self.printBtn.setObjectName("printBtn")
        self.gridLayout_2.addWidget(self.printBtn, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.DATA_COMPILAZIONE_SCHEDA.setDisplayFormat(QtGui.QApplication.translate("Form", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "Rilevatore", None, QtGui.QApplication.UnicodeUTF8))
        self.printBtn.setText(QtGui.QApplication.translate("Form", "Stampa", None, QtGui.QApplication.UnicodeUTF8))

