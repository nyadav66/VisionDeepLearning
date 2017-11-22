import math
from math import radians, cos, sin, asin, sqrt
import numpy as np
from matplotlib import pyplot as plt

import sys
import gdal, ogr, os, osr
from PIL import Image

class RoofPatch:

	def __init__(self,lat,lon,bbox,tileFile):
		self.lat = lat
		self.lon = lon
		self.bbox = bbox
		self.tileFile = tileFile


	def getpixelsPerM(self,tileFile,bbox):
		length = self.haversine(bbox[0], bbox[1], bbox[0], bbox[3]) * 1000
		return (tileFile.shape[1] * 1.0) / length


	def haversine(self, lon1, lat1, lon2, lat2):
		"""
		Calculate the great circle distance between two points
		on the earth (specified in decimal degrees)
		"""
		# convert decimal degrees to radians
		lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

		# haversine formula
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
		c = 2 * asin(sqrt(a))
		r = 6371  # Radius of earth in kilometers. Use 3956 for miles
		return c * r


	def pixelOffset2coord(self,rasterfn,xOffset,yOffset):
		raster = gdal.Open(rasterfn)
		geotransform = raster.GetGeoTransform()
		originX = geotransform[0]
		originY = geotransform[3]
		pixelWidth = geotransform[1]
		pixelHeight = geotransform[5]
		coordX = originX+pixelWidth*xOffset
		coordY = originY+pixelHeight*yOffset
		return coordX, coordY


	def coord2Pixel(self,raster,lat,lon,transform):
		#raster = gdal.Open(rasterfn)
		projection = raster.GetProjection()
		src = osr.SpatialReference();
		src.SetWellKnownGeogCS("WGS84");
		dst = osr.SpatialReference(projection)
		ct = osr.CoordinateTransformation(src, dst)
		xy = ct.TransformPoint(lon, lat)
		y = (int((xy[0] - transform[0]) / transform[1]))
		x = (int((xy[1] - transform[3]) / transform[5]))
		return x,y


	def getPatchCoordinates(self,xOffset, yOffset, imageWidth, imageHeight, pixelsPerM):

		#xOffset,yOffset = self.coord2Pixel(self.tileFile,center_lat,center_lon)

		roadVector = np.array([1, 0])
		perpVector = np.array([0, 1])

		pixelRadius = int(math.ceil((imageWidth / 2) * pixelsPerM))
		pixelLength = int(math.ceil(imageHeight * pixelsPerM))
		#print "pixelRadius",pixelRadius, "pixelLength",pixelLength

		orig = np.array([xOffset, yOffset]) - (perpVector * pixelRadius) - (roadVector*pixelRadius)
		patchCoords = np.zeros([pixelLength, 2 * pixelRadius,2])
		for i in range(0, pixelLength):
		    currOrig = orig + roadVector * i
		    for j in range(0, 2 * pixelRadius):
		        currPoint = currOrig + perpVector * j
                        #print "neha", currPoint.shape
		        patchCoords[i, j] = currPoint

		return patchCoords
        def GInterpolate(self,image, x, y):

            orig = np.array([x, y])
            bl = np.array([math.floor(x), math.floor(y)]).astype(int)
            br = np.array([math.ceil(x), math.floor(y)]).astype(int)
            tl = np.array([math.floor(x), math.ceil(y)]).astype(int)
            tr = np.array([math.ceil(x), math.ceil(y)]).astype(int)
            corners = [bl, br, tl, tr]
            val = np.zeros(3)
            denum = 0
            for corner in corners:
                # weight = 1.0/(1.0+np.linalg.norm(orig-corner))
                weight = (math.sqrt(2) - np.linalg.norm(orig - corner))
                val += image[corner[0], corner[1]] * weight
                denum += weight
            val = val / denum
            return np.round(val.astype(int))

	def getPatchPixelCoords(self,imageWidth,imageHeight):
		
		tileFileArray = plt.imread(self.tileFile)

		pixelsPerM = self.getpixelsPerM(tileFileArray,self.bbox)

		raster = gdal.Open(self.tileFile)
		transform = raster.GetGeoTransform()

		xOffset,yOffset = self.coord2Pixel(raster,self.lat,self.lon,transform)

		pixelRadius = int(math.ceil((imageWidth / 2) * pixelsPerM))
		pixelLength = int(math.ceil(imageHeight * pixelsPerM))


		patchCoords = self.getPatchCoordinates(xOffset,yOffset,imageWidth,imageHeight,pixelsPerM)
                
                patchValues = np.zeros([patchCoords.shape[0], patchCoords.shape[1], 3])

		for i in range(0, patchCoords.shape[0]):
		    for j in range(0, patchCoords.shape[1]):
                        #print "shape",tileFileArray[patchCoords[i].astype(int),patchCoords[j].astype(int),:].shape, patchCoords[i],patchCoords[j]
		        currPixel = patchCoords[i, j]
                        #print "currPixel",currPixel.shape
                        patchValues[i, j] = 255 - self.GInterpolate(tileFileArray, currPixel[0], currPixel[1])
                return patchValues
		#return tileFileArray[xOffset-pixelRadius:pixelRadius+xOffset,yOffset-pixelRadius:pixelRadius+yOffset,:]

