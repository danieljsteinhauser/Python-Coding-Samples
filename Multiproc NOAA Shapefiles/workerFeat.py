import arcpy

#Parameters for each created station shapefile formated as 'station.shp'
def FeatureCreation(station):
    #File Paths
    arcpy.env.overwriteOutput = True
    workspace = r'C:\Users\14102\Documents\Python3Scripts\Steinhauser_Final\Shapefiles'
    spatialRef = 4326 # This numerical value represents WGS1984
    arcpy.CreateFeatureclass_management(workspace, station, "Point", "", "", "", spatialRef)
    fcLocation = workspace + "//" + station + ".shp"
    
    #Add Fields
    arcpy.AddField_management(fcLocation, "Date", "SHORT")
    arcpy.AddField_management(fcLocation, "Time", "TEXT")
    arcpy.AddField_management(fcLocation, "Wind", "TEXT")
    arcpy.AddField_management(fcLocation, "Visibility", "FLOAT")
    arcpy.AddField_management(fcLocation, "Weather", "TEXT")
    arcpy.AddField_management(fcLocation, "Air_Temp", "SHORT")
    arcpy.AddField_management(fcLocation, "Dew_Point", "SHORT")
    arcpy.AddField_management(fcLocation, "Rel_Humid", "TEXT")
    arcpy.AddField_management(fcLocation, "Air_Pres", "FLOAT")
    arcpy.AddField_management(fcLocation, "Precip_1hr", "FLOAT")
    arcpy.AddField_management(fcLocation, "Precip_3hr", "FLOAT")
    arcpy.AddField_management(fcLocation, "Precip_6hr", "FLOAT")
