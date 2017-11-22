import pandas as pd

class extractFileInfo:

    def __init__(self,shapeRecords,xlsFileName):
        #self.latLonList = self.genLatLonList(xlsFileName)
        self.shapeRecords = shapeRecords

    def genLatLonList(self,xlsFileName):
        df = pd.read_csv(xlsFileName, delimiter=",").fillna("-NA-")
        latLonList = df.filter(["latitude",'longitude'], axis=1)
        return latLonList

    def returnHitInfo(self, latLon):
        for index,shapeRecList in enumerate(self.shapeRecords):
            for ind,shapeRec in enumerate(shapeRecList):
                shape = shapeRec.shape
                record = shapeRec.record
                bbox = shape.bbox
                tiff_file = record[0]
                #print "bbox",bbox
                #print "latlon",latLon
                if self.pointInBox(bbox, latLon):
                    return [tiff_file,'#'.join(str(e) for e in shape.bbox)]

        return ""

    def findTiffFile(self,xlsFileName,destFile):
        print "Getting correspinding tiff file for all records"
        df = pd.read_csv(xlsFileName, delimiter=",").fillna("-NA-")
        tt = pd.concat([df, pd.DataFrame(columns=['filename', 'bbox'])])
        for tt_index, tt_row in tt.iterrows():
             print "lat",tt_row["latitude"],"lon",tt_row["longitude"],"index",tt_index+1
             if(tt_row["latitude"] == "-NA-" or tt_row["longitude"] == "-NA-"):
		continue
             hitInfo = self.returnHitInfo([float(tt_row["latitude"]),float(tt_row["longitude"])])
             print "hitinfo",hitInfo
             if hitInfo != "":
                tt_row["filename"] = hitInfo[0]
                tt_row["bbox"] = hitInfo[1]
                tt.set_value(tt_index,'filename',hitInfo[0])
                tt.set_value(tt_index,'bbox',hitInfo[1])
             else:
                 tt.set_value(tt_index,'filename',"-NA-")
                 tt.set_value(tt_index,'bbox',"-NA-")



        tt.to_csv(destFile, index=False, encoding='utf-8')
        print "Finished process to get tiffed file"


    def pointInBox(self, bbox, latLon):
        return (latLon[0] <= bbox[3] and latLon[1] <= bbox[2] and latLon[0] >= bbox[1] and latLon[1] >= bbox[0])





