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
from PyQt4.QtSql import *
from pyspatialite import dbapi2 as sqlite

class ConnectionManager:

	defaultConnType = "QSQLITE"
	defaultConnName = "rt_omero_default_connection"

	connPySL = None
	isTransaction = False
	transactionError = False
	numTransaction = 0

	@classmethod
	def setConnection(self, path):
		# connessione tramite pyspatialite
		try:
			self.connPySL = PySLDatabase(path)
		except sqlite.OperationalError, e:
			return False

		# connessione tramite QtSql
		conn = QSqlDatabase.database( self.defaultConnName )
		if conn != None and conn.isValid():
			return True

		conn = QSqlDatabase.addDatabase( self.defaultConnType, self.defaultConnName )
		conn.setHostName("localhost")
		conn.setDatabaseName(path)
		return conn.open()

	@classmethod
	def closeConnection(self):
		del self.connPySL
		self.connPySL = None

		conn = QSqlDatabase.database( self.defaultConnName )
		if conn != None and conn.isValid():
			conn.close()
			conn = None
			QSqlDatabase.removeDatabase( self.defaultConnName )

	@classmethod
	def getConnection(self, type=0):
		if type == 1:
			conn = self.connPySL
		else:
			conn = QSqlDatabase.database( self.defaultConnName, True )

		if conn == None or not conn.isValid():
			return None
		return conn

	@classmethod
	def getNewQuery(self, type=0):
		conn = self.getConnection(type)
		if conn == None:
			return None

		if self.isTransaction and self.transactionError:
			return None

		if type == 1:
			return PySLQuery(conn, not self.isTransaction)
		return QSqlQuery(conn)

	@classmethod
	def startTransaction(self):
		self.transactionError = False
		conn = self.getConnection(0)
		self.isTransaction = conn != None and conn.transaction()
		conn = self.getConnection(1)
		self.isTransaction = self.isTransaction and conn != None and conn.transaction()
		self.numTransaction = self.numTransaction + 1
		if self.numTransaction == 1:
			from AutomagicallyUpdater import AutomagicallyUpdater
			AutomagicallyUpdater._setEditFlag( True )
		return self.isTransaction

	@classmethod
	def abortTransaction(self, errorMsg=QString()):
		if not self.isTransaction:
			return
		self.transactionError = True

		conn = self.getConnection(0)
		if conn != None:
			conn.rollback()

		conn = self.getConnection(1)
		if conn != None:
			conn.rollback()

		raise ConnectionManager.AbortedException( errorMsg )

	@classmethod
	def endTransaction(self, force=False):
		if not self.isTransaction:
			return
		self.isTransaction = False
		self.numTransaction = self.numTransaction - 1 

		if self.numTransaction > 0 and not force:
			return

		from AutomagicallyUpdater import AutomagicallyUpdater
		AutomagicallyUpdater._setEditFlag( False )

		if self.transactionError:
			self.transactionError = False
			return

		conn = self.getConnection(0)
		if conn != None:
			conn.commit()

		conn = self.getConnection(1)
		if conn != None:
			conn.commit()


	class AbortedException(Exception):
		def __init__(self, msg):
			Exception(self, msg)
			self.msg = msg

		def __str__(self):
			return unicode(self.msg).encode("utf-8")

		def toString(self):
			return QString(self.msg)


class PySLDatabase:

	def __init__(self, path):
		self._error = QString()
		try:
			self.connection = sqlite.connect(u"%s" % path)
		except sqlite.OperationalError, e:
			self._error = QString( str(e) )

	def getQuery(self, autocommit=True):
		return PySLQuery(self)

	def __del__(self):
		self.connection = None

	def isValid(self):
		return self._error.isEmpty()

	def transaction(self):
		return True

	def rollback(self):
		self.connection.rollback()

	def commit(self):
		try:
			self.connection.commit()
		except sqlite.OperationalError, e:
			pass

class PySLError:
	def __init__(self, msg=''):
		self.msg = QString(msg)

	def text(self):
		return self.msg

class PySLQuery:

	def __init__(self, conn, autocommit=True):
		self._autocommit = autocommit
		self._dbconn = conn
		self._cursor = self._dbconn.connection.cursor()
		self.clear()

	def clear(self):
		self._sql = QString()
		self._query = QString()
		self._markParams = []
		self._namedParams = {}
		self._error = PySLError()
		self._value = None

	def prepare(self, sql):
		self.setQuery(sql)

	def escapeValue(self, value):
		value = self.convertResult( value )
		if not value.isValid():
			return 'NULL'

		if value.type() == QVariant.ByteArray:
			return buffer( value.toByteArray() )
		if value.type() == QVariant.Int:
			return value.toInt()[0]
		if value.type() == QVariant.Double:
			return value.toDouble()[0]

		return unicode( value.toString() )

	def convertResult(self, value):
		return QVariant(value) if value != None else QVariant()

	def addBindValue(self, value):
		self._markParams.append( self.escapeValue(value) )

	def bindValue(self, key, value):
		self._namedParams[key] = self.escapeValue(value)

	def setQuery(self, sql):
		self.clear()
		self._sql = QString(sql)
		self._query = self._sql

	def exec_(self, sql=None):
		if sql != None:
			self.setQuery(sql)

		try:
			params = self._namedParams if len(self._namedParams) > 0 else self._markParams
			self._cursor.execute(u"%s" % self._query, params)
		except sqlite.Error, e:
			self._error = PySLError( str(e) )
			return False

		return True

	def lastQuery(self):
		return QString(self._sql)

	def lastError(self):
		return self._error

	def next(self):
		self._value = self._cursor.fetchone()
		return self._value != None

	def value(self, index):
		if index < len(self._value):
			val = self._value[index]
			from AutomagicallyUpdater import AutomagicallyUpdater
			return self.convertResult( AutomagicallyUpdater._getRealValue(val) )
		return None

	def lastInsertId(self):
		return self.convertResult(self._cursor.lastrowid)

	def rollback(self):
		self._dbconn.rollback()

	def commit(self):
		self._dbconn.commit()

	def __del__(self):
		if self._autocommit:
			self.commit()

