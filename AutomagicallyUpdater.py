# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin
Date                 : August 15, 2010 
copyright            : (C) 2010 by Giuseppe Sucameli (Faunalia)
email                : sucameli@faunalia.it
 ***************************************************************************/

Omero plugin
Works done from Faunalia (http://www.faunalia.it) with funding from Regione 
Toscana - S.I.T.A. (http://www.regione.toscana.it/territorio/cartografia/index.html)

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from ConnectionManager import ConnectionManager
from Utils import Porting

class AutomagicallyUpdater:

	DEBUG = False

	DEFAULT_CONN_TYPE = 1	# usa la connessione tramite pyspatialite
	EDIT_CONN_TYPE = 1	# usa la connessione tramite pyspatialite

	PROGRESSIVO_ID = -1
	MAC_ADDRESS = None

	@classmethod
	def _reset(self):
		AutomagicallyUpdater.PROGRESSIVO_ID = -1
		AutomagicallyUpdater.MAC_ADDRESS = None

	@classmethod
	def _getProgressivoID(self):
		AutomagicallyUpdater.PROGRESSIVO_ID = (AutomagicallyUpdater.PROGRESSIVO_ID + 1) % 100000
		return AutomagicallyUpdater.PROGRESSIVO_ID

	@classmethod
	def _getMacAddress(self):
		if AutomagicallyUpdater.MAC_ADDRESS == None:
			settings = QSettings()
			macAddress = settings.value( "/omero_RT/mac3chars", "", type=str )
			if macAddress == "":
				try:
					import uuid
					macAddress = unicode( uuid.uuid1() )[-5:-1]
				except ImportError:
					# modulo uuid non trovato (molto difficile che ciò avvenga)
					# genero i caratteri in modo random
					import random
					value = random.randint(0x0, 0xFFFF)
					macAddress = hex(value)[2:]
				settings.setValue( "/omero_RT/mac3chars", macAddress )
			AutomagicallyUpdater.MAC_ADDRESS = macAddress
		return AutomagicallyUpdater.MAC_ADDRESS

	@classmethod
	def _getIDComune(self):
		settings = QSettings()
		return settings.value( "/omero_RT/lastIDComune", "", type=str )

	@classmethod
	def _getIDRilevatore(self):
		settings = QSettings()
		return settings.value( "/omero_RT/lastIDRilevatore", "", type=str )

	@classmethod
	def _getPathToDb(self):
		settings = QSettings()
		return settings.value( "/omero_RT/pathToSqliteDB", "", type=str )

	@classmethod
	def _setPathToDb(self, path):
		settings = QSettings()
		settings.setValue( "/omero_RT/pathToSqliteDB", path )

	@classmethod
	def _getLastUsedDir(self, key):
		settings = QSettings()
		lastProjectDir = settings.value( "/UI/lastProjectDir", "", type=str )
		return settings.value( "/omero_RT/lastUsedDir/%s" % key, lastProjectDir, type=str )

	@classmethod
	def _setLastUsedDir(self, key, filePath):
		settings = QSettings()
		fileInfo = QFileInfo(filePath)
		if fileInfo.isDir():
			dirPath = fileInfo.filePath()
		else:
			dirPath = fileInfo.path()
		settings.setValue( "/omero_RT/lastUsedDir/%s" % key, dirPath )

	@classmethod
	def offlineMode(self):
		settings = QSettings()
		return settings.value( "/omero_RT/offlineMode", False, type=bool )

	@classmethod
	def setOfflineMode(self, value):
		settings = QSettings()
		settings.setValue( "/omero_RT/offlineMode", value )

	@classmethod
	def getPathToCache(self):
		settings = QSettings()
		return settings.value( "/omero_RT/pathToCache", "", type=str )

	@classmethod
	def setPathToCache(self, value):
		settings = QSettings()
		settings.setValue( "/omero_RT/pathToCache", value )

	@classmethod
	def getCachedExternalWms(self):
		settings = QSettings()
		return settings.value( "/omero_RT/cachedExternalWms", {} )

	@classmethod
	def setCachedExternalWms(self, value):
		settings = QSettings()
		settings.setValue( "/omero_RT/cachedExternalWms", value )

	@classmethod
	def printBehavior(self):
		settings = QSettings()
		mode = settings.value( "/omero_RT/printBehavior", QPrinter.PdfFormat, type=int )
		res = settings.value( "/omero_RT/printResolution", QPrinter.HighResolution, type=int )
		return mode, res

	@classmethod
	def setPrintBehavior(self, mode, res):
		settings = QSettings()
		settings.setValue( "/omero_RT/printBehavior", mode )
		settings.setValue( "/omero_RT/printResolution", res )

		# destroy the printer so the resolution can be updated
		from ManagerWindow import ManagerWindow
		ManagerWindow.destroyPrinter()

	@classmethod
	def getWMSRepositoryUrl(self):
		settings = QSettings()
		return settings.value( "/omero_RT/wmsRepositoryURL", "http://www502.regione.toscana.it/geoscopio/documenti/omero/zz_wms.zip", type=str )

	@classmethod
	def setWMSRepositoryUrl(self, value):
		settings = QSettings()
		settings.setValue( "/omero_RT/wmsRepositoryURL", value )


	class Query():
		def __init__(self, query, params=None, conntype=None):
			self.query = query
			self.setParams(params)
			if conntype == None:
				conntype = AutomagicallyUpdater.DEFAULT_CONN_TYPE
			self.connType = conntype

		def setParams(self, params=None):
			if params == None:
				params = []
			self.params = params if hasattr(params, '__iter__') else [ params ]

		def getQuery(self):
			query = ConnectionManager.getNewQuery(self.connType)
			if query == None:
				return
			query.prepare(self.query)
			for p in self.params:
				query.addBindValue( "%s" % p if p != None else None )

			return query

		def getRow(self, row, ncols):
			query = self.getQuery()
			if query == None:
				return
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text() )
				return
			AutomagicallyUpdater._onQueryExecuted( query.lastQuery() )
			# loop for select the row
			for i in range(row+1):
				if not query.next():
					return
			# store cols
			res = []
			for col in range(ncols):
				res.append( AutomagicallyUpdater._getRealValue( query.value(col) ) )

			return res

		def getFirstResult(self):
			return self.getResult(0, 0)

		def getResult(self, row, col):
			query = self.getQuery()
			if query == None:
				return
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text() )
				return
			AutomagicallyUpdater._onQueryExecuted( query.lastQuery() )
			for i in range(row+1):
				if not query.next():
					return
			return AutomagicallyUpdater._getRealValue( query.value(col) )

	class Table(Query):
		def __init__(self, table, filters=None, params=None, conntype=None):
			self.table = table
			if filters == None:
				filters = []

			query = "SELECT * FROM %s" % self.table
			for f in filters:
				query += " " + f

			AutomagicallyUpdater.Query.__init__(self, query, params, conntype)

	class ZZTable(Table):
		def __init__(self, table, pk=None, orderByField=None, conntype=None):
			if pk == None:
				pk = "ID"
			where = "WHERE %s <> '%s'" % (pk, AutomagicallyUpdater.VALORE_NON_INSERITO)
			if orderByField == None:
				orderByField = 'DESCRIZIONE'
			orderByFilter = "ORDER BY %s ASC" % orderByField

			AutomagicallyUpdater.Table.__init__(self, table, [where, orderByFilter], None, conntype)

	NONE = 0x0
	REQUIRED = 0x1
	OPTIONAL = 0x2

	VALORE_NON_INSERITO = '-900099'

	@classmethod
	def loadValues(self, widget, action):
		widget = self._getRealWidget(widget)
		if widget == None:
			return

		if isinstance(action, AutomagicallyUpdater.Query):
			value = action.getFirst()
			self.setValue(widget, value)

	@classmethod
	def loadTables(self, widget, action):
		widget = self._getRealWidget(widget)
		if widget == None:
			return

		if isinstance(action, AutomagicallyUpdater.Query):
			query = action.getQuery()
			if query == None:
				return
			if not query.exec_():
				self._onQueryError( query.lastQuery(), query.lastError().text(), widget )
				return

		if isinstance(widget, QComboBox):
			if isinstance(action, AutomagicallyUpdater.Query):
				widget.clear()
				while query.next():
					ID = unicode( query.value(0) )
					if ID == self.VALORE_NON_INSERITO:
						continue
					name = unicode( query.value(1) )
					widget.addItem( name, ID )

		elif isinstance(widget, QTableWidget):
			if isinstance(action, AutomagicallyUpdater.Query):
				widget.setRowCount(0)
				widget.setSortingEnabled(False)

				if widget.columnCount() == 0:
					firstLoad = True
					# set columns' name as table header
					widget.setColumnCount( query.record().count() - 1 )
					for col in range(widget.columnCount()):
						colname = QTableWidgetItem( query.record().field(col+1).name() )
						widget.setHorizontalHeaderItem(col, colname)

				while query.next():
					row = widget.rowCount()
					widget.insertRow( row )
					ID = query.value(0)
					for col in range(widget.columnCount()):
						item = QTableWidgetItem()
						try:
							value = int( query.value(col+1) )
						except:
							value = unicode( query.value(col+1) )
						item.setData( Qt.DisplayRole, value )
						item.setData( Qt.UserRole, ID )
						widget.setItem( row, col, item )

				widget.setSortingEnabled(True)

		elif isinstance(widget, QTableView):
			if isinstance(action, AutomagicallyUpdater.Query):
				if isinstance(widget.model(), QSqlQueryModel):
					model = widget.model()	
				else:
					model = QSqlQueryModel()
				model.setQuery( query )
				widget.setModel(model)
				widget.setColumnHidden(0, True)	# hide ID column

		elif isinstance(widget, QListWidget):
			if isinstance(action, AutomagicallyUpdater.Query):
				widget.clear()
				while query.next():
					ID = unicode( query.value(0) )
					if ID == self.VALORE_NON_INSERITO:
						continue
					name = unicode( query.value(1) )
					item = QListWidgetItem( name )
					item.setData( Qt.UserRole, ID )
					widget.addItem( item )

		elif isinstance(widget, QListView):
			if isinstance(action, AutomagicallyUpdater.Query):
				if isinstance(widget.model(), QSqlQueryModel):
					model = widget.model()	
				else:
					model = QSqlQueryModel()
				model.setQuery( query )
				widget.setModel(model)
				widget.setModelColumn(1)	# show the Description column

		self.setValue(widget, None)

	@classmethod
	def getValue(self, widget):
		widget = self._getRealWidget(widget)
		value = None

		from Utils import PicViewer

		if isinstance(widget, MappingOne2One):
			value = widget._ID

		elif isinstance(widget, MappingMany2Many):
			value = widget.getValues()

		elif isinstance(widget, QWidget) and not widget.isEnabled() and (not hasattr(widget, 'isReadOnly') or not widget.isReadOnly()):
			pass

		elif isinstance(widget, PicViewer):
			value = widget.getBytes()

		elif isinstance(widget, QGraphicsView):
			items = widget.scene().items()
			if len(items) <= 0:
				value = None
			else:
				image = items[0].pixmap()
				byteArray = QByteArray()
				bufferIO = QBuffer(byteArray)
				bufferIO.open(QIODevice.WriteOnly)
				image.save(bufferIO, "PNG")
				value = byteArray

		elif isinstance(widget, QComboBox):
			index = widget.currentIndex()
			text = widget.currentText()
			if index >= 0 and widget.itemText(index) == text:
				value = unicode( widget.itemData(index) )
				value = self._getRealValue(value)
				if value == None:
					value = text
			else:
				value = text

		elif isinstance(widget, QAbstractButton) or (isinstance(widget, QGroupBox) and widget.isCheckable()):
			value = True if widget.isChecked() else False

		elif isinstance(widget, QLineEdit):
			value = widget.text() 

		elif isinstance(widget, QPlainTextEdit):
			value = widget.toPlainText()

		elif isinstance(widget, QDateEdit):
			value = widget.date().toString( widget.displayFormat() )

		elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
			value = unicode( widget.value() )

		elif isinstance(widget, QDoubleSpinBox):
			value = unicode( widget.value() )

		elif isinstance(widget, (QTableWidget, QListWidget)):
			selItems = widget.selectedItems()
			if len(selItems) > 0:
				value = unicode( selItems[0].data(Qt.UserRole) )

		elif isinstance(widget, (QTableView, QListView)):
			selIndexes = widget.selectedIndexes()
			if len(selIndexes) > 0:
				# recupera l'ID dal modello
				row = selIndexes[0].row()
				sqlRecord = widget.model().record(row)
				value = unicode( sqlRecord.value(0) )

		return self._getRealValue(value)


	@classmethod
	def setValue(self, widget, value):
		widget = self._getRealWidget(widget)
		value = self._getRealValue(value)

		from Utils import PicViewer

		if isinstance(value, AutomagicallyUpdater.Query):
			value = value.getFirstResult()

		if isinstance(widget, MappingOne2One):
			widget.setupLoader(value)

		elif isinstance(widget, MappingMany2Many):
			widget.setValues(value)

		elif isinstance(widget, PicViewer):
			widget.loadImage( value )

		elif isinstance(widget, QGraphicsView):
			scene = widget.scene()
			if scene == None:
				scene = QGraphicsScene()
				widget.setScene( scene )

			scene.clear()
			if value == None:
				return

			if isinstance(value, str) or isinstance(value, unicode):
				image = QPixmap( value )

			elif isinstance(value, QByteArray):
				image = QPixmap()
				if not image.loadFromData( value ):
					return

			elif isinstance(value, QPixmap):
				image = value

			item = QGraphicsPixmapItem( image )
			scene.addItem( item )

		elif isinstance(widget, QComboBox):
			if value != None:
				index = widget.findData(value)
				if index >= 0:
					widget.setCurrentIndex(index)
				else:
					index = widget.findText(unicode( value ))
					if index >= 0:
						widget.setCurrentIndex(index)
					else:
						widget.setEditText(unicode( value ))
			else:
				widget.setCurrentIndex(-1)

		elif isinstance(widget, QAbstractButton) or (isinstance(widget, QGroupBox) and widget.isCheckable()):
			if isinstance(value, str) or isinstance(value, unicode):
				enabler = value != '0'
			else:
				enabler = True if value else False
			widget.setChecked( enabler )

		elif isinstance(widget, QLineEdit):
			widget.setText(unicode( value )) if value != None else widget.clear()

		elif isinstance(widget, QPlainTextEdit):
			widget.setPlainText(unicode( value )) if value != None else widget.clear()

		elif isinstance(widget, QDateEdit):
			if value == None:
				value = QDate.currentDate()
			if isinstance(value, str) or isinstance(value, unicode):
				value = QDate.fromString( value, widget.displayFormat() )
			widget.setDate(value)

		elif isinstance(widget, QSpinBox):
			if value == None:
				value = 0
			try:
				value = int(value)
			except ValueError:
				value = 0
			widget.setValue(value)

		elif isinstance(widget, QDoubleSpinBox):
			if value == None:
				value = 0
			try:
				value = float(value)
			except ValueError:
				value = 0
			widget.setValue(value)

		elif isinstance(widget, QTableWidget):
			# deseleziona le righe selezionate
			widget.clearSelection()
			if value == None:
				return

			# seleziona la riga che ha ID uguale a quello passato
			for row in range(widget.rowCount()):
				item = widget.item(row, 0)
				if item == None:
					continue
				if value == item.data(Qt.UserRole):
					if widget.selectionBehavior() == QAbstractItemView.SelectRows:
						widget.selectRow( row )
					else:
						item.setSelected( True )
					break

		elif isinstance(widget, QTableView):
			# deseleziona le righe selezionate
			widget.clearSelection()
			if value == None:
				return

			# seleziona la riga che ha ID uguale a quello passato
			row=0
			model = widget.model()
			while model.hasIndex(row,0):
				if unicode(value) == unicode(model.record(row).value(0)):
					widget.selectRow(row)
					break
				row = row + 1

		elif isinstance(widget, QListWidget):
			# seleziona la riga che ha ID uguale a quello passato
			for row in range(widget.count()):
				item = widget.item(row)
				enabler = value != None and unicode(value) == unicode(item.data(Qt.UserRole))
				item.setSelected(enabler)

		elif isinstance(widget, QListView):
			# deseleziona le righe selezionate
			widget.clearSelection()
			if value == None:
				return

			# seleziona la riga che ha ID uguale a quello passato
			row=0
			model = widget.model()
			while model.hasIndex(row,0):
				if not widget.isRowHidden(row) and unicode(value) == unicode(model.record(row).value(0)):
					widget.selectionModel().select( model.index(row, 1), QItemSelectionModel.Rows )
					break
				row = row + 1

		#self._refreshWidgetColor(widget)

	@classmethod
	def _getRealWidget(self, widget):
		if widget == None:
			return
		if isinstance(widget, QWidget):
			return widget
		if ( isinstance(widget, str) or isinstance(widget, unicode) ) and hasattr(self, widget):
			return getattr(self, widget)
		return

	@classmethod
	def _getRealValue(self, value):

		if isinstance(value, buffer):
			value = value = QByteArray( str(value) )

