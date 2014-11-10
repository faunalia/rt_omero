# -*- coding: utf-8 -*-

"""
/***************************************************************************
Name                 : Omero RT
Description          : Omero plugin
Date                 : October 21, 2011 
copyright            : (C) 2011 by Giuseppe Sucameli (Faunalia)
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
import re
import os
import inspect
from osgeo import gdal

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from qgis.core import *

from DlgWaiting import DlgWaiting
from ManagerWindow import ManagerWindow 
from AutomagicallyUpdater import *

class DlgWmsLayersManager(DlgWaiting):

	def __init__(self, iface, parent=None):
		DlgWaiting.__init__(self, parent)
		self.iface = iface
		self.canvas = self.iface.mapCanvas()

	def run(self):
		self.reset()
		try:
			ret = self.switchToOnlineMode() if ManagerWindow.instance.offlineMode else self.switchToOfflineMode()
			self.onProgress(-1)
		finally:
			self.finished = True
		self.done(ret)

	def switchToOfflineMode(self):
		# offline mode is already on
		if ManagerWindow.instance.offlineMode:
			return False

		def saveWorldFile(imgpath, pxdim, extent):
			""" create a worldfile """
			out = open( u"%s.wld" % imgpath[:-4], 'w')
			out.write( u"%.16f\n%.16f\n%.16f\n%.16f\n%.16f\n%.16f" % (pxdim, 0.0, 0.0, -pxdim, extent.xMinimum(), extent.yMaximum()) )
			out.close()

		def buildAllPyramids(layer):
			""" build raster pyramids """
			evloop = QEventLoop()
			thread = BuildPyramidsThread(layer)
			QObject.connect( thread, SIGNAL("finished()"), evloop.quit )
			thread.start()
			evloop.exec_()


		default_scale = 1500	# 1:1500
		default_extent = 2000	# 2km
		reqpxdim = 1200	# 1200px

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		# disable the rendering
		prevRenderFlag = self.canvas.renderFlag()
		self.canvas.setRenderFlag( False )

		# disable raster icons
		settings = QSettings()
		prevRasterIcons = settings.value("/qgis/createRasterLegendIcons", True, type=bool)
		settings.setValue("/qgis/createRasterLegendIcons", False)


		# backup %cache% folder (move it to %cache%.old)
		# then remove it only if the process ends successfully
		cache_path = AutomagicallyUpdater.getPathToCache()
		dircache = QDir(cache_path)
	
		dircache_name = dircache.dirName()
		if dircache.cd( ".." ) and dircache.rename(dircache_name, u"%s.old" % dircache_name):
			dircache.mkdir( dircache_name )

		# store current zoom
		prevScale = self.canvas.scale()
		# get central point
		rect = self.canvas.extent()
		center = QgsPoint(rect.xMinimum() + rect.width()/2, rect.yMinimum() + rect.height()/2)
		
		# dump the wms layers' info from online repository to cache file
		layersinfo = self.retrieveWmsLayerList()
		wmslistfn = QDir(cache_path).absoluteFilePath("zz_wms.list.txt")
		with open(unicode(wmslistfn), 'w') as f:
			if layersinfo is not None:
				import json
				json.dump(layersinfo, f)
				
		cached_images = {}
		try:
			# get the list of wms layers to be switched
			wms_layers = []
			legend = self.iface.legendInterface()
			for layer in reversed(legend.layers()):
				p = layer.dataProvider()
				if p.name() != "wms":
					continue

				prop = layer.customProperty( "loadedByOmeroRTPlugin" )
				if not prop and legend.isLayerVisible(layer):
					# a wms layer not loaded by omero, don't cache if it's hidden
					prop = u"WMS_OFFLINE %s" % layer.source()
					wms_layers.append( (layer, default_scale, default_extent, prop) )

				elif prop.startswith( "RLID_WMS" ) and not prop.startswith( "RLID_WMS_OFFLINE" ):
					# a wms layer loaded by omero
					# get cache scale and extent for the layer
					if layersinfo is None:
						continue
						
					# get layer info by order
					order = int(prop[9:])
					linfos = filter(lambda x: x['order'] == order, layersinfo)
					if len(linfos) <= 0:
						continue
					# use just the first item
					linfo = linfos[0]
						
					scale, extent = linfo['cache_scale'], linfo['cache_extent']
					if scale is None:
						continue
					if extent is None:
						extent = default_extent

					prop = u"RLID_WMS_OFFLINE %s" % order
					wms_layers.append( (layer, scale, extent, prop) )


			# convert each wms to an offline layer
			for idx_layer, val_layer in enumerate(wms_layers):
				layer, scale, extent, prop = val_layer

				# zoom to scale
				self.canvas.zoomScale( scale )

				m_px = self.canvas.getCoordinateTransform().mapUnitsPerPixel()
				reqdim = reqpxdim*m_px	# tile extent in map units

				# calculate the number of tiles to be downloaded
				n_float = extent/reqdim
				n = int(n_float)
				n = n+1 if n_float > n else n

				# set title and progressbar range
				self.setWindowTitle( self.tr( "[%d/%d] Download in corso..." % ( idx_layer+1, len(wms_layers) ) ) )
				self.setRange( 0, n*n+1 )

				# bottom-left point
				bl = QgsPoint(center.x()-reqdim*n/2.0, center.y()-reqdim*n/2.0)

				name = layer.name()
				visible = legend.isLayerVisible(layer)
				layerid = layer.id()
				source = layer.source()
				p = layer.dataProvider()

				# use a vrt catalog to store the cached layer instead
				# of write all the tiles onto a single image
				escaped_name = re.sub( "[^a-zA-Z0-9]", "_", name ).lower()[:100]
				use_catalog = True
				if not use_catalog:
					out_path = QDir(cache_path).absoluteFilePath( u"%s.png" % escaped_name )
					out_image = QImage( reqpxdim*n, reqpxdim*n, QImage.Format_ARGB32 )
				else:
					out_path = QDir(cache_path).absoluteFilePath( u"%s.vrt" % escaped_name )

				# get all tiles disabling enable_render_caching because if enabled
				# rendering is not produced (due to some characteristic of draw())
				prevRenderCache = settings.value("/qgis/enable_render_caching", False, type=bool)
				settings.setValue("/qgis/enable_render_caching", False)
				
				in_images = []
				for i in range( n*n ):
					row, col = i/n, i%n
					posx, posy = reqdim*row, reqdim*col
					toposx, toposy = reqdim*(row+1), reqdim*(col+1)
					reqextent = QgsRectangle(bl.x()+posx, bl.y()+posy, bl.x()+toposx, bl.y()+toposy)

					# get and store image
					imagepart = p.draw( reqextent, reqpxdim, reqpxdim )
					if not use_catalog:
						# seems the following lines do not work as expected
						painter = QPainter(out_image)
						painter.drawImage(posx, posy, imagepart, reqpxdim, reqpxdim)
						painter.end()

						# save worldfile if upper-left corner
						if row == n-1 and col == 0:
							saveWorldFile(out_path, m_px, reqextent)

					else:
						in_path = QDir(cache_path).absoluteFilePath( u"%s_%s.png" % (i, escaped_name) )
						imagepart.save( in_path, "PNG" )
						in_images.append( unicode(in_path) )
						saveWorldFile(in_path, m_px, reqextent)

					self.onProgress()
				
				# re set to previous enable_render_caching  configuration
				settings.setValue("/qgis/enable_render_caching", prevRenderCache)

				saved = False
				if not use_catalog:
					saved = out_image.save( out_path, "PNG" )
				else:
					# create the catalog from tiles
					cmd = ["gdalbuildvrt", "-overwrite"]
					
					# force srs to avoid warning message on loading vrt raster - fix #237 
					if int(gdal.VersionInfo('VERSION_NUM')) >= 1100000:
						srs = ManagerWindow.instance.DEFAULT_SRID
						srsCmd = [ "-a_srs", "epsg:%d" % srs ]
						cmd.extend( srsCmd )
					cmd.extend( [ unicode(out_path) ] )

					cmd.extend( in_images )
					import subprocess
					saved = (0 == subprocess.call( cmd ))
				self.onProgress()

				if saved:				
					# remove the online layer
					ManagerWindow._removeMapLayer(layerid)

					# override projection behaviour: do not ask for CRS
					settings = QSettings()
					oldProjectionBehaviour = settings.value( "/Projections/defaultBehaviour", "prompt", type=str )
					settings.setValue( "/Projections/defaultBehaviour", "useProject" )
					# add the offline layer
					try:
						layer = self.iface.addRasterLayer( out_path, "CACHED - %s" % name )
					finally:
						# restore projection behaviour
						settings.setValue( "/Projections/defaultBehaviour", oldProjectionBehaviour )
						
					if layer and layer.isValid():
						# set the layer custom property
						layer.setCustomProperty( "loadedByOmeroRTPlugin", prop )
						if prop.startswith( "WMS_OFFLINE" ):
							cached_images[out_path] = source

						elif prop.startswith( "RLID_WMS_OFFLINE" ):
							order = int( prop.split(" ")[1] )
							ManagerWindow.RLID_WMS[order] = ManagerWindow._getLayerId(layer)

						# show/hide the layer 
						legend.setLayerVisible(layer, visible)

						# set to build all available raste
						# set title and progressbar range 
						# then build all available raster pyramids
						self.setWindowTitle( self.tr( "[%d/%d] Costruzione piramidi..."  % ( idx_layer+1, len(wms_layers) ) ) )
						self.setRange( 0, 0 )	#self.setRange( 0, len(pyramids) )
						buildAllPyramids(layer)

# 						# set the transparent band
# 						p = layer.dataProvider()
# 						if True:
# 							layer.setTransparentBandName( "Band 4" )
# 						else:
# 							for i in range(layer.bandCount()):
# 								# there're no python bindings for both 
# 								# QgsRasterDataProvider::colorInterpretation() and
# 								# QgsRasterDataProvider::generateBandName() 
# 								if p.colorInterpretation(i) == QgsRasterDataProvider.AlphaBand:
# 									layer.setTransparentBandName( p.generateBandName(i) )
# 									break

			AutomagicallyUpdater.setCachedExternalWms( cached_images )
			ManagerWindow.instance.offlineMode = True

		except:
			dircache.rename(u"%s.old" % dircache_name, dircache_name)
			raise

		else:
			import shutil
			shutil.rmtree(u"%s.old" % cache_path)

		finally:
			# restore prev zoom
			self.canvas.zoomScale(prevScale)
			self.canvas.setRenderFlag( prevRenderFlag )
			# restore the raster icons
			settings.setValue("/qgis/createRasterLegendIcons", prevRasterIcons)

			QApplication.restoreOverrideCursor()

		return True

	def switchToOnlineMode(self):
		# check if online mode is already on
		if not ManagerWindow.instance.offlineMode:
			return False

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		prevRenderFlag = self.canvas.renderFlag()
		self.canvas.setRenderFlag( False )

		try:
			cached_images = AutomagicallyUpdater.getCachedExternalWms()

			# remove offline WMS layers, so the plugin can add the online ones
			legend = self.iface.legendInterface()
			for layer in reversed(legend.layers()):
				p = layer.dataProvider()
				if p.name() != "gdal":
					continue

				name = layer.name()
				visible = legend.isLayerVisible(layer)
				layerid = layer.id()

				prop = layer.customProperty( "loadedByOmeroRTPlugin" )
				if not prop:
					# a wms layer not loaded by omero
					continue

				elif prop.startswith( "RLID_WMS_OFFLINE" ):
					# a wms layer loaded by omero, remove it
					ManagerWindow._removeMapLayer( layerid )
					continue

				elif prop.startswith( "WMS_OFFLINE" ):
					# an external cached wms
					if not cached_images.has_key( layer.source() ):
						continue

				else:
					continue

				# remove the offline layer
				ManagerWindow._removeMapLayer(layerid)

			ManagerWindow.instance.offlineMode = False

		finally:
			self.canvas.setRenderFlag( prevRenderFlag )
			QApplication.restoreOverrideCursor()

		return True

	@classmethod
	def loadWmsLayers(self, firstStart):
	
		def isHostAccessible(host):
			""" check whether a host can be reached """
			from PyQt4.QtNetwork import QHostInfo
			info = QHostInfo.fromName( host )
			if info.error() == QHostInfo.NoError:
				return True
			return False

		# check if offline mode changed
		if not firstStart and ManagerWindow.instance.offlineMode != AutomagicallyUpdater.offlineMode():

			# show progress bar
			if not DlgWmsLayersManager( ManagerWindow.instance.iface ).exec_():
				# no switch has occurred
				return True

			# a mode switch has occurred
			# now AutomagicallyUpdater.offlineMode() == self.offlineMode
			if AutomagicallyUpdater.offlineMode():
				# we are now in offline mode
				return True

		else:
			ManagerWindow.instance.offlineMode = AutomagicallyUpdater.offlineMode()

		cache_path = AutomagicallyUpdater.getPathToCache()

		# get the list of already loaded WMS layers
		loaded_wms = []
		for order, rlid in ManagerWindow.RLID_WMS.iteritems():
			if QgsMapLayerRegistry.instance().mapLayer( rlid ) != None:
				loaded_wms.append( order )

		layersinfo = self.retrieveWmsLayerList( excludeList = loaded_wms )
		if layersinfo is None:
			return False
		
		for l in layersinfo:
			order, url, title = l['order'], l['url'], l['title'], 
			layers, styles, format, crs = l['layers'], l['styles'], l['format'], l['crs']

			if not ManagerWindow.instance.offlineMode:
				# online mode, load layers from the wms server
				if QGis.QGIS_VERSION[0:3] <= "1.8":	# handle QGIS API changes
					rl = QgsRasterLayer(0, url, title, 'wms', layers, styles, format, crs)
				else:
					uri = QgsDataSourceURI()
					uri.setParam("url", url)
					uri.setParamList("layers", layers)
					uri.setParamList("styles", styles)
					uri.setParam("format", format)
					uri.setParam("crs", crs)
					
					rl = QgsRasterLayer(str(uri.encodedUri()), title, 'wms')

				prop = "RLID_WMS %s" % order
				
			else:
				# offline mode, load layers from local cache
				escaped_title = re.sub( "[^a-zA-Z0-9]", "_", title ).lower()[:100]
				vrt_path = QDir( cache_path ).absoluteFilePath( u'%s.vrt' % escaped_title )
				if not QFileInfo( vrt_path ).exists():
					continue
					
				# override projection behaviour: do not ask for CRS
				settings = QSettings()
				oldProjectionBehaviour = settings.value( "/Projections/defaultBehaviour", "prompt", type=str )
				settings.setValue( "/Projections/defaultBehaviour", "useProject" )
				try:
					rl = QgsRasterLayer( vrt_path, u"CACHED - %s" % title )
				finally:
					# restore projection behaviour
					settings.setValue( "/Projections/defaultBehaviour", oldProjectionBehaviour )
				
				#rl.setTransparentBandName( "Band 4" )
				prop = "RLID_WMS_OFFLINE %s" % order

			if not rl.isValid():
				continue

			ManagerWindow.RLID_WMS[order] = ManagerWindow._getLayerId(rl)
			ManagerWindow._addMapLayer(rl)
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( rl, False )

			# set custom property
			rl.setCustomProperty( "loadedByOmeroRTPlugin", prop )
			
		return True
		
	@classmethod
	def retrieveWmsLayerList(self, excludeList=None, retrieveList=None):
		if excludeList is None:
			excludeList = []
		if retrieveList is None:
			# empty list means retrieve ALL the layers
			retrieveList = []

		layersinfo = []
		
		if ManagerWindow.instance.offlineMode:
			# offline mode is on, get the wms list from cache
			cache_path = AutomagicallyUpdater.getPathToCache()
			wmslistfn = QDir(cache_path).absoluteFilePath("zz_wms.list.txt")

			cachedinfo = []
			try:
				with open(unicode(wmslistfn), 'r') as f:
					import json
					cachedinfo = json.load(f)
			except (IOError, ImportError, ValueError) as e:
				ManagerWindow._logMessage("RT Omero", u"Impossibile recuperare la lista dei layer WMS dal file %s.\n%s" % ( wmslistfn, unicode(e)) )

			for linfo in cachedinfo:
				# check whether retrieve or not the layer
				order = linfo['order']
				if order in excludeList:
					continue
				if len(retrieveList) > 0 and order not in retrieveList:
					continue
				
				layersinfo.append( linfo )

		else:
			# online mode, get the WMS layer list from online repository 
			repourl = AutomagicallyUpdater.getWMSRepositoryUrl()
			if repourl:
				# get layers from WMS repository by URL			
				def downloadFinished(reply, evloop, done):
					ok = True
					if reply.error() != QNetworkReply.NoError:
						ManagerWindow._logMessage("RT Omero", u"Impossibile recuperare la lista dei layer WMS dal server.\n" +
								u"Error code: %s" % reply.error() )
						ok = False
					else:
						status = reply.attribute( QNetworkRequest.HttpStatusCodeAttribute )
						if status is not None and status > 400:
							phrase = reply.attribute( QNetworkRequest.HttpReasonPhraseAttribute )
							ManagerWindow._logMessage("RT Omero", u"Impossibile recuperare la lista dei layer WMS dal server.\n" +
									u"Status: %s\nReason phrase: %s" % (status, phrase ) )
							ok = False
					
					done[0] = ok
					evloop.exit()
				
				done = [False] # trick to pass the value by reference
				evloop = QEventLoop()
				
				req = QNetworkRequest( QUrl(repourl) )
				reply = QgsNetworkAccessManager.instance().get( req )
				reply.finished.connect( lambda: downloadFinished(reply, evloop, done) )

				# wait until the download finishes
				evloop.exec_()
				if done[0]:
					import zipfile
					try:
						# we have the data, let's create the zip file
						tmp = QTemporaryFile()
						tmp.setFileTemplate( tmp.fileTemplate() + ".zip" )
						tmp.open( QIODevice.ReadWrite )
						tmp.write( reply.readAll() )
						tmp.close()
					
						# open the zip file and get the csv/txt file containing the WMS list
						zf = zipfile.ZipFile(unicode(tmp.fileName()), 'r')
					
						# the file within the zip has the same basename of the url file path
						csv_data = None
						for name in sorted(zf.namelist()):
							f_basename = unicode(QFileInfo( QUrl(repourl).path() ).completeBaseName())
							if not name.lower().startswith( f_basename.lower() ):
								continue
							
							# try to get the file content
							import csv
							try:
								with zf.open( zf.getinfo( name ), 'r' ) as csv_f:
									csvreader = csv.reader(csv_f, delimiter=',', quotechar="'")
									for row in csvreader:
										if row[0] == '*':
											# XXX: the file ends with a star (*) as EOF. why???
											break

										linfo = {}
										linfo['order'] = int(row[0])
										
										# check whether retrieve or not the layer
										if linfo['order'] in excludeList:
											continue
										if len(retrieveList) > 0 and linfo['order'] not in retrieveList:
											continue

										linfo['title'] = row[1]
										linfo['url'] = row[2]
										
										linfo['layers'] = row[3].split(",")
										linfo['styles'] = [ '' ] * len( linfo['layers'] )
										linfo['crs'] = row[4]
										linfo['format'] = "image/%s" % row[5].lower()
										linfo['transparent'] = row[6]
										linfo['version'] = row[7]
										
										try:
											linfo['cache_scale'] = int(row[8])
										except ValueError:
											linfo['cache_scale'] = None
										try:
											linfo['cache_extent'] = int(row[9])
										except ValueError:
											linfo['cache_extent'] = None
										
										layersinfo.append( linfo )
										
										# update ZZ_WMS entries replacing the ones with the same order number
										query = AutomagicallyUpdater.Query( u'DELETE FROM ZZ_WMS WHERE "ORDER" = ?' , linfo['order'] )
										query.getQuery().exec_()
										query = AutomagicallyUpdater.Query( u'''INSERT INTO ZZ_WMS
												("ORDER", TITLE, URL, LAYERS, SRS, FORMAT, TRANSPARENT, VERSION, CACHE_SCALA, CACHE_ESTENSIONE)
												VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''' , row )
										query.getQuery().exec_()
									
							except IOError:
								continue

					except (IOError, zipfile.BadZipfile) as e:
						# unable to open the zip file
						ManagerWindow._logMessage("RT Omero", u"Impossibile recuperare la lista dei layer WMS dal server.\n%s" % unicode(e) )
				
		if len(layersinfo) <= 0:
			# unable to retrieve the list, get values from ZZ_WMS table
			ManagerWindow._logMessage("RT Omero", u"Recupero la lista dei layer WMS dal database..." )
			
			whereclauses = [ "1=1" ]
			if len(retrieveList) > 0:
				whereclauses.append( u'"ORDER" IN (%s)' % u",".join( map(str, retrieveList) ) )
			if len(excludeList) > 0:
				whereclauses.append( u'"ORDER" NOT IN (%s)' % u",".join( map(str, excludeList) ) )
			
			query = AutomagicallyUpdater.Query( u'SELECT * FROM ZZ_WMS WHERE %s ORDER BY "ORDER" ASC' % " AND ".join(whereclauses) )
			query = query.getQuery()
			if not query.exec_():
				AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text(), ManagerWindow.instance )
				return

			while query.next():
				layer = {}
				layer['order'] = int( query.value(0) )
				layer['title'] = Porting.str( query.value(1) )
				layer['url'] = Porting.str( query.value(2) )
				
				layer['layers'] = query.value(3).split(",")
				layer['styles'] = [ '' ] * len( layer['layers'] )
				layer['crs'] = Porting.str( query.value(4) )
				layer['format'] = "image/%s" % query.value(5).lower()
				layer['transparent'] = Porting.str( query.value(6) )
				layer['version'] = Porting.str( query.value(7) )
				
				layer['cache_scale'] = int( query.value(8) )
				layer['cache_extent'] = int( query.value(9) )
				
				layersinfo.append(layer)
			
		return layersinfo


class BuildPyramidsThread(QThread):
	def __init__(self, layer, parent=None):
		QThread.__init__(self, parent)
		self.layer = layer

	def run(self):
		# set to build all available raster pyramids
		provider = self.layer.dataProvider()
		if QGis.QGIS_VERSION[0:3] <= "1.8":	# handle API changes
			provider.buildPyramidList = self.layer.buildPyramidList
			provider.buildPyramids = self.layer.buildPyramids

		pyramids = provider.buildPyramidList()
		for i in range( len(pyramids) ):
			# mark to be pyramided
			pyramids[i].build = True

		method = QCoreApplication.translate("QgsGdalProvider", "Average",  None, QApplication.UnicodeUTF8)
		provider.buildPyramids( pyramids, method, True )

