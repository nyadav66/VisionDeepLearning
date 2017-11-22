
from processShapeFiles import *
from extractFileInfo import *

processShapeFiles = processShapeFiles("/home/jtaneja/data/DG/ftp2.digitalglobe.com")
print "Getting all shape records"
shapeRecords = processShapeFiles.get_shapeRecords()
print "Finished process to obtain shapeRecords"
extractFileInfo = extractFileInfo(shapeRecords,"./obs.csv") 
extractFileInfo.findTiffFile("./obs.csv","./obsTiff.csv")