# 		if isinstance(value, QByteArray):
# 			value = QByteArray( value.decode("utf-8") )

# 		if isinstance(value, QVariant):
# 			if not value.isValid():
# 				return
# 
# 			if value.type() == QVariant.ByteArray:
# 				value = value.toByteArray()
# 			else:
# 				value = str( value )

		if value == self.VALORE_NON_INSERITO:
			return

		if hasattr(value, '__len__'):
			if len(value) == 0:
				return

		return value

	@classmethod
	def _getDBStrValue(self, value):
		if value == None:
			return "NULL"
		if isinstance(value, bool):
			return '1' if value else '0'

		value = "%s" % value
		return "'%s'" % value.replace("'","''")


	@classmethod
	def _setEditFlag(self, enabler=True):
		# attiva/disattiva il flag di modifica aggiornando la data di ultima modifica
		valuesDict = {
			'ATTIVO' : 1 if enabler else 0, 
			'DB_LAST_DATE_USAGE' : QDate.currentDate().toString( 'dd/MM/yyyy' )
		}

		# imposta la data di prima modifica se non già impostato
		query = AutomagicallyUpdater.Query( "SELECT DB_FIRST_DATE_USAGE FROM ZZ_DISCLAIMER" )
		if self._getRealValue( query.getFirstResult() ) == None:
			valuesDict[ 'DB_FIRST_DATE_USAGE'] = QDate.currentDate().toString( 'dd/MM/yyyy' )
		self._updateValue( valuesDict, 'ZZ_DISCLAIMER', None, None )

	@classmethod
	def _saveValue(self, name2valueDict, table, pk, ID=None):
		if ID == None:
			return self._insertValue(name2valueDict, table, pk)
		return self._updateValue(name2valueDict, table, pk, ID)

	@classmethod
	def _insertValue(self, name2valueDict, table, pk):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		if name2valueDict == None:
			name2valueDict = {}

		IDComune = self._getIDComune()
		IDRilevatore = self._getIDRilevatore()
		progressivo = self._getProgressivoID()
		macAddress = self._getMacAddress()

		fields = []
		values = []
		bindValues = []
		if pk != None:
			fields.append( pk )
			values.append( "'" + IDComune + "-'||strftime('%Y%m%d%H%M%S', 'now')||'-" + macAddress + "-" + unicode(progressivo) + "_" + IDRilevatore + "'" )
			
		for name, value in name2valueDict.iteritems():
			fields.append( name ) 
			if value == None and unicode(name).startswith( "ZZ" ):
				value = self.VALORE_NON_INSERITO
			elif isinstance(value, (buffer)):
				bindValues.append( value )
				value = '?'
			elif isinstance(value, (QByteArray)):
				bindValues.append( Porting.str( value.toHex() ) )
				value = '?'
			else:
				value = self._getDBStrValue(value)
			values.append( value )

		# memorizza la riga
		query.prepare( "INSERT INTO " + table + " (" + ", ".join(fields) + ") VALUES (" + ", ".join(values) + ")" )
		for v in bindValues:
			query.addBindValue( v )

		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return

		ROWID = unicode( query.lastInsertId() )	# restituisce ROWID
		if pk == None:
			ROWID = None if ROWID == "" else ROWID
			if self.DEBUG:
				print ">>>", query.lastQuery(), " >>> ROWID = ", ROWID
			return ROWID

		# recupera il valore della pk
		insertQuery = query.lastQuery()
		query.prepare( "SELECT " + pk + " FROM " + table + " WHERE ROWID = ?" )
		query.addBindValue( ROWID )
		if not query.exec_() or not query.next():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return

		ID = unicode( query.value(0) )
		if self.DEBUG:
			print ">>>", insertQuery, " >>> pk = ", ID, ">>> ROWID =", ROWID

		return ID

	@classmethod
	def _updateValue(self, name2valueDict, table, pk, ID, filterStr=None, filterParams=None):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		if name2valueDict == None or len(name2valueDict) <= 0:
			return ID

		assignments = []
		bindValues = []
		for name, value in name2valueDict.iteritems():
			if value == None and unicode(name).startswith( "ZZ" ):
				value = self.VALORE_NON_INSERITO
			elif isinstance(value, (buffer, QByteArray)):
				bindValues.append( value )
				value = '?'
			else:
				value = self._getDBStrValue(value)

			assignments.append( "%s = %s" % (name, value) )

		whereClauses = []
		if pk != None:
			whereClauses.append( pk + " = ?" )
			bindValues.append( ID )

		if filterStr != None:
			whereClauses.append( "%s" % filterStr )
			if filterParams != None:
				bindValues.extend( filterParams )

		whereStr = ''
		if whereClauses.__len__() > 0:
			whereStr = " WHERE " + " AND ".join(whereClauses)

		# aggiorna la riga
		query.prepare( "UPDATE " + table + " SET " + ", ".join(assignments) + whereStr )
		for v in bindValues:
			query.addBindValue( v if v != None else None )

		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return
		if self.DEBUG:
			print ">>>", query.lastQuery(), " >>> pk = ", ID
		return ID

	@classmethod
	def _deleteValue(self, table, name2valueDict=None, filterStr=None, filterParams=None):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return False

		if name2valueDict == None:
			name2valueDict = {}

		whereClauses = []
		bindValues = []
		for name, value in name2valueDict.iteritems():
			if value == None and unicode(name).startswith( "ZZ" ):
				value = self.VALORE_NON_INSERITO
			elif isinstance(value, (buffer, QByteArray)):
				bindValues.append( value )
				value = '?'
			else:
				value = self._getDBStrValue(value)

			if value != None:
				whereClauses.append( "%s = %s" % (name, value) )
			else:
				whereClauses.append( "%s IS %s" % (name, value) )

		if filterStr != None:
			whereClauses.append( "%s" % filterStr )
			if filterParams != None:
				bindValues.extend( filterParams )

		whereStr = ''
		if whereClauses.__len__() > 0:
			whereStr = " WHERE " + " AND ".join(whereClauses)
		query.prepare( "DELETE FROM " + table + whereStr )
		for v in bindValues:
			query.addBindValue( v if v != None else None )

		# elimina
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return False
		if self.DEBUG:
			print ">>>", query.lastQuery()
		return True

	@classmethod
	def _insertGeometriaNuova(self, wkb, srid, stato=9):
		return self._insertGeometria(wkb, srid, None, stato)

	@classmethod
	def _insertGeometriaCopiata(self, codice, stato=1):
		return self._insertGeometria(None, -1, codice, stato)

	@classmethod
	def _insertGeometriaSpezzata(self, wkb, srid, codice, stato=2):
		return self._insertGeometria(wkb, srid, codice, stato)

	@classmethod
	def _insertGeometria(self, wkb=None, srid=-1, codice=None, stato=1):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		IDComune = self._getIDComune()
		IDRilevatore = self._getIDRilevatore()
		progressivo = self._getProgressivoID()
		macAddress = self._getMacAddress()

		IDGeometria = "'" + IDComune + "-'||strftime('%Y%m%d%H%M%S', 'now')||'-" + macAddress + "-" + unicode(progressivo) + "_" + IDRilevatore + "'"

		# costruisci la query
		insertStr = "INSERT INTO GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE (ID_UV_NEW, GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE, ZZ_STATO_GEOMETRIAID, ABBINATO_A_SCHEDA, geometria)"

