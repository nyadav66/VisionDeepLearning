from glob import glob
from os import listdir
from os.path import isfile, join
import shapefile

class processShapeFiles:

    def __init__(self,sourcePath):
        self.sourcePath = sourcePath
        self.shapeFileReaders = self.get_shapefile_reader_obj(sourcePath)

    def get_shapefile_reader_obj(self,sourcePath):

        shapeFileReader = []
        for dir in glob(self.sourcePath + "/*/"):
            for file in listdir(dir):
                filePath = join(dir, file)
                if (file.endswith(".shp")):
                    shapeFileReader.append(shapefile.Reader(filePath))
        print "total ShapefileReader",len(shapeFileReader)
        return shapeFileReader

    def get_shapeRecords(self):
        shapeRecords = [sf.shapeRecords() for sf in self.shapeFileReaders]
        return shapeRecords





