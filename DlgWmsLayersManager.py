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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
			ret = self.onlineMode() if ManagerWindow.instance.offlineMode else self.offlineMode()
			self.onProgress(-1)
		finally:
			self.finished = True
		self.done(ret)

	def offlineMode(self):
		if ManagerWindow.instance.offlineMode:
			return False

		def saveWorldFile(imgpath, pxdim, extent):
			# save worldfile
			out = open( u"%s.wld" % imgpath[:-4], 'w')
			out.write( u"%.16f\n%.16f\n%.16f\n%.16f\n%.16f\n%.16f" % (pxdim, 0.0, 0.0, -pxdim, extent.xMinimum(), extent.yMaximum()) )
			out.close()

		def buildAllPyramids(layer):
			# create raster pyramids
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
		prevRasterIcons = settings.value("/qgis/createRasterLegendIcons", True)
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

		cached_images = {}
		try:
			# get the list of wms layers to switch
			wms_layers = []
			legend = self.iface.legendInterface()
			for layer in reversed(legend.layers()):
				p = layer.dataProvider()
				if p.name() != "wms":
					continue

				prop = layer.customProperty( "loadedByOmeroRTPlugin" )
				if not prop.isValid() and legend.isLayerVisible(layer):
					# a wms layer not loaded by omero, don't cache if it's hidden
					prop = QVariant( u"WMS_OFFLINE %s" % layer.source() )
					wms_layers.append( (layer, default_scale, default_extent, prop) )

				elif prop.toString().startsWith( "RLID_WMS" ) and not prop.toString().startsWith( "RLID_WMS_OFFLINE" ):
					# a wms layer loaded by omero
					# get scale and extent from database
					order = int(prop.toString()[9:])
					res = AutomagicallyUpdater.Query( u'SELECT CACHE_SCALA, CACHE_ESTENSIONE FROM ZZ_WMS WHERE "ORDER" = %s' % order ).getRow(0, 2)
					if res == None:
						continue
					scale, extent = res
					if scale is None or not scale.toInt()[1]:
						continue
					else:
						scale = scale.toInt()[0]
					if extent is None or not extent.toInt()[1]:
						extent = default_extent
					else:
						extent = extent.toInt()[0]

					prop = QVariant( u"RLID_WMS_OFFLINE %s" % order )
					wms_layers.append( (layer, scale, extent, prop) )


			# convert each wms in an offline layer
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
				self.setWindowTitle( self.tr( "[%1/%2] Download in corso..." ).arg(idx_layer+1).arg(len(wms_layers)) )
				self.setRange( 0, n*n+1 )

				# bottom-left point
				bl = QgsPoint(center.x()-reqdim*n/2.0, center.y()-reqdim*n/2.0)

				name = layer.name()
				visible = legend.isLayerVisible(layer)
				layerid = layer.id()
				source = layer.source()
				p = layer.dataProvider()

				# use a vrt catalog to store the cached layer instead
				# of write all the tiles on a single image
				escaped_name = name.replace( QRegExp("[^a-zA-Z0-9]"), "_" ).toLower()[:100]
				use_catalog = True
				if not use_catalog:
					out_path = QDir(cache_path).absoluteFilePath( u"%s.png" % escaped_name )
					out_image = QImage( reqpxdim*n, reqpxdim*n, QImage.Format_ARGB32 )
				else:
					out_path = QDir(cache_path).absoluteFilePath( u"%s.vrt" % escaped_name )

				# get all tiles
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

				saved = False
				if not use_catalog:
					saved = out_image.save( out_path, "PNG" )
				else:
					# create the catalog from tiles
					cmd = ["gdalbuildvrt", "-overwrite", unicode(out_path)]
					cmd.extend( in_images )
					import subprocess
					saved = (0 == subprocess.call( cmd ))
				self.onProgress()

				if saved:
					# remove the online layer and add the offline one
					QgsMapLayerRegistry.instance().removeMapLayer(layerid)
					layer = self.iface.addRasterLayer( out_path, "CACHED - %s" % name )
					if layer and layer.isValid():
						# set the layer custom property
						layer.setCustomProperty( "loadedByOmeroRTPlugin", QVariant(prop) )
						if prop.toString().startsWith( "WMS_OFFLINE" ):
							cached_images[out_path] = source

						elif prop.toString().startsWith( "RLID_WMS_OFFLINE" ):
							order = int( prop.toString().split(" ")[1] )
							ManagerWindow.RLID_WMS[order] = ManagerWindow._getLayerId(layer)

						# show/hide the layer 
						legend.setLayerVisible(layer, visible)

						# set to build all available raste
						# set title and progressbar range 
						# then build all available raster pyramids
						self.setWindowTitle( self.tr( "[%1/%2] Costruzione piramidi..." ).arg(idx_layer+1).arg(len(wms_layers)) )
						self.setRange( 0, 0 )	#self.setRange( 0, len(pyramids) )
						buildAllPyramids(layer)

						# set the transparent band
						p = layer.dataProvider()
						if True:
							layer.setTransparentBandName( "Band 4" )
						else:
							for i in range(layer.bandCount()):
								# there're no python bindings for both 
								# QgsRasterDataProvider::colorInterpretation() and
								# QgsRasterDataProvider::generateBandName() 
								if p.colorInterpretation(i) == QgsRasterDataProvider.AlphaBand:
									layer.setTransparentBandName( p.generateBandName(i) )
									break

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

	def onlineMode(self):
		if not ManagerWindow.instance.offlineMode:
			return False

		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

		prevRenderFlag = self.canvas.renderFlag()
		self.canvas.setRenderFlag( False )

		try:
			cached_images = AutomagicallyUpdater.getCachedExternalWms()

			legend = self.iface.legendInterface()
			for layer in reversed(legend.layers()):
				p = layer.dataProvider()
				if p.name() != "gdal":
					continue

				name = layer.name()
				visible = legend.isLayerVisible(layer)
				layerid = layer.id()

				prop = layer.customProperty( "loadedByOmeroRTPlugin" )
				if not prop.isValid():
					# a wms layer not loaded by omero
					continue

				elif prop.toString().startsWith( "RLID_WMS_OFFLINE" ):
					# a wms layer loaded by omero, remove it
					QgsMapLayerRegistry.instance().removeMapLayer( layerid )
					continue

				elif prop.toString().startsWith( "WMS_OFFLINE" ):
					# an external cached wms
					if not cached_images.has_key( layer.source() ):
						continue

				else:
					continue

				# remove the offline layer and add the online one
				QgsMapLayerRegistry.instance().removeMapLayer(layerid)

			ManagerWindow.instance.offlineMode = False

		finally:
			self.canvas.setRenderFlag( prevRenderFlag )
			QApplication.restoreOverrideCursor()

		return True

	@classmethod
	def loadWmsLayers(self, firstStart):
		def isHostAccessible(host):
			from PyQt4.QtNetwork import QHostInfo
			info = QHostInfo.fromName( host )
			if info.error() == QHostInfo.NoError:
				return True
			return False

		# check if offline mode changed
		if not firstStart and ManagerWindow.instance.offlineMode != AutomagicallyUpdater.offlineMode():

			# show progress bar
			if not DlgWmsLayersManager( ManagerWindow.instance.iface ).exec_():	# no switch occurs
				return True

			# now AutomagicallyUpdater.offlineMode() == self.offlineMode
			if AutomagicallyUpdater.offlineMode():	# switched from online to offline mode
				return True

		else:
			ManagerWindow.instance.offlineMode = AutomagicallyUpdater.offlineMode()


		# lista dei layer wms già caricati
		loaded_wms = QStringList()
		for order, rlid in ManagerWindow.RLID_WMS.iteritems():
			if QgsMapLayerRegistry.instance().mapLayer( rlid ) != None:
				loaded_wms << "'%s'" % order

		# recupera le informazioni sui layer wms da caricare
		query = AutomagicallyUpdater.Query( 'SELECT * FROM ZZ_WMS WHERE "ORDER" NOT IN (%s) ORDER BY "ORDER" ASC' % loaded_wms.join(",") )
		query = query.getQuery()
		if not query.exec_():
			AutomagicallyUpdater._onQueryError( query.lastQuery(), query.lastError().text(), ManagerWindow.instance )
			return False

		while query.next():
			order = query.value(0).toInt()[0]
			title = query.value(1).toString()
			url = query.value(2).toString()
			layers = query.value(3).toString()
			crs = query.value(4).toString()
			format = query.value(5).toString()
			transparent = query.value(6).toString()
			version = query.value(7).toString()

			styles = u",".join( [ 'pseudo' ] * len(layers) )
			format = "image/%s" % format.toLower()

			if not ManagerWindow.instance.offlineMode:
				# online mode, load layers from the wms server
				if QGis.QGIS_VERSION[0:3] <= "1.8":	# API changes from QGis 1.9
					rl = QgsRasterLayer(0, url, title, 'wms', layers.split(","), styles.split(","), format, crs)
				else:
					uri = QgsDataSourceURI()
					uri.setParam("url", url)
					uri.setParamList("layers", layers)
					uri.setParamList("styles", styles)
					uri.setParam("format", format)
					uri.setParam("crs", crs)
					
					rl = QgsRasterLayer(QString(uri.encodedUri()), title, 'wms')

				prop = "RLID_WMS %s" % order
			else:
				# offline mode, load layers from local cache
				escaped_title = title.replace( QRegExp("[^a-zA-Z0-9]"), "_" ).toLower()[:100]
				vrt_path = QDir( AutomagicallyUpdater.getPathToCache() ).absoluteFilePath( u'%s.vrt' % escaped_title )
				if not QFileInfo( vrt_path ).exists():
					continue
				rl = QgsRasterLayer( vrt_path, u"CACHED - %s" % title )
				rl.setTransparentBandName( "Band 4" )
				prop = "RLID_WMS_OFFLINE %s" % order

			if not rl.isValid():
				continue

			ManagerWindow.RLID_WMS[order] = ManagerWindow._getLayerId(rl)
			QgsMapLayerRegistry.instance().addMapLayer(rl)
			ManagerWindow.instance.iface.legendInterface().setLayerVisible( rl, False )
			# set custom property
			rl.setCustomProperty( "loadedByOmeroRTPlugin", QVariant(prop) )

		return True


class BuildPyramidsThread(QThread):
	def __init__(self, layer, parent=None):
		QThread.__init__(self, parent)
		self.layer = layer

	def run(self):
		# set to build all available raster pyramids
		if QGis.QGIS_VERSION[0:3] <= "1.8":	# API changes from QGis 1.9
			self.layer.dataProvider().buildPyramidList = self.layer.buildPyramidList
			self.layer.dataProvider().buildPyramids = self.layer.buildPyramids

		pyramids = self.layer.dataProvider().buildPyramidList()
		for i in range( len(pyramids) ):
			# mark to be pyramided
			pyramids[i].build = True

		method = QCoreApplication.translate("QgsGdalProvider", "Average",  None, QApplication.UnicodeUTF8)
		self.layer.dataProvider().buildPyramids( pyramids, method, True )

