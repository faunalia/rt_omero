# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wdgSezPrincipale.ui'
#
# Created: Sat Sep 24 21:02:59 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(380, 451)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.DATA_COMPILAZIONE_SCHEDA = QtGui.QDateEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DATA_COMPILAZIONE_SCHEDA.sizePolicy().hasHeightForWidth())
        self.DATA_COMPILAZIONE_SCHEDA.setSizePolicy(sizePolicy)
        self.DATA_COMPILAZIONE_SCHEDA.setDateTime(QtCore.QDateTime(QtCore.QDate(2010, 9, 1), QtCore.QTime(0, 0, 0)))
        self.DATA_COMPILAZIONE_SCHEDA.setCalendarPopup(True)
        self.DATA_COMPILAZIONE_SCHEDA.setObjectName(_fromUtf8("DATA_COMPILAZIONE_SCHEDA"))
        self.gridLayout_2.addWidget(self.DATA_COMPILAZIONE_SCHEDA, 0, 1, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.RILEVATOREID = QtGui.QTableView(self.groupBox_2)
        self.RILEVATOREID.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.RILEVATOREID.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.RILEVATOREID.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.RILEVATOREID.setObjectName(_fromUtf8("RILEVATOREID"))
        self.gridLayout.addWidget(self.RILEVATOREID, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.printBtn = QtGui.QPushButton(Form)
        self.printBtn.setObjectName(_fromUtf8("printBtn"))
        self.gridLayout_2.addWidget(self.printBtn, 6, 0, 1, 1)
        self.schedaID = QtGui.QLineEdit(Form)
        self.schedaID.setEnabled(False)
        self.schedaID.setReadOnly(True)
        self.schedaID.setObjectName(_fromUtf8("schedaID"))
        self.gridLayout_2.addWidget(self.schedaID, 4, 1, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.NOME_EDIFICIO = QtGui.QLineEdit(Form)
        self.NOME_EDIFICIO.setMaxLength(255)
        self.NOME_EDIFICIO.setObjectName(_fromUtf8("NOME_EDIFICIO"))
        self.gridLayout_2.addWidget(self.NOME_EDIFICIO, 2, 1, 1, 1)
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.vboxlayout.addWidget(self.label_4)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.vboxlayout, 3, 0, 1, 1)
        self.NOTA_STORICA = QtGui.QPlainTextEdit(Form)
        self.NOTA_STORICA.setObjectName(_fromUtf8("NOTA_STORICA"))
        self.gridLayout_2.addWidget(self.NOTA_STORICA, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.DATA_COMPILAZIONE_SCHEDA.setDisplayFormat(QtGui.QApplication.translate("Form", "dd/MM/yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "Rilevatore", None, QtGui.QApplication.UnicodeUTF8))
        self.printBtn.setText(QtGui.QApplication.translate("Form", "Stampa", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Identif. scheda edificio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Nome edificio", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Nota storiografica", None, QtGui.QApplication.UnicodeUTF8))

