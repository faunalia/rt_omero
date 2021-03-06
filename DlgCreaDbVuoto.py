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

from ui.dlgCreaDbVuoto_ui import Ui_Dialog
from AutomagicallyUpdater import *
from ConnectionManager import PySLDatabase, SqlException
from Utils import Porting

from qgis.core import *
from qgis.gui import QgsMessageViewer
from osgeo import ogr
from ManagerWindow import ManagerWindow

import time
import zipfile
import os.path, sys
currentPath = os.path.dirname(__file__)

class DlgCreaDbVuoto(QDialog, Ui_Dialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)

		# setup the progress dialog
		self.progressDlg = QProgressDialog(self)
		self.progressDlg.setWindowModality(Qt.WindowModal)
		self.progressDlg.setMinimumDuration(0)
		self.progressDlg.setAutoClose(False)
		self.connect(self.progressDlg, SIGNAL("canceled()"), self.onCancel)

		# dict containing geometry tables and their informations
		self.geomTables = {
			ManagerWindow.TABLE_GEOM_ORIG : ('geometria', ManagerWindow.DEFAULT_SRID, 'POLYGON', 'XY'), 
			ManagerWindow.TABLE_GEOM_MODIF : ('geometria', ManagerWindow.DEFAULT_SRID, 'POLYGON', 'XY'), 
			'ZZ_COMUNI' : ('geometria', ManagerWindow.DEFAULT_SRID, 'MULTIPOLYGON', 'XY')
		}

		# get all "input shapefile" groups
		self.defaultComboValue = self.tr(u"Seleziona un valore")
		i=1
		self._groups = []
		while hasattr(self, 'filename%dEdit'%i):
			grp = (
				getattr(self, 'shape%dGroup'%i), 
				getattr(self, 'filename%dEdit'%i), 
				getattr(self, 'browse%dBtn'%i), 
				getattr(self, 'field%dCombo'%i), 
				getattr(self, 'prefix%dCombo'%i), 
			)
			self._groups += [grp]

			browsebtn = grp[2]
			self.connect(browsebtn, SIGNAL("clicked()"), self.browseFile)

			prefixcombo = grp[4]
			prefixcombo.clear()
			prefixcombo.addItems( ["RT020101", "RT020202", "RT020107"] )

			i += 1

		# get comuni boundary
		self._generalDataGroup = (
				self.authorEdit,
				self.projectNameEdit,
				self.targetEdit,
				self.bufferSpinBox,
		)
		self._confiniGroup = (
				self.filenameConfiniEdit,
				self.browseConfiniBtn,
				self.fieldCodiceIstatCombo,
		)
		self.connect(self.browseConfiniBtn, SIGNAL("clicked()"), self.confiniComunaliBrowseFile)
		#self.connect(self.fieldCodiceIstatCombo, SIGNAL("currentIndexChanged(int)"), self.readCodiciIstat)

	def browseFile(self):
		senderbtn = self.sender()

		lastUsedDir = AutomagicallyUpdater._getLastUsedDir("importshape")
		infile = QFileDialog.getOpenFileName(self, u"Seleziona uno shapefile di input", lastUsedDir, "Shapefile (*.shp)")
		if infile == "":
			return
		AutomagicallyUpdater._setLastUsedDir("importshape", infile)

		fields = self.getVectorFields(infile)
		if fields == None:
			QMessageBox.warning(self, "RT Omero", u"Il file selezionato non è uno shapefile valido")
			return

		for shapegrp, fnedit, browsebtn, fldcombo, prefixcombo in self._groups:
			if senderbtn != browsebtn:
				continue

			fnedit.setText(infile)
			fldcombo.clear()
			fldcombo.addItems(fields)
			break

	def confiniComunaliBrowseFile(self):
		senderbtn = self.sender()

		lastUsedDir = AutomagicallyUpdater._getLastUsedDir("importshape")
		infile = QFileDialog.getOpenFileName(self, u"Seleziona uno shapefile di input", lastUsedDir, "Shapefile (*.shp)")
		if infile == "":
			return
		AutomagicallyUpdater._setLastUsedDir("importshape", infile)

		fields = self.getVectorFields(infile)
		if fields == None:
			QMessageBox.warning(self, "RT Omero", u"Il file selezionato non è uno shapefile valido")
			return
		fields = sorted(fields, key=str)
		fields[:0] = [self.defaultComboValue]
		
		self.filenameConfiniEdit.setText(infile)
		self.fieldCodiceIstatCombo.clear()
		self.fieldCodiceIstatCombo.addItems(fields)
	
	def getVectorFields(self, vectorFile):
		hds = ogr.Open( unicode(vectorFile).encode('utf8') )
		if hds == None:
			return None

		names = []
		layer = hds.GetLayer(0)
		defn = layer.GetLayerDefn()

		for i in range(defn.GetFieldCount()):
			fieldDefn = defn.GetFieldDefn(i)
			names.append(fieldDefn.GetName())

		return names


	def getOutputPath(self):
		lastUsedDir = QFileInfo(AutomagicallyUpdater._getPathToDb()).path()
		output = QFileDialog.getSaveFileName(self, u"Salva un database", lastUsedDir, "SQLite database (*.db3 *.sqlite);;Tutti i file (*)")
		if not output:
			return
		if output[-4:] != ".db3" and output[-7:] != ".sqlite" and output[-3:] != ".db":
			output += ".db3"
		return output

	def accept(self):
		# check input data
		if self.authorEdit.text() == "":
			QMessageBox.warning(self, "RT Omero", u"Specificare l'autore del progetto")
			return

		if self.projectNameEdit.text() == "":
			QMessageBox.warning(self, "RT Omero", u"Specificare il nome progetto")
			return

		if self.targetEdit.text() == "":
			QMessageBox.warning(self, "RT Omero", u"Specificare il target del progetto")
			return

		# check if a codiceIstat name has bee selected
		if self.fieldCodiceIstatCombo.currentText() == self.defaultComboValue or self.fieldCodiceIstatCombo.currentText() == "":
			QMessageBox.warning(self, "RT Omero", u"Specificare il nome della colonna Codici Istat")
			return
		
		self.outputPath = self.getOutputPath()
		if not self.outputPath:
			return

		self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled(False)
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		self.resetProgress(None, "Creazione database %s in corso..." % self.outputPath )
		self.progressDlg.forceShow()

		# run the work on a different thread
		self.mythread = CreateDbThread(self.outputPath, self._groups, self.geomTables, self._confiniGroup, self._generalDataGroup, self)
		self.connect(self.mythread, SIGNAL("messageSent"), self.onMessage)
		self.connect(self.mythread, SIGNAL("exceptionRaised"), self.reRaiseExceptions)	# error handler
		self.connect(self.mythread, SIGNAL("resetProgress"), self.resetProgress)
		self.connect(self.mythread, SIGNAL("updateProgress"), self.updateProgress)
		self.connect(self.mythread, SIGNAL("creationDone"), self.workDone)
		self.connect(self.mythread, SIGNAL("finished()"), self.stop)
		#self.mythread.run()	###DEBUG
		self.finished = False
		self.mythread.start()
		#self.mythread.run()
		
		while not self.finished:
			qApp.processEvents()
			time.sleep(0.1)
			
	def workDone(self, ok, log):
		self.finished = True
		if ok:
			title = u"<h3>Creazione database <em>'%s'</em> completata.</h3>" % self.outputPath
		else:
			title = "<h3>Errore durante la creazione del database <em>'%s'</em>.</h3>" % self.outputPath

		# display the log
		if log != "":
			vw = QgsMessageViewer(self)
			vw.setTitle("RT Omero")
			vw.setMessageAsHtml( u"%s\n%s" % (title, log) )
			vw.exec_()
		else:
			self.onMessage(0 if ok else 2, title)

		if ok:
			QDialog.accept(self)

	def stop(self):
		self.mythread.deleteLater()
		QApplication.restoreOverrideCursor()
		self.buttonBox.button( QDialogButtonBox.Ok ).setEnabled(True)
		self.progressDlg.hide()

	def onCancel(self):
		self.mythread.terminate()
		self.stop()

	def reRaiseExceptions(self, exc_info):
		""" error handler: re-raise the exception """
		raise exc_info[1], None, exc_info[2]

	def onMessage(self, level, msg):
		msgbox = QMessageBox.information
		if level == 1:
			msgbox = QMessageBox.warning
		elif level == 2:
			msgbox = QMessageBox.critical
		msgbox(self, "RT Omero", msg)

	def resetProgress(self, maximum=None, label=None):
		self.progressDlg.reset()
		if label is not None:
			self.progressDlg.setLabelText( label )
		if maximum is not None:
			self.progressDlg.setMaximum( maximum )
		else:
			self.progressDlg.setRange(0, 0)

	def updateProgress(self, val=None):
		self.progressDlg.setValue( val if val is not None else self.progressDlg.value()+1 )


