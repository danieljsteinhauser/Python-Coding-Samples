import arcpy
#===============================Arcpy Functions ==============================#
#Search Cursor which adds all country names in shapefile to empty list for combo-box
def CountryNameExtract(polygonFile, countryNameList):
    with arcpy.da.SearchCursor(polygonFile, "NAME") as cursor:
        for row in cursor:
            countryNameList.append(row[0])
    del cursor
    countryNameList.sort(key=str.casefold) #casefold code found https://stackoverflow.com/questions/13954841/sort-list-of-strings-ignoring-upper-lower-case
    
#Search Cursor which adds all shop types in shapefile to empty list for combo-box    
def PointFieldExtract(pointFile, pointField, pointFieldList):
    with arcpy.da.SearchCursor(pointFile, pointField) as cursor:
        for row in cursor:
            if row[0] == ' ':
                continue
            if not row[0] in pointFieldList:
                pointFieldList.append(row[0])
    del cursor
    pointFieldList.sort(key=str.casefold) #casefold code found https://stackoverflow.com/questions/13954841/sort-list-of-strings-ignoring-upper-lower-case

def FeatureExtract(polygonFile, pointFile, polygonField, pointField, polygonValue, pointValue, outputFile):
    polygonQuery = '"{0}" = \'{1}\''.format(polygonField, polygonValue)          # query string
    arcpy.MakeFeatureLayer_management(polygonFile,"polygonLayer", polygonQuery)  # produce layer based on query string
     
    # select target points from point file
    if pointValue:   # not None, so the query string needs to use pointValue
        pointQuery = '"{0}" = \'{1}\''.format(pointField, pointValue)
    else:            # pointValue is None, so the query string aks for entries that are not NULL and not the empty string
        pointQuery = '"{0}" IS NOT NULL AND "{0}" <> \'\''.format(pointField) 
    arcpy.MakeFeatureLayer_management(pointFile,"pointLayer", pointQuery)        # produce layer based on query string
     
    # select only points of interest in point layer that are within the target polygon    
    arcpy.SelectLayerByLocation_management("pointLayer", "WITHIN", "polygonLayer")
     
    # write selection to output file
    arcpy.CopyFeatures_management("pointLayer", outputFile)
     
    # clean up layers    
    arcpy.Delete_management("polygonLayer")
