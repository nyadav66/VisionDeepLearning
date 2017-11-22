
import pandas as pd
from RoofPatch import *

outFolder = "/home/nyadav/patches/"

DGMapFolder = '/home/jtaneja/data/DG/ftp2.digitalglobe.com'


def getPatch(xlsFileName):
    df = pd.read_csv(xlsFileName, delimiter=",").fillna("-NA-")
    for df_index, df_row in df.iterrows():
        lat = float(df_row["latitude"])
        lon = float(df_row["longitude"])
        tileFile = "/home/jtaneja/data/DG/ftp2.digitalglobe.com/"+str(df_row["filename"])
        bbox = str(df_row["bbox"]).split("#")
        bbox = [float(num) for num in bbox]
        print lat,lon
       
        imageWidth = 100
        imageHeight = 100
        zoom = 18.26
        pixel_size = 19584
        tile_size = 512
        if lat != '-NA-' and lon != '-NA-' and bbox != '-NA-' and tileFile != '-NA-':
            rpatch = RoofPatch(lat,lon,bbox,tileFile)
            patch = rpatch.getPatchPixelCoords(imageWidth,imageHeight)
            patchName = str(df_index) + '_' + str(lat) + '_' + str(lon) + '_' +str(tileFile).split('/')[-1] +'.jpg'
            plt.imsave(outFolder + patchName, 255-patch.astype('uint8'))


getPatch('/home/nyadav/src/obsTiff.csv')