# 		if wkb != None:
# 			query.prepare( insertStr + " VALUES ( %s, ?, ?, '0', ST_GeomFromWKB(?, ?) )" % IDGeometria )
# 			query.addBindValue( codice if codice != None else None )
# 			query.addBindValue( stato if stato != None else self.VALORE_NON_INSERITO )
# 			query.addBindValue( wkb )
# 			query.addBindValue( srid )
		if wkb != None:
			query.prepare( insertStr + " VALUES ( %s, ?, ?, '0', ST_GeomFromText(?, ?) )" % IDGeometria )
			query.addBindValue( codice if codice != None else None )
			query.addBindValue( stato if stato != None else self.VALORE_NON_INSERITO )
			query.addBindValue( wkb )
			query.addBindValue( srid )

		elif codice != None:
			query.prepare( insertStr + " SELECT %s, CODICE, ?, '0', geometria FROM GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA WHERE CODICE = ?" % IDGeometria )
			query.addBindValue( stato if stato != None else self.VALORE_NON_INSERITO )
			query.addBindValue( codice )

		else:
			raise Exception( "AutomagicallyUpdater._insertGeometria() chiamata senza i dovuti parametri" )

		# memorizza la geometria
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return

		ROWID = unicode( query.lastInsertId() )	# restituisce ROWID

		# recupera il valore della pk
		insertQuery = query.lastQuery()
		query.prepare( "SELECT ID_UV_NEW FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ROWID = ?" )
		query.addBindValue( ROWID )
		if not query.exec_() or not query.next():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return
		ID = unicode( query.value(0) )
		if self.DEBUG:
			print ">>>", insertQuery, ">>> pk =", ID, ">>> ROWID =", ROWID

		return ID

	@classmethod
	def _updateGeometria(self, ID, wkb, srid=-1):
		if ID == None:
			return
        
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		#query.prepare( "UPDATE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE SET geometria = ST_GeomFromWKB(?, ?) WHERE ID_UV_NEW = ?" )
		query.prepare( "UPDATE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE SET geometria = ST_GeomFromText(?, ?) WHERE ID_UV_NEW = ?" )
		query.addBindValue( wkb )
		query.addBindValue( srid )
		query.addBindValue( ID )

		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return
		if self.DEBUG:
			print ">>>", query.lastQuery(), ">>> pk =", ID

		return ID 

	@classmethod
	def _deleteGeometria(self, ID=None, filterStr=None, filterParams=None):
		name2valueDict = None
		if ID != None:
			name2valueDict = { "ID_UV_NEW" : ID }
		return AutomagicallyUpdater._deleteValue("GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE", name2valueDict, filterStr, filterParams)

	@classmethod
	def _insertRilevatore(self, nome, cognome, IDComune):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		if IDComune == None:
			IDComune = self._getIDComune()

		IDRilevatore = "'" + IDComune + "-'|| CASE WHEN count(ID) > 0 THEN max(SUBSTR(ID, 10))+1 ELSE 1 END"

		# memorizza il rilevatore
		query.prepare( "INSERT INTO RILEVATORE (ID, NOME, COGNOME) SELECT " + IDRilevatore + ", ?, ? FROM RILEVATORE WHERE ID LIKE '" + IDComune + "%'" )
		query.addBindValue( unicode(nome).upper() )
		query.addBindValue( unicode(cognome).upper() )

		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return
		return unicode( query.lastInsertId() )

	@classmethod
	def _onQueryError(self, query, error, widget=None):
		msg = u"ERROR executing a query:\n\tquery: %s\n\terror: %s\n\twidget: %s" % (query, error, widget)
		if self.DEBUG:
			print msg.encode('utf-8')
		else:
			ConnectionManager.abortTransaction( msg )

	@classmethod
	def _onQueryExecuted(self, query, widget=None):
		msg = u"DEBUG executed query:\n\tquery: %s\n\twidget: %s" % (query, widget)
		if self.DEBUG:
			print msg.encode('utf-8')


