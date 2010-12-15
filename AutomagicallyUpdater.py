# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from ConnectionManager import ConnectionManager

class AutomagicallyUpdater:

	EDIT_CONN_TYPE = 1	# usa la connessione tramite pyspatialite

	PROGRESSIVO_ID = -1
	MAC_ADDRESS = None

	@classmethod
	def _reset(self):
		self.PROGRESSIVO_ID = -1
		self.MAC_ADDRESS = None

	@classmethod
	def _getProgressivoID(self):
		self.PROGRESSIVO_ID = (self.PROGRESSIVO_ID + 1) % 100000
		return self.PROGRESSIVO_ID

	@classmethod
	def _getMacAddress(self):
		if self.MAC_ADDRESS == None:
			settings = QSettings()
			macAddress = settings.value( "/omero_RT/mac3chars", QVariant("") ).toString()
			if macAddress.isEmpty():
				try:
					import uuid
					macAddress = str( uuid.uuid1() )[-5:-1]
				except ImportError:
					# modulo uuid non trovato (molto difficile che ciò avvenga)
					# genero i caratteri in modo random
					import random
					value = random.randint(0x0, 0xFFFF)
					macAddress = hex(value)[2:]
				settings.setValue( "/omero_RT/mac3chars", QVariant(macAddress) )
			self.MAC_ADDRESS = macAddress
		return self.MAC_ADDRESS

	@classmethod
	def _getIDComune(self):
		settings = QSettings()
		return settings.value( "/omero_RT/lastIDComune", QVariant("") ).toString()

	@classmethod
	def _getIDRilevatore(self):
		settings = QSettings()
		return settings.value( "/omero_RT/lastIDRilevatore", QVariant("") ).toString()


	class Query():
		def __init__(self, query, params=None):
			self.query = query
			self.setParams(params)

		def setParams(self, params=None):
			if params == None:
				params = []
			self.params = params

		def getQuery(self):
			query = ConnectionManager.getNewQuery()
			if query == None:
				return
			query.prepare(self.query)
			for p in self.params:
				query.addBindValue( "%s" % p if p != None else QVariant() )

			return query

		def getFirstResult(self):
			query = self.getQuery()
			if query == None:
				return
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text() )
				return
			if not query.next():
				return
			value = query.value(0)
			return value.toString() if value.isValid() else None

	class Table(Query):
		def __init__(self, table, filters=None, params=None):
			self.table = table
			if filters == None:
				filters = []

			query = "SELECT * FROM %s" % self.table
			for f in filters:
				query += " " + f

			AutomagicallyUpdater.Query.__init__(self, query, params)

	class ZZTable(Table):
		def __init__(self, table, pk=None, orderByField=None):
			if pk == None:
				pk = "ID"
			where = "WHERE %s <> '%s'" % (pk, AutomagicallyUpdater.VALORE_NON_INSERITO)
			if orderByField == None:
				orderByField = 'DESCRIZIONE'
			orderByFilter = "ORDER BY %s ASC" % orderByField

			AutomagicallyUpdater.Table.__init__(self, table, [where, orderByFilter])

	NONE = 0x0
	REQUIRED = 0x1
	OPTIONAL = 0x2

	VALORE_NON_INSERITO = QString('-900099')

	DEBUG = False

	@classmethod
	def _refreshWidgetColor(self, widget):
		widget = self._getRealWidget(widget)
		if not hasattr(widget, 'setStyleSheet'):
			return

		value = self._getRealValue( self.getValue(widget) )
		if value == None and widget.isEnabled():
			widget.setStyleSheet("background-color: yellow")
		else:
			widget.setStyleSheet("")

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
					ID = query.value(0).toString()
					if ID == self.VALORE_NON_INSERITO:
						continue
					name = query.value(1).toString()
					widget.addItem( name, QVariant(ID) )

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
					ID = query.value(0).toString()
					if ID == self.VALORE_NON_INSERITO:
						continue
					name = query.value(1).toString()
					item = QListWidgetItem( name )
					item.setData( Qt.UserRole, QVariant(ID) )
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

		if isinstance(widget, MappingOne2One):
			value = widget._ID

		elif isinstance(widget, MappingMany2Many):
			value = widget.getValues()

		elif isinstance(widget, QComboBox):
			index = widget.currentIndex()
			text = widget.currentText()
			if index < 0:
				value = text
			elif widget.itemText(index) == text:
				value = widget.itemData(index).toString()
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

		elif isinstance(widget, QSpinBox):
			value = QString.number( widget.value() )

		elif isinstance(widget, QListWidget):
			selItems = widget.selectedItems()
			if len(selItems) > 0:
				value = selItems[0].data(Qt.UserRole)

		elif isinstance(widget, QTableView) or isinstance(widget, QListView):
			selIndexes = widget.selectedIndexes()
			if len(selIndexes) > 0:
				# recupera l'ID dal modello
				row = selIndexes[0].row()
				sqlRecord = widget.model().record(row)
				value = sqlRecord.value(0).toString()

		return self._getRealValue(value)


	@classmethod
	def setValue(self, widget, value):
		widget = self._getRealWidget(widget)
		value = self._getRealValue(value)

		if isinstance(value, AutomagicallyUpdater.Query):
			value = value.getFirstResult()

		if isinstance(widget, MappingOne2One):
			widget.setupLoader(value)

		elif isinstance(widget, MappingMany2Many):
			widget.setValues(value)

		elif isinstance(widget, QComboBox):
			value = value if value != None else ''

			index = -1
			if value != None:
				index = widget.findData(value)

			if index < 0 and widget.isEditable():
				index = widget.findText(value)
				if index < 0:
					widget.setEditText(value)

			widget.setCurrentIndex(index)

		elif isinstance(widget, QAbstractButton) or (isinstance(widget, QGroupBox) and widget.isCheckable()):
			if isinstance(value, str) or isinstance(value, QString):
				enabler = value != '0'
			else:
				enabler = True if value else False
			widget.setChecked( enabler )

		elif isinstance(widget, QLineEdit):
			widget.setText(value) if value != None else widget.clear()

		elif isinstance(widget, QPlainTextEdit):
			widget.setPlainText(value) if value != None else widget.clear()

		elif isinstance(widget, QDateEdit):
			if value == None:
				value = QDate.currentDate()
			if isinstance(value, str) or isinstance(value, QString):
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

		elif isinstance(widget, QTableView):
			# deseleziona le righe selezionate
			widget.clearSelection()
			if value == None:
				return

			# seleziona la riga che ha ID uguale a quello passato
			row=0
			model = widget.model()
			while model.hasIndex(row,0):
				if value == model.record(row).value(0):
					widget.selectRow(row)
					break
				row = row + 1

		elif isinstance(widget, QListWidget):
			# seleziona la riga che ha ID uguale a quello passato
			for row in range(widget.count()):
				item = widget.item(row)
				enabler = value != None and value == item.data(Qt.UserRole)
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
				if not widget.isRowHidden(row) and value == model.record(row).value(0):
					widget.selectionModel().select( model.index(row, 1), QItemSelectionModel.Rows )
					break
				row = row + 1

		#self._refreshWidgetColor(widget)

	@classmethod
	def _getRealWidget(self, widget):
		if widget == None:
			return

		if not isinstance(widget, str):
			return widget

		if hasattr(self, widget):
			return getattr(self, widget)

		try:
			exec( "found = %s" % widget )
			return found
		except:
			pass

		return

	@classmethod
	def _getRealValue(self, value):
		if value == self.VALORE_NON_INSERITO:
			return

		if value == "":
			return

		if isinstance(value, QVariant) and not value.isValid():
			return

		return value

	@classmethod
	def _getDBStrValue(self, value):
		if isinstance(value, bool):
			return '1' if value else '0'
		if value == None:
			return "NULL"

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

		fields = QStringList()
		values = QStringList()
		if pk != None:
			fields << pk
			values << "'" + IDComune + "-'||strftime('%Y%m%d%H%M%S', 'now')||'-" + macAddress + "-" + str(progressivo) + "_" + IDRilevatore + "'"
			
		for name, value in name2valueDict.iteritems():
			fields << name
			if value == None and QString(name).startsWith( "ZZ" ):
				value = self.VALORE_NON_INSERITO
			else:
				value = self._getDBStrValue(value)
			values << value

		# memorizza la riga
		query.prepare( "INSERT INTO " + table + " (" + fields.join(", ") + ") VALUES (" + values.join(", ") + ")" )

		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return

		ROWID = query.lastInsertId().toString()	# restituisce ROWID
		if pk == None:
			ROWID = None if ROWID.isEmpty() else ROWID
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

		ID = query.value(0).toString()
		if self.DEBUG:
			print ">>>", insertQuery, " >>> pk = ", ID, ">>> ROWID =", ROWID

		return ID

	@classmethod
	def _updateValue(self, name2valueDict, table, pk, ID):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		if name2valueDict == None:
			name2valueDict = {}

		assignments = QStringList()
		for name, value in name2valueDict.iteritems():
			if value == None and QString(name).startsWith( "ZZ" ):
				value = self.VALORE_NON_INSERITO
			else:
				value = self._getDBStrValue(value)

			assignments << "%s = %s" % (name, value)

		whereStr = ''
		if pk != None:
			whereStr += " WHERE " + pk + " = ?"

		# aggiorna la riga
		query.prepare( "UPDATE " + table + " SET " + assignments.join(", ") + whereStr )
		if pk != None:
			query.addBindValue( ID )

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

		whereClauses = QStringList()
		for name, value in name2valueDict.iteritems():
			if value == None and QString(name).startsWith( "ZZ" ):
				value = self.VALORE_NON_INSERITO
			else:
				value = self._getDBStrValue(value)

			whereClauses << "%s = %s" % (name, value)

		if filterStr != None:
			whereClauses << "%s" % filterStr

		query.prepare( "DELETE FROM " + table + ( " WHERE " + whereClauses.join(" AND ") if whereClauses.count() else '' ) )
		if filterParams != None:
			for p in filterParams:
				query.addBindValue( p if p != None else QVariant() )

		# elimina
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return False
		if self.DEBUG:
			print ">>>", query.lastQuery()
		return True

	@classmethod
	def _insertGeometriaNuova(self, wkb, stato=9):
		return self._insertGeometria(wkb, None, stato)

	@classmethod
	def _insertGeometriaCopiata(self, codice, stato=1):
		return self._insertGeometria(None, codice, stato)

	@classmethod
	def _insertGeometriaSpezzata(self, wkb, codice, stato=2):
		return self._insertGeometria(wkb, codice, stato)

	@classmethod
	def _insertGeometria(self, wkb=None, codice=None, stato=1):
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		IDComune = self._getIDComune()
		IDRilevatore = self._getIDRilevatore()
		progressivo = self._getProgressivoID()
		macAddress = self._getMacAddress()

		IDGeometria = "'" + IDComune + "-'||strftime('%Y%m%d%H%M%S', 'now')||'-" + macAddress + "-" + str(progressivo) + "_" + IDRilevatore + "'"

		# costruisci la query
		insertStr = "INSERT INTO GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE (ID_UV_NEW, GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZACODICE, ZZ_STATO_GEOMETRIAID, geometria)"

		if wkb != None:
			query.prepare( insertStr + " VALUES ( %s, ?, ?, GeomFromWKB(?) )" % IDGeometria )
			query.addBindValue( codice if codice != None else QVariant() )
			query.addBindValue( stato if stato != None else self.VALORE_NON_INSERITO )
			query.addBindValue( wkb )

		elif codice != None:
			query.prepare( insertStr + " SELECT %s, CODICE, ?, geometria FROM GEOMETRIE_UNITA_VOLUMETRICHE_ORIGINALI_DI_PARTENZA WHERE CODICE = ?" % IDGeometria )
			query.addBindValue( stato if stato != None else self.VALORE_NON_INSERITO )
			query.addBindValue( codice if codice != None else QVariant() )

		else:
			raise Exception( "AutomagicallyUpdater._insertGeometria() chiamata senza i dovuti parametri" )

		# memorizza la geometria
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return

		ROWID = query.lastInsertId().toString()	# restituisce ROWID

		# recupera il valore della pk
		insertQuery = query.lastQuery()
		query.prepare( "SELECT ID_UV_NEW FROM GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE WHERE ROWID = ?" )
		query.addBindValue( ROWID )
		if not query.exec_() or not query.next():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return
		ID = query.value(0).toString()
		if self.DEBUG:
			print ">>>", insertQuery, ">>> pk =", ID, ">>> ROWID =", ROWID

		return ID

	@classmethod
	def _updateGeometria(self, ID, wkb):
		if ID == None:
			return
        
		query = ConnectionManager.getNewQuery( AutomagicallyUpdater.EDIT_CONN_TYPE )
		if query == None:
			return

		query.prepare( "UPDATE GEOMETRIE_RILEVATE_NUOVE_O_MODIFICATE SET geometria = GeomFromWkb(?) WHERE ID_UV_NEW = ?" )
		query.addBindValue( wkb )
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
		query.addBindValue( QString(nome).toUpper() )
		query.addBindValue( QString(cognome).toUpper() )

		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), self )
			return
		return query.lastInsertId().toString()

	@classmethod
	def _onQueryError(self, query, error, widget=None):
		msg = u"ERROR executing a query:\n\tquery: %s\n\terror: %s\n\twidget: %s" % (query, error, widget)
		if not self.DEBUG:
			print msg.encode('ascii', 'replace')
		else:
			ConnectionManager.abortTransaction( msg )


