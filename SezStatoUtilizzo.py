
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.gui
import qgis.core

from ui.wdgSezStatoUtilizzo_ui import Ui_Form
from ConnectionManager import ConnectionManager
from AutomagicallyUpdater import *

class SezStatoUtilizzo(QWidget, MappingOne2One, Ui_Form):

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		MappingOne2One.__init__(self, "STATO_UTILIZZO_EDIFICIO")
		self.setupUi(self)

		# carica i widget multivalore con i valori delle relative tabelle
		tablesDict = {
			self.ZZ_FRUIZIONE_TEMPORALEID: AutomagicallyUpdater.ZZTable( "ZZ_FRUIZIONE_TEMPORALE" ),
			self.ZZ_STATO_EDIFICIOID: AutomagicallyUpdater.ZZTable( "ZZ_STATO_EDIFICIO" ),
			self.ZZ_TIPOLOGIA_EDILIZIAID: AutomagicallyUpdater.ZZTable( "ZZ_TIPOLOGIA_EDILIZIA" )
		}
		self.setupTablesUpdater(tablesDict)
		self.loadTables()

		# mappa i widget con i campi delle tabelle
		childrenList = [
			self.ZZ_FRUIZIONE_TEMPORALEID,
			self.ZZ_STATO_EDIFICIOID, 
			self.ZZ_TIPOLOGIA_EDILIZIAID,
			self.DESCRIZIONE_VISIVA, 
			self.CATEGORIA_USO_PREVALENTE, 
			self.CATEGORIA_USO_PIANO_TERRA, 
			self.CATEGORIA_USO_ALTRI_PIANI
		]
		self.setupValuesUpdater(childrenList)

		self.connect(self.CATEGORIA_USO_PREVALENTE, SIGNAL( "selectionChanged()" ), self.aggiornaListaPrevalente)
		self.connect(self.CATEGORIA_USO_PIANO_TERRA, SIGNAL( "selectionChanged()" ), self.aggiornaListaPianoTerra)
		self.connect(self.CATEGORIA_USO_ALTRI_PIANI, SIGNAL( "selectionChanged()" ), self.aggiornaListaAltriPiani)

	def aggiornaListaPrevalente(self):
		self.aggiornaListaRiepilogo(self.CATEGORIA_USO_PREVALENTE, self.catUsoPrevalenteList)

	def aggiornaListaPianoTerra(self):
		self.aggiornaListaRiepilogo(self.CATEGORIA_USO_PIANO_TERRA, self.catUsoPianoTerraList)

	def aggiornaListaAltriPiani(self):
		self.aggiornaListaRiepilogo(self.CATEGORIA_USO_ALTRI_PIANI, self.catUsoAltriPianiList)

	def aggiornaListaRiepilogo(self, listaConValori, listaDiRiepilogo):
		values = listaConValori.getValues()
		values = map( lambda x: "'%s'" % x, values )
		query = AutomagicallyUpdater.Query( "SELECT * FROM " + listaConValori._tableWithValues + " WHERE ID IN (" + ",".join(values) + ") ORDER BY DESCRIZIONE ASC" )
		self.loadTables(listaDiRiepilogo, query)