class MappingOne2One(AutomagicallyUpdater):
	def __init__(self, table=None, pk=None):
		self._ID = None
		self._tableName = table
		self._pkColumn = pk if pk != None else self.findPKColumnName(table)

		self._parentRef = None
		self._childrenRefs = []

		self._requiredChildren = []
		self._widget2action = {}


	def onClosing(self):
		for widget in self._childrenRefs:
			if isinstance(widget, MappingOne2One):
				widget.onClosing()


	def save(self):
		allChildren = self._recursiveChildrenRefs()
		
		# salva le tabelle collegate a questa con relazione Uno a Uno
		for parent, widget in allChildren:
			if not isinstance(widget, (MappingOne2Many, MappingMany2Many)):
				if not isinstance(widget, MappingOne2One):
					continue
				if not widget.save():
					return False

		values = {}
		# salva i valori dei widget riferiti da questa tabella
		for parent, widget in allChildren:
			if not isinstance(widget, (MappingOne2Many, MappingMany2Many)):
				values[widget.objectName()] = parent.getValue(widget)

		ID = self._saveValue(values, self._tableName, self._pkColumn, self._ID)

		if ID == None:
			return False

		# aggiorna l'id degli oggetti MappingPart
		for widget in self._childrenRefs:
			if isinstance(widget, MappingPart):
				if self._ID == None:	# se non esisteva
					widget.refreshId( ID )	# ricarica i valori


		# salva i valori delle tabelle collegate con relazione Uno a Molti e 
		# Molti a Molti
		for parent, widget in allChildren:
			if isinstance(widget, (MappingOne2Many, MappingMany2Many)):
				if self._ID == None:	# se non esisteva
					widget._ID = ID
				if not widget.save():
					return False

		self._ID = ID
		return True

	def delete(self):
		# elimina i valori delle tabelle collegate
		for parent, widget in self._recursiveChildrenRefs():
			if isinstance(widget, MappingOne2One):
				widget.delete()

		ret = self._deleteValue( self._tableName, { self._pkColumn : self._ID } )
		if ret:
			self._ID = None
		return ret


	def findPKColumnName(self, table):
		if table == None:
			return

		query = AutomagicallyUpdater.Query( "PRAGMA table_info(%s)" % table )
		query = query.getQuery()
		if query == None:
			return
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), None )
			return

		while query.next():
			if unicode( query.value(5) ) == "1":
				return unicode( query.value(1) )
		return

	def _refreshWidgetColor(self, widget):
		widget = self._getRealWidget(widget)
		if not hasattr(widget, 'setStyleSheet'):
			return

		value = self._getRealValue( self.getValue(widget) )
		if widget in self._requiredChildren and value == None:# and widget.isEnabled():
			widget.setStyleSheet("background-color: yellow")
		else:
			widget.setStyleSheet("")


	def setupLoader(self, ID=None):
		self._ID = self._getRealValue(ID)
		self.loadValues()

	def setupValuesUpdater(self, actionsList):
		for action in actionsList:
			role = self.REQUIRED
			if isinstance(action, (tuple, list)):
				child = action[0]
				if len(action) > 1:
					role = action[1]
			else:
				child = action

			self.addChildRef(child, role)

	def setupTablesUpdater(self, actionsDict):
		self._widget2action = actionsDict
		self.loadTables()


	def addChildRef(self, widget, role=None):
		widget = self._getRealWidget(widget)

		self._childrenRefs.append(widget)
		if isinstance(widget, AutomagicallyUpdater):
			widget._parentRef = self
			return

		# imposta il valore di default
		self.setValue(widget, None)

		if role == None:
			role = self.REQUIRED

		if role == self.NONE:
			return

		if role == self.REQUIRED:
			self._requiredChildren.append(widget)

			if isinstance(widget, QComboBox):
				QObject.connect(widget, SIGNAL("currentIndexChanged(int)"), self._refreshWidgetState)
				if widget.isEditable():
					QObject.connect(widget, SIGNAL("editTextChanged(const QString &)"), self._refreshWidgetState)

			elif isinstance(widget, QAbstractButton) or (isinstance(widget, QGroupBox) and widget.isCheckable()):
				return

			elif isinstance(widget, QLineEdit):
				QObject.connect(widget, SIGNAL("textChanged(const QString &)"), self._refreshWidgetState)

			elif isinstance(widget, QPlainTextEdit):
				QObject.connect(widget, SIGNAL("textChanged()"), self._refreshWidgetState)

			elif isinstance(widget, QDateEdit):
				QObject.connect(widget, SIGNAL("dateChanged (const QDate &)"), self._refreshWidgetState)

			elif isinstance(widget, QSpinBox):
				QObject.connect(widget, SIGNAL("valueChanged(int)"), self._refreshWidgetState)

			elif isinstance(widget, QDoubleSpinBox):
				QObject.connect(widget, SIGNAL("valueChanged(double)"), self._refreshWidgetState)

			elif isinstance(widget, QTableView):
				return

			self._refreshWidgetColor(widget)

	def delChildRef(self, widget):
		widget = self._getRealWidget(widget)
		if widget not in self._childrenRefs:
			return
		if isinstance(widget, AutomagicallyUpdater):
			widget._parentRef = None

		self._childrenRefs.remove(widget)

	def _recursiveChildrenRefs(self):
		allChildren = []
		for widget in self._childrenRefs:
			if isinstance(widget, MappingPart):
				allChildren.extend( widget._recursiveChildrenRefs() )
			else:
				allChildren.append( (self, widget) )
		return allChildren

	def _refreshWidgetState(self):
		widget = self.sender()
		self._refreshWidgetColor(widget)


	def _recursiveUpdate(self, func):
		if func == "loadTables":
			widgetsList = self._widget2action.keys()
		elif func == "loadValues":
			widgetsList = self._childrenRefs
		
		for widget in widgetsList:
			if hasattr(self, func):
				handler = getattr(self, func)
				handler(widget)


	def _computeQuery(self, query):
		if query == None:
			return

		if not ':id' in query.lastQuery():
			return query

		if self._ID == None:
			return

		if not hasattr(self._ID, '__iter__'):
			query.bindValue( 'id', self._ID )
		else:
			for i, ID in enumerate(self._ID):
				query.bindValue( 'id%s' % i, ID )
		return query

	def retrieveValue(self, widget, action=None):
		action = self._computeAction(widget, action)

		if isinstance(action, AutomagicallyUpdater.Query):
			query = self._computeQuery( action.getQuery() )
			if query == None:
				return

			if not query.exec_():
				self._onQueryError( query.lastQuery(), query.lastError().text(), self._getRealWidget(widget) )
				return
			if not query.next():
				return

			return query.value(0)

	def _computeAction(self, widget, action=None):
		if action != None:
			return action

		widget = self._getRealWidget(widget)
		if widget == None:
			return

		whereClauses = []
		if not hasattr(self._pkColumn, '__iter__'):
			whereClauses.append( "%s = :id" % (self._pkColumn) )
		else:
			for i, pk in enumerate(self._pkColumn):
				whereClauses.append( "%s = :id%n" % (pk, i) )

		return AutomagicallyUpdater.Query( "SELECT %s FROM %s WHERE %s" % ( widget.objectName(), self._tableName, " AND ".join(whereClauses) ) )


	def loadValues(self, widget=None, action=None):
		if widget == None:
			return self._recursiveUpdate('loadValues')

		widget = self._getRealWidget(widget)
		if widget == None:
			return

		if isinstance(widget, MappingPart):
			return widget.setupLoader(self._ID)
		elif isinstance(widget, MappingOne2Many):
			return widget.setupLoader(self._ID)

		value = self.retrieveValue( widget, action )
		if value is not None:
			self.setValue(widget, value)


	def loadTables(self, widget=None, action=None):
		widget = self._getRealWidget(widget)
		if widget == None:
			return self._recursiveUpdate('loadTables')

		if action == None:
			if not self._widget2action.has_key( widget ):
				return
			action = self._widget2action[widget]

		return AutomagicallyUpdater.loadTables(widget, action)


