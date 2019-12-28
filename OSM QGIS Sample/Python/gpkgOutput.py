import hydro_classes
import json, os 

import qgis
import qgis.core

qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()

def returnOutput(jsonFile, outputLinear, outputAreal):
    #opens the supplied JSON file and parses way and node data
    with open(jsonFile, encoding = "utf8") as file: 
        data = json.load(file)
    nodesDict = {}  # create empty dictionary for the node elements
    waysDict = {}   # create empty dictionary for the way elements
   
    for element in data['elements']:            # go through all elements in input data
        if element['type'] == 'node':           # check if element is an OSM node
            nodesDict[element['id']] = element  # place element in nodes dictionary using its ID as the key
        elif element['type'] == 'way':          # check if element is an OSM way
            waysDict[element['id']] = element   # place element in ways dictionary using its ID as the key
                    
    
    #Empty lists which will recieve returns from the toQgsFeature function
    #The populated objects will later be used to create the GPKG files
    returnLinearList = []
    returnArealList = []
    
    #lists containing each bottom-level areal and linear classes
    aClassName = [hydro_classes.Lake, hydro_classes.Pond, hydro_classes.Reservoir]
    lClassName = [hydro_classes.Stream, hydro_classes.River, hydro_classes.Canal]
    
    #loops through each id in the waysDict and feeds a dictionary entry of waysDict[wayID]
    #into the fromOSMWay function of each linear class fromOSMWay function
    #the class objects are then fed into toQgsFeature to return a QgsFeature 
    #object which is appended to a list for future GPKG creation
    for wayID in waysDict:
        for x in lClassName:
            way = waysDict[wayID]
            returnLinear = x.fromOSMWay(way, nodesDict)
            if returnLinear:
                returnFeat = returnLinear.toQgsFeature()
                returnLinearList.append(returnFeat)
            
    #loops through each id in the waysDict and feeds a dictionary entry of waysDict[wayID]
    #into the fromOSMWay function of the class object is then fed into
    #the class objects are then fed into toQgsFeature to return a QgsFeature 
    #object which is appended to a list for future GPKG creation      
    for wayID in waysDict:
        for x in aClassName:
            way = waysDict[wayID]
            returnAreal = x.fromOSMWay(way, nodesDict)
            if returnAreal:
                returnFeat = returnAreal.toQgsFeature()
                returnArealList.append(returnFeat)
    
    #Adds the list items for each list to a QgsProvider object and creates the GPKG 
    lLayer = qgis.core.QgsVectorLayer('LineString?crs=EPSG:4326&field=NAME:string(50)&field=TYPE:string(10)&field=LENGTH:double(2)', 'Linear Features' , 'memory')
    aLayer = qgis.core.QgsVectorLayer('Polygon?crs=EPSG:4326&field=NAME:string(50)&field=TYPE:string(10)&field=AREA:double(2)', 'Areal Features' , 'memory')
    
    aProv = aLayer.dataProvider()
    lProv = lLayer.dataProvider()
    
    aProv.addFeatures(returnArealList)
    lProv.addFeatures(returnLinearList)
    
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(lLayer, outputLinear, "utf-8", lLayer.crs(), "GPKG") 
    print('GPKG file containing linear features within the JSON file was created at file location ' + outputLinear)
    
    qgis.core.QgsVectorFileWriter.writeAsVectorFormat(aLayer, outputAreal, "utf-8", aLayer.crs(), "GPKG")
    print('\nGPKG file containing linear features within the JSON file was created at file location ' + outputAreal)