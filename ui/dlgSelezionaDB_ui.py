# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dlgSelezionaDB.ui'
#
# Created: Sun Apr 10 14:49:57 2011
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DlgSelezionaDB(object):
    def setupUi(self, DlgSelezionaDB):
        DlgSelezionaDB.setObjectName("DlgSelezionaDB")
        DlgSelezionaDB.resize(589, 352)
        self.gridLayout = QtGui.QGridLayout(DlgSelezionaDB)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.label = QtGui.QLabel(DlgSelezionaDB)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(DlgSelezionaDB)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DlgSelezionaDB)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.btnDbWork = QtGui.QPushButton(DlgSelezionaDB)
        self.btnDbWork.setObjectName("btnDbWork")
        self.gridLayout.addWidget(self.btnDbWork, 3, 1, 1, 1)
        self.btnDbDemo = QtGui.QPushButton(DlgSelezionaDB)
        self.btnDbDemo.setObjectName("btnDbDemo")
        self.gridLayout.addWidget(self.btnDbDemo, 2, 1, 1, 1)
        self.groupBox = QtGui.QGroupBox(DlgSelezionaDB)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtGui.QScrollArea(self.groupBox)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 524, 436))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)

        self.retranslateUi(DlgSelezionaDB)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DlgSelezionaDB.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DlgSelezionaDB.reject)
        QtCore.QMetaObject.connectSlotsByName(DlgSelezionaDB)

    def retranslateUi(self, DlgSelezionaDB):
        DlgSelezionaDB.setWindowTitle(QtGui.QApplication.translate("DlgSelezionaDB", "Necessario un database", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DlgSelezionaDB", "Vuoi utilizzare il DB dimostrativo (DB DEMO)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DlgSelezionaDB", "oppure disponi di un DB di lavoro (DB WORK)?", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDbWork.setText(QtGui.QApplication.translate("DlgSelezionaDB", "DB WORK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDbDemo.setText(QtGui.QApplication.translate("DlgSelezionaDB", "DB DEMO", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DlgSelezionaDB", "Informazioni", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DlgSelezionaDB", "Il plugin Omero-RT impiega un database in formato sqlite/spatialite con una ben precisa struttura di tabelle al suo interno.\n"
"Tale database al momento con questa versione di Omero-RT viene prodotto direttamente dal Servizio S.I.T.A. di Regione Toscana che provvede a creare la base dati e a pre-caricarla con tutti i dati necessari al suo funzionamento tra cui le geometrie di Unita-Volumetriche attinenti al territorio da indagare già codificate con gli opportuni codici regionali da mantenere.\n"
"\n"
"Nel caso si disponga di un database così predisposto per funzionare con il plugin Omero-RT assicurarsi che sia collocato in una cartella in cui si dispone dei diritti di scrittura.\n"
"\n"
"Per permettere di provare l’operativita’ del programma nel caso che non si disponga di un proprio database delle geometrie originali come sopra descritto, il plugin prevede alla partenza l\'opzione di scegliere l\'impiego di un database dimostrativo (DB DEMO) avente la struttura gia\' impostata, i dati precaricati e un centinaio di geometrie precaricate.\n"
"La versione dimostrativa non ha alcuna limitazione salvo il numero di geometrie precaricate limitate per ragioni di spazio a un centinaio di geometrie di unita-volumetriche.\n"
"\n"
"Una avvertenza: \n"
"Il database sqlite/spatialite impiegato con Omero-RT va impiegato esclusivamente con il plugin in questione. In nessun caso va editato con altri strumenti per non alterare irrimediabilmente i contenuti della base dati stessa.", None, QtGui.QApplication.UnicodeUTF8))

