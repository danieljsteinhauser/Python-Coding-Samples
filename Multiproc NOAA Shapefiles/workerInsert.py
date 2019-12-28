import os
import arcpy

#Accepts a full list of station tabular data to cycle through and insert the correct index location's data
def InsertWeatherData(station):

    workspace = r'C:\Users\14102\Documents\Python3Scripts\Steinhauser_Final\Shapefiles' 
    for dataEntry in station:

        statID = (dataEntry[0])
        lat = (dataEntry[1])
        lon = (dataEntry[2])
        date = (dataEntry[3])
        time = (dataEntry[4])
        wind = (dataEntry[5])
        visib = (dataEntry[6])
        weather = (dataEntry[7])
        airTemp = (dataEntry[9])
        dewPoint = (dataEntry[10])
        relativeHumid = (dataEntry[13])
        windChill = (dataEntry[14])
        airPresure = (dataEntry[16])
        precip1h = (dataEntry[18])
        precip3h = (dataEntry[19])
        precip6h = (dataEntry[20])
        addList = [lon, lat, date, time, wind, visib, weather, airTemp, dewPoint, relativeHumid, airPresure, precip1h, precip3h, precip6h]
        
        fcLocation = os.path.join(workspace, statID + '.shp')
        with arcpy.da.InsertCursor(fcLocation,["SHAPE@X", "SHAPE@Y", "Date", "Time", "Wind", "Visibility", "Weather", "Air_Temp", "Dew_Point", 
                                               "Rel_Humid", "Air_Pres", "Precip_1hr", "Precip_3hr", "Precip_6hr",],) as cursor:
            cursor.insertRow(addList)
        addList = []
        del cursor