#class CreateDbThread(QDialog):	###DEBUG
#class CreateDbThread(QObject):	###DEBUG
class CreateDbThread(QThread):

	def __init__(self, dbpath, inputGroups, geomTables, confiniGroup, generalDataGroup, parent=None):
		#QObject.__init__(self, parent)	###DEBUG
		#QDialog.__init__(self, parent)
		QThread.__init__(self, parent)
		self.dbpath = dbpath
		self.inputGroups = inputGroups
		self.geomTables = geomTables
		self.authorEdit, self.projectNameEdit, self.targetEdit, self.bufferSpinBox = generalDataGroup
		self.filenameConfiniEdit, self.browseConfiniBtn, self.fieldCodiceIstatCombo = confiniGroup
		self.log = []

	def run(self):
		# Let's catch all the exceptions to avoid crashes! 
		# QGis tries to display a dialog with the traceback for uncaugth exceptions 
		# but GUI can't be drawn out of the main thread
		try:
			self.exec_()
		except:
			self.emit(SIGNAL("exceptionRaised"), sys.exc_info() )

	def exec_(self):
		# if the file exists remove it
		finfo = QFileInfo(self.dbpath)
		if finfo.exists():
			if not finfo.isReadable() or not finfo.isWritable():
				self.emit(SIGNAL("messageSent"), 1, u"Impossibile scrivere nella directory selezionata.")
				return
			QFile.remove(self.dbpath)

		# create an empty database
		conn = PySLDatabase(self.dbpath)
		if not conn.isValid():
			self.emit(SIGNAL("messageSent"), 2, u"Errore connettendosi al database: \n%s" % conn.error())
			return

		# add spatial metadata
		query = conn.getQuery()
		if not query.exec_("SELECT InitSpatialMetadata(1);"):
			query.exec_("SELECT InitSpatialMetadata();")
		del query

		# run the scripts
		scriptsPath = unicode(os.path.join(currentPath, "docs", "scripts_create_db_spatialite.zip"))
		if not QFile.exists( scriptsPath ):
			self.emit(SIGNAL("messageSent"), 2, u"Impossibile trovare l'archivio contenente gli scripts." )
			return

		ok = self.runScriptsAndFill( scriptsPath, conn )
		log = u""
		for line in  self.log:
			log += u"%s\n" %line
		self.emit(SIGNAL("creationDone"), ok, log )
		return


	def runScriptsAndFill(self, pathToScripts, conn):
		try:
			# scripts are into a zip archive
			zf = zipfile.ZipFile( unicode(pathToScripts) )
			if len( zf.namelist() ) <= 0:
				raise zipfile.BadZipfile( "no files in the archive" )

			count = len(zf.namelist()) + 2
			index = 0
			for name in sorted(zf.namelist()):
				f = zf.open( zf.getinfo( name ), 'r' )
				if not f:
					raise zipfile.BadZipfile( u"unable to extract %s, the file may be broken" % name )

				# run the sql script file
				index += 1
				self.emit(SIGNAL("resetProgress"), None, "(%d/%d) Esecuzione dello script file %s..." % (index, count, name) )

				query = conn.getQuery(False)	# disable autocommit
				try:
					if not query.executeScript( unicode(f.read(), 'utf8') ):
						raise SqlException( u"Errore durante l'esecuzione del file %s: \n%s" % (name, query.lastError().text()) )
					conn.commit()
				except:
					conn.rollback()
					raise
				finally:
					f.close()			

				# add geometry columns after the table creation
				if Porting.str(name).startswith("01"):
					index += 1
					self.emit(SIGNAL("resetProgress"), len(self.geomTables), "(%d/%d) Creazione colonne geometriche..." % (index, count) )

					for tbl, geom in self.geomTables.iteritems():
						geomcol, srid, geomtype, dim = geom[:4]
						query = conn.getQuery(False)
						sql = u"SELECT AddGeometryColumn('%s', '%s', %d, '%s', '%s')" % (tbl, geomcol, srid, geomtype, dim)
						if not query.exec_( sql ):
							raise SqlException( u"Impossibile aggiungere una colonna geometrica alla tabella %s:\n%s" % (tbl, query.lastError().text()) )
						self.emit(SIGNAL("updateProgress"))

				# populate geometry tables before create triggers
				if Porting.str(name).startswith("03"):
					index += 1
					self.emit(SIGNAL("resetProgress"), None, "(%d/%d) Riempimento tabelle geometriche..." % (index, count) )

					if not self.populateGeometryTables(conn):
						return False

			conn.commit()

			# init ZZ_COMUNI and ZZ_DISCLAIMER with data related to selected Municipio
			self.emit(SIGNAL("resetProgress"), None, "Inizializializzazione ZZ_COMUNI" )
			if not self.initZZ_COMUNI(conn):
				return False

			# set ZZ_DISCLAIMER values
			self.emit(SIGNAL("resetProgress"), None, "Inizializializzazione ZZ_DISCLAIMER" )
			if not self.initZZ_DISCLAIMER(conn):
				return False

			conn.commit()

		except (IOError, KeyError, zipfile.BadZipfile), e:
			self.emit(SIGNAL("messageSent"), 2, u"Impossibile estrarre dall'archivio contenente gli scripts.\n\nError message: %s" % e.message )
			return False

		except SqlException, e:
			conn.rollback()
			self.emit(SIGNAL("messageSent"), 2, e.message )
			return False

		return True

	def populateGeometryTables(self, conn):
		geomOrigSrid = self.geomTables[ManagerWindow.TABLE_GEOM_ORIG][1]
		insertSql = u"INSERT INTO %s (CODICE, geometria) VALUES (?, ST_GeomFromText(?, ?))" % ManagerWindow.TABLE_GEOM_ORIG

		query = conn.getQuery(False)	# disable autocommit

		self.log.append( u"<h3>Log di creazione nuovo database</h3><ul>" )
		errorCount = 0

		for shapegrp, fnedit, browsebtn, fldcombo, prefixcombo in self.inputGroups:
			shppath = fnedit.text()
			fldname = fldcombo.currentText()
			prefix = prefixcombo.currentText()

			if not shapegrp.isChecked() or shppath == "" or fldname == "" or prefix == "":
				continue

			self.log.append( u"<li><p><strong>Importazione geometrie dal layer '%s'...</strong></p>" % shppath )

			shpvl = QgsVectorLayer(shppath, QFileInfo(shppath).fileName(), 'ogr')
			if not shpvl or not shpvl.isValid():
				self.log.append( u"<p style='color:red'>Impossibile caricare il layer '%s': il layer non è valido ed è stato ignorato</p>" % shppath )
				errorCount += 1
				continue

			crs = shpvl.crs() if hasattr(shpvl, 'crs') else shpvl.srs()
			shpSrid = crs.postgisSrid()
			if shpSrid != geomOrigSrid:
				self.log.append( u"<p style='color:red'>Il layer '%s' ha un sistema di riferimento differente da quanto richiesto ed è stato ignorato: trovato %d, richiesto %d</p>" % (shppath, shpSrid, geomOrigSrid) )
				continue

			# add the features to the table on the database
			self.emit(SIGNAL("resetProgress"), shpvl.dataProvider().featureCount())

			feat = QgsFeature()
			fldindex = shpvl.dataProvider().fieldNameIndex(fldname)
			# check --------------> shpvl.select([fldindex])

			errors = []
			currentProgress = 0
			emitStep = shpvl.dataProvider().featureCount() / 10
			for feat in shpvl.getFeatures( QgsFeatureRequest().setSubsetOfAttributes([fldindex]) ):
				idval = Porting.str( feat.attributes()[fldindex] )

				newidval = u"%s%s" % (prefix, idval)
				#wkb = QByteArray( feat.geometry().asWkb() )
				wkt = "%s" % feat.geometry().exportToWkt()

				query.prepare( insertSql )
				query.addBindValue( newidval )
				query.addBindValue( wkt )
				query.addBindValue( int(shpSrid) )

				if not query.exec_():
					errorCount += 1
					errors.append( u"<p style='color:red'>Errore aggiungendo la geometria [%s = %s]: %s</p>" % (fldname, idval, query.lastError().text()) )

				if len(errors) >= 100:
					break

				# send progress update only evety tenth features to avoid QT crash on WIN7
				currentProgress +=1
				if (currentProgress % emitStep) == 0:
					self.emit(SIGNAL("updateProgress"), currentProgress)

			if len(errors) == 0:
				self.log.append( "<p>completata correttamente.</p>" )
			else:
				self.log.append( errors )

			if errorCount > 150:
				self.log.append( u"<li><p><strong>Si sono verificati troppi errori, il processo sarà stato interrotto.</strong></p>" )
				break

		return errorCount <= 0

	def initZZ_COMUNI(self, conn):
		query = conn.getQuery(False)	# disable autocommit
		self.log.append( u"<li><p><strong>Inizializzazione confini comunali</strong></p>" )

		# get values
		codiciIstat = self.readCodiciIstat()
		fieldName = self.fieldCodiceIstatCombo.currentText()
		
		# get srid of the current shape
		geomOrigSrid = self.geomTables[ManagerWindow.TABLE_GEOM_ORIG][1]
		filename = self.filenameConfiniEdit.text()
		shpvl = QgsVectorLayer(filename, QFileInfo(filename).fileName(), 'ogr')
		if not shpvl or not shpvl.isValid():
			self.log.append( u"<p style='color:red'>Impossibile caricare il layer '%s': il layer non è valido ed è stato ignorato</p>" % filename )
			return False

		crs = shpvl.crs() if hasattr(shpvl, 'crs') else shpvl.srs()
		shpSrid = crs.postgisSrid()
		if shpSrid != geomOrigSrid:
			self.log.append( u"<p style='color:red'>Il layer '%s' ha un sistema di riferimento differente da quanto richiesto: trovato %d, richiesto %d</p>" % (filename, shpSrid, geomOrigSrid) )
			return False
		
		# get values in the selected column
		driver = ogr.GetDriverByName("ESRI Shapefile")
		dataSource = driver.Open( str(filename).encode('utf8') )
		layer = dataSource.GetLayer()

		# for each codiceIstat
		for codiceIstat in codiciIstat:
			# check if record is available in zz_comuni
			selectSql = u"SELECT * FROM ZZ_COMUNI WHERE ISTATCOM = '%s';" % codiceIstat
			query.prepare( selectSql )
			if not query.exec_():
				self.log.append( u"<p style='color:red'>Errore cercando il record ZZ_COMUNI [ISTATCOM = %s]: %s</p>" % (codiceIstat, query.lastError().text()) )
				return False
 			if not query.next():
 				self.log.append( u"<p style='color:orange'>Non trovo il record in ZZ_COMUNI da aggiornare [ISTATCOM = %s]</p>" % codiceIstat )
			 	continue
			 	
			# get geometry from the first feature that match attribute filter
			fieldFilter = str( "%s = '%s'" % (fieldName, codiceIstat) ) # <- can't use unicode to specify values in the filter
			layer.SetAttributeFilter( fieldFilter.encode('utf8') )
			newgeom = None
			wkt = None
			for feature in layer:
				geom = feature.GetGeometryRef()
				# if not convert in multipart
				wkt = geom.ExportToWkt()
				if wkt == None:
					self.log.append( u"<p style='color:red'>Non trovo la la geometria nel file %s per il codice istat %s</p>" % (filename, codiceIstat) )
					return False
				
				tempgeom = QgsGeometry.fromWkt(wkt)
				if not tempgeom:
					self.log.append( u"<p style='color:red'>Non posso convertire la geometria da Wkt per il codice istat %s</p>" % codiceIstat )
					return False
				if newgeom:
					newgeom = newgeom.combine(tempgeom)
					if not newgeom:
						self.log.append( u"<p style='color:red'>Non posso fare la union delle geometrie per il codice istat %s</p>" % codiceIstat )
						return False
				else:
					newgeom = tempgeom
			
			if not newgeom:
				self.log.append( u"<p style='color:red'>Nessuna geometria trovata per il codice istat %s</p>" % codiceIstat )
				return False
			
			# add geometry for selected codiceIstat
			updateSql = u"UPDATE ZZ_COMUNI SET geometria=CastToMulti(ST_GeomFromText('%s', %i)) WHERE ISTATCOM = '%s';" % (newgeom.exportToWkt(), int(shpSrid), codiceIstat)
			query.prepare( updateSql )
	
			if not query.exec_():
				self.log.append( u"<p style='color:red'>Errore aggiungendo la geometria ZZ_COMUNI [ISTATCOM = %s]: %s</p>" % (codiceIstat, query.lastError().text()) )
				return False
			
		self.log.append( "<p>completata correttamente.</p>" )
		return True


	def readCodiciIstat(self):
		# get selected field name for comuni
		fieldName = self.fieldCodiceIstatCombo.currentText()
		
		# get values in the selected column
		filename = self.filenameConfiniEdit.text()
		driver = ogr.GetDriverByName("ESRI Shapefile")
		dataSource = driver.Open( str(filename).encode('utf8') )
		layer = dataSource.GetLayer()
		
		values = []
		for feature in layer:
			values.append( feature.GetField( str(fieldName) ) )
		values = sorted(values, key=str)
		return [str(v) for v in values]


	def initZZ_DISCLAIMER(self, conn):
		self.log.append( u"<li><p><strong>Inizializzazione dati di progetto</strong></p>" )

		# for each codiceIstat (should be only ONE!!!!)
		values = (
			self.projectNameEdit.text(), 
			self.targetEdit.text(), 
			self.authorEdit.text(), 
			self.bufferSpinBox.value(), 
			str( QDate.currentDate().toString( 'dd/MM/yyyy' ) ),
		)

		query = conn.getQuery(False)	# disable autocommit
		sql = "UPDATE ZZ_DISCLAIMER SET DATABASE = ?, TARGET = ?, AUTHOR = ?,  BUFFER = ?, DB_CREATION_DATE = ? ;"
		query.prepare( sql )
		for value in values:
			query.addBindValue( value )
			
		if not query.exec_():
			self.log.append( u"<p style='color:red'>Errore aggiornando la tabella ZZ_DISCLAIMER: %s</p>" % query.lastError().text() )
			return False
		
		self.log.append( "<p>completata correttamente.</p>" )
		return True


