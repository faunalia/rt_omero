# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import qgis.gui
import qgis.core

from ui.mainSchedaEdificio_ui import Ui_SchedaEdificio
from AutomagicallyUpdater import *

class SchedaEdificio(QMainWindow, MappingOne2One, Ui_SchedaEdificio):

	def __init__(self, parent=None, iface=None):
		QMainWindow.__init__(self, parent)
		MappingOne2One.__init__(self, "SCHEDA_EDIFICIO")
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.iface = iface
		self.setupUi(self)
		self.sectionsStacked.setCurrentIndex(0)

		# salva il titolo predefinito della finestra
		self.title = self.windowTitle()

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.ZZ_PROPRIETA_PREVALENTEID: AutomagicallyUpdater.ZZTable( "ZZ_PROPRIETA_PREVALENTE" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.PRINCIPALE, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ,
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.ZZ_PROPRIETA_PREVALENTEID, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.NUM_UNITA_IMMOBILIARI, 
			self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.PARTICELLE_CATASTALI, 
			self.UNITA_VOLUMETRICHE, 
			self.INTERVENTI, 
			self.STATO_UTILIZZO_EDIFICIOID,
			self.CARATTERISTICHE_STRUTTURALI, 
			self.CARATTERISTICHE_ARCHITETTONICHE_EDIFICIOID
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.sectionsList, SIGNAL("itemSelectionChanged()"), self.currentSectionChanged)

		# aggiorna il titolo della scheda con l'indirizzo del primo tab indirizzi
		primoTabIndirizzi = self.LOCALIZZAZIONE_EDIFICIOIDLOCALIZZ.LOCALIZZAZIONE_EDIFICIO_INDIRIZZO_VIA.firstTab
		self.connect(primoTabIndirizzi, SIGNAL("indirizzoChanged(const QString &)"), self.impostaTitolo)

	def currentSectionChanged(self):
		if self.sectionsList.currentRow() < 0:
			return
		self.sectionsStacked.setCurrentIndex(self.sectionsList.currentRow())

	def impostaTitolo(self, title=QString()):
		if not title.isEmpty():
			self.setWindowTitle( title )
		else:
			self.setWindowTitle( self.title )

	def closeEvent(self, event):
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ConnectionManager.startTransaction()

			# effettua il salvataggio della scheda
			self.save()

		except Exception, e:
			if isinstance(e, ConnectionManager.AbortedException):
				QMessageBox.critical(self, "Errore", e.toString())
				return
			raise

		finally:
			ConnectionManager.endTransaction()
			QApplication.restoreOverrideCursor()

		return QMainWindow.closeEvent(self, event)