# rappresenta una parte di una tabella, da trattare quindi come 
# sottogruppo di valori della tabella puntata da _tableName
class MappingPart(MappingOne2One):

	def refreshId(self, ID=None):
		for widget in self._childrenRefs:
			if isinstance(widget, MappingPart):
				widget.refreshId( ID )	# ricarica i valori
		self._ID = ID


# rappresenta un riferimento Uno a Molti
# il valore _ID rappresenta l'ID della tabella padre (Uno) mentre i 
# figli (Molti) sono realizzati come riferimenti Uno a Uno a questo oggetto
class MappingOne2Many(MappingOne2One):

	def __init__(self, table=None, pk=None, parentPk=None):
		MappingOne2One.__init__(self, table, pk)
		self._parentPkColumn = parentPk

	def save(self):
		if self._ID == None:
			return False

		ret = True
		# salva i valori dei widget riferiti da questa tabella
		for parent, widget in self._recursiveChildrenRefs():
			if isinstance(widget, MappingOne2One):
				if hasattr(widget, self._parentPkColumn):
					parentIDwidget = getattr(widget, self._parentPkColumn)
					parent.setValue(parentIDwidget, self._ID)
				ret = widget.save()
				if not ret:
					break

		return ret

	def addNewChild(self):
		return False 

	def _computeAction(self, action):
		if action != None:
			return action

		whereClauses = []
		if not hasattr(self._parentPkColumn, '__iter__'):
			whereClauses.append( "%s = :id" % (self._parentPkColumn) )
		else:
			for i, pk in enumerate(self._parentPkColumn):
				whereClauses.append( "%s = :id%s" % (pk, i) )

		return AutomagicallyUpdater.Query( "SELECT %s FROM %s WHERE %s" % ( self._pkColumn, self._tableName, " AND ".join(whereClauses) ) )

	def loadValues(self, action=None):
		action = self._computeAction(action)

		if isinstance(action, AutomagicallyUpdater.Query):
			query = self._computeQuery( action.getQuery() )
			if query == None:
				return

			if not query.exec_():
				self._onQueryError( query.lastQuery(), query.lastError().text(), self )
				return
			
			i = 0
			while query.next():
				subID = unicode( query.value(0) )
				if i >= len(self._childrenRefs):
					if self.addNewChild() == False:
						break

				self.setValue(self._childrenRefs[i], subID)
				i = i + 1

# rappresenta un riferimento Molti a Molti
class MappingMany2Many(MappingOne2Many):

	def __init__(self, table=None, pk=None, parentPk=None, tableWithValues=None):
		MappingOne2Many.__init__(self, table, pk, parentPk)
		self._tableWithValues = tableWithValues

	def loadValues(self, action=None):
		action = self._computeAction(action)

		if isinstance(action, AutomagicallyUpdater.Query):
			query = self._computeQuery( action.getQuery() )
			if query == None:
				return

			if not query.exec_():
				self._onQueryError( query.lastQuery(), query.lastError().text(), self )
				return
			
			values = []
			i = 0
			while query.next():
				values.append( unicode( query.value(0) ) )
				i = i + 1

			self.setValues(values)

	def getValues(self):
		return []

	def setValues(self, values):
		pass