class MappingOne2One(AutomagicallyUpdater):
	def __init__(self, table=None, pk=None):
		self._ID = None
		self._tableName = table
		self._pkColumn = pk if pk != None else self.findPKColumnName(table)

		self._parentRef = None
		self._childrenRefs = []

		self._requiredChildren = []
		self._widget2action = {}


	def save(self):
		allChildren = self._recursiveChildrenRefs()
		
		# salva le tabelle collegate a questa con relazione Uno a Uno
		for widget in allChildren:
			if not ( isinstance(widget, MappingOne2Many) or isinstance(widget, MappingMany2Many) ):
				if not isinstance(widget, MappingOne2One):
					continue
				if not widget.save():
					return False

		values = {}
		# salva i valori dei widget riferiti da questa tabella
		for widget in allChildren:
			if not ( isinstance(widget, MappingOne2Many) or isinstance(widget, MappingMany2Many) ):
				values[widget.objectName()] = self.getValue(widget)

		ID = self._saveValue(values, self._tableName, self._pkColumn, self._ID)

		if ID == None:
			return False

		# salva i valori delle tabelle collegate con relazione Uno a Molti e 
		# Molti a Molti
		for widget in allChildren:
			if isinstance(widget, MappingOne2Many) or isinstance(widget, MappingMany2Many):
				if self._ID == None:	# se non esisteva
					widget._ID = ID
				if not widget.save():
					return False

		self._ID = ID
		return True

	def delete(self):
		# elimina i valori delle tabelle collegate
		for widget in self._recursiveChildrenRefs():
			if isinstance(widget, MappingOne2One):
				widget.delete()

		return self._deleteValue( self._tableName, { self._pkColumn : self._ID } )


	def findPKColumnName(self, table):
		if table == None:
			return

		query = AutomagicallyUpdater.Query( "PRAGMA table_info(%s)" % table )
		query = query.getQuery()
		if query == None:
			return
		if not query.exec_():
			self._onQueryError( query.lastQuery(), query.lastError().text(), widget )
			return

		while query.next():
			if query.value(5).toString() == "1":
				return query.value(1).toString()
		return

	def _refreshWidgetColor(self, widget):
		widget = self._getRealWidget(widget)
		if self._requiredChildren.count(widget) == 0:
			return
		AutomagicallyUpdater._refreshWidgetColor(widget)


	def setupLoader(self, ID=None):
		self._ID = self._getRealValue(ID)
		self.loadValues()

	def setupValuesUpdater(self, actionsList):
		for action in actionsList:
			role = self.REQUIRED
			if isinstance(action, tuple) or isinstance(action, list):
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

		if role == self.NONE:
			return

		if role == None:
			role = self.REQUIRED

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

			elif isinstance(widget, QTableView):
				return

			self._refreshWidgetColor(widget)

	def delChildRef(self, widget):
		widget = self._getRealWidget(widget)
		if self._childrenRefs.count(widget) == 0:
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
				allChildren.append( widget )
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

		if not query.lastQuery().contains(':id'):
			return query

		if self._ID == None:
			return

		if not hasattr(self._ID, '__iter__'):
			query.bindValue( ':id', self._ID )
		else:
			for i, ID in enumerate(self._ID):
				query.bindValue( ':id%s' % i, ID )
		return query

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

		if action == None:
			whereClauses = QStringList()
			if not hasattr(self._pkColumn, '__iter__'):
				whereClauses << "%s = :id" % (self._pkColumn)
			else:
				for i, pk in enumerate(self._pkColumn):
					whereClauses << "%s = :id%n" % (pk, i)

			action = AutomagicallyUpdater.Query( "SELECT %s FROM %s WHERE %s" % ( widget.objectName(), self._tableName, whereClauses.join(" AND ") ) )

		if isinstance(action, AutomagicallyUpdater.Query):
			query = self._computeQuery( action.getQuery() )
			if query == None:
				return

			if not query.exec_():
				self._onQueryError( query.lastQuery(), query.lastError().text(), widget )
				return
			if not query.next():
				return

			self.setValue(widget, query.value(0).toString())


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
	pass


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
		for widget in self._recursiveChildrenRefs():
			if not ( isinstance(widget, MappingOne2Many) or isinstance(widget, MappingMany2Many) ):
				if not isinstance(widget, MappingOne2One):
					continue

				if hasattr(widget, self._parentPkColumn):
					parentIDwidget = getattr(widget, self._parentPkColumn)
					self.setValue(parentIDwidget, self._ID)
				ret = widget.save()
				if not ret:
					break

		return ret

	def addNewChild(self):
		return False 

	def _computeAction(self, action):
		if action != None:
			return action

		whereClauses = QStringList()
		if not hasattr(self._parentPkColumn, '__iter__'):
			whereClauses << "%s = :id" % (self._parentPkColumn)
		else:
			for i, pk in enumerate(self._parentPkColumn):
				whereClauses << "%s = :id%s" % (pk, i)

		return AutomagicallyUpdater.Query( "SELECT %s FROM %s WHERE %s" % ( self._pkColumn, self._tableName, whereClauses.join(" AND ") ) )

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
				subID = query.value(0).toString()
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
				values.append( query.value(0).toString() )
				i = i + 1

			self.setValues(values)

	def getValues(self):
		return []

	def setValues(self, values):
		pass
