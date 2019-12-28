import qgis
import qgis.core

import os

qgis_prefix = os.getenv("QGIS_PREFIX_PATH")
qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()

# abstract class Waterbody is the root class of our hierarchy 
class Waterbody():
    
    # constructor (can be derived by subclasses)
    def __init__(self, name, geometry):
        self.name = name            # instance variable for storing the name of the watebrbody
        self.geometry = geometry    # instance variable for storing the a QgsGeometry object with the geometry for this waterbody

    # abstract static class function for creating a waterbody object if the given way satisfies
    # the required conditions; needs to be overridden by instantiable subclasses 
    def fromOSMWay(way, allNodes):     
        pass
    
    # abstract method for creating QgsFeature object for this waterbody;
    # needs to be overridden by instantiable subclasses 
    def toQgsFeature(self):
        pass
    

# abstract class LinearWaterBody is derived from class Waterbody
class LinearWaterbody(Waterbody):
    
    # constructor (can be invoked by derived classes and takes care of the length computation)
    def __init__(self, name, geometry):
        super(LinearWaterbody, self).__init__(name, geometry)
            
        #calculate length of this linear waterbody
        qda = qgis.core.QgsDistanceArea() 
        qda.setEllipsoid('WGS84')
        length = qda.measureLength(geometry)

        #instance variable for storing the length of this linear waterbody
        self.length = qda.convertLengthMeasurement(length, qgis.core.QgsUnitTypes.DistanceMeters) 

    def toQgsFeature(self):
        pass
    # ... you may want to add additional auxiliary methods or class functions to this class definition
    
#    def isFeatureLine(way, allNodes):
#        if way['nodes'][0] != way[nodes][-1]:
#            
#        else:
#            pass

# abstract class ArealWaterbody is derived from class Waterbody
class ArealWaterbody(Waterbody):

    # constructor (can be invoked by derived classes and takes care of the area computation)
    def __init__(self, name, geometry):
        super(ArealWaterbody, self).__init__(name, geometry)

         #calculate area of this areal waterbody
        qda = qgis.core.QgsDistanceArea() 
        qda.setEllipsoid('WGS84')
        area = qda.measureArea(geometry)

        # instance variable for storing the length of this areal waterbody
        self.area = qda.convertAreaMeasurement(area, qgis.core.QgsUnitTypes.AreaSquareMeters)
#    
    def toQgsFeature(self):
        pass

    # ... you may want to add additional auxiliary methods or class functions to this class definition
#    def isFeaturePoly(geometry):
#        if way['nodes'][0] == way[nodes][-1]:
#            
#        else:
#            pass

# class Stream is derived from class LinearWaterBody and can be instantiated
class Stream(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Stream,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        try:
            #Boolean statement to test if the feature is actually a stream
            if way['tags']['waterway'] != 'stream':
                return(None) 
            
            #If the way is a stream, proceed with class objection creation
            else:
                
                #If the way does not have a name, assign it the name 'unknown'
                if  way['tags'].get('name'):
                   streamName = way['tags']['name']
                else:
                    streamName = 'unknown'
                    
                #list of nodes which compose the provided way
                nodeList = way['nodes']
                
                #Empty List to add the Qgs Geography Points.
                qgsPoints = []
                
                #References the node dictionary for the lat/long of each node in the way
                #Then creates a QGS Point object to place in the qgsPoints list
                for node in nodeList:
                    lat = allNodes[node]['lat']
                    lon = allNodes[node]['lon']
                    qgsPoint = qgis.core.QgsPointXY(lon, lat)
                    qgsPoints.append(qgsPoint)
                    
                #uses the qgsPoints list to create a singular line geography object
                qgsLine = qgis.core.QgsGeometry.fromPolylineXY(qgsPoints)      
                output = Stream(streamName, qgsLine)
                return(output)
                
        except:
            pass
        
    #function to return Qgs Feature objects for linear feature creation             
    def toQgsFeature(self):
        feat = qgis.core.QgsFeature()
        feat.setGeometry(self.geometry)
        feat.setAttributes([self.name, "Stream", self.length])
        return(feat)
        
    #returns information about the given object via print(obj)
    def __str__(self):
        return 'Feature Name: {0}, Feature Type: {1}, Feature Length: {2}m'.format(self.name, "Stream", self.length)
    
# class River is derived from class LinearWaterBody and can be instantiated
class River(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(River,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        try:
            #Boolean statement to test if the feature is actually a river
            if way['tags']['waterway'] != 'river':
                return None 
            
            #If the way is a stream, proceed with class objection creation
            else:
                
                #If the way does not have a name, assign it the name 'unknown'
                if  way['tags'].get('name'):
                   riverName = way['tags']['name']
                else:
                    riverName = 'unknown'
                    
                #list of nodes which compose the provided way
                nodeList = way['nodes']
                
                #Empty List to add the Qgs Geography Points.
                qgsPoints = []
                
                #References the node dictionary for the lat/long of each node in the way
                #Then creates a QGS Point object to place in the qgsPoints list
                for node in nodeList:
                    lat = allNodes[node]['lat']
                    lon = allNodes[node]['lon']
                    qgsPoint = qgis.core.QgsPointXY(lon, lat)
                    qgsPoints.append(qgsPoint)
                    
                #uses the qgsPoints list to create a singular line geography object
                qgsLine = qgis.core.QgsGeometry.fromPolylineXY(qgsPoints)
                output = River(riverName, qgsLine)
                return(output)
                
        except:
            pass
        
    #function to return Qgs Feature objects for linear feature creation             
    def toQgsFeature(self):
        feat = qgis.core.QgsFeature()
        feat.setGeometry(self.geometry)
        feat.setAttributes([self.name, "River", self.length])
        return(feat)
    
    #returns information about the given object via print(obj)    
    def __str__(self):
        return 'Feature Name: {0}, Feature Type: {1}, Feature Length: {2}m'.format(self.name, "River", self.length)

# class Canal is derived from class LinearWaterBody and can be instantiated
class Canal(LinearWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Canal,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        try:
            #Boolean statement to test if the feature is actually a river
            if way['tags']['waterway'] != 'canal':
                return None 
            
            #If the way is a stream, proceed with class objection creation
            else:
                #If the way does not have a name, assign it the name 'unknown'
                if  way['tags'].get('name'):
                   canalName = way['tags']['name']
                else:
                    canalName = 'unknown'   
                #list of nodes which compose the provided way
                nodeList = way['nodes']
                
                #Empty List to add the Qgs Geography Points.
                qgsPoints = []
                #References the node dictionary for the lat/long of each node in the way
                #Then creates a QGS Point object to place in the qgsPoints list
                for node in nodeList:
                    lat = allNodes[node]['lat']
                    lon = allNodes[node]['lon']
                    qgsPoint = qgis.core.QgsPointXY(lon, lat)
                    qgsPoints.append(qgsPoint)
                    
                #uses the qgsPoints list to create a singular line geography object
                qgsLine = qgis.core.QgsGeometry.fromPolylineXY(qgsPoints)
                output = Canal(canalName, qgsLine)
                return(output)
                
        except:
            pass
        
    #function to return Qgs Feature objects for linear feature creation             
    def toQgsFeature(self):
        feat = qgis.core.QgsFeature()
        feat.setGeometry(self.geometry)
        feat.setAttributes([self.name, "Canal", self.length])
        return(feat)
        
    #returns information about the given object via print(obj)    
    def __str__(self):
        return 'Feature Name: {0}, Feature Type: {1}, Feature Length: {2}m'.format(self.name, "Canal", self.length)

# class Lake is derived from class ArealWaterbody and can be instantiated
class Lake(ArealWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Lake,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        try:
            #Boolean statement to test if the feature is actually a river
            if way['tags']['natural'] != 'water' or way['tags']['water'] != 'lake':
                return None 
            
            #If the way is a stream, proceed with class objection creation
            else:
                #If the way does not have a name, assign it the name 'unknown'
                if  way['tags'].get('name'):
                   lakeName = way['tags']['name']
                else:
                    lakeName = 'unknown'   
                #list of nodes which compose the provided way
                nodeList = way['nodes']
                
                #Empty List to add the Qgs Geography Points.
                qgsPoints = []
                
                #Empty List which the populated qgsPoints list will be appended 
                polygonList = []
                #References the node dictionary for the lat/long of each node in the way
                #Then creates a QGS Point object to place in the qgsPoints list
                for node in nodeList:
                    lat = allNodes[node]['lat']
                    lon = allNodes[node]['lon']
                    qgsPoint = qgis.core.QgsPointXY(lon, lat)
                    qgsPoints.append(qgsPoint)
                    
                #uses the qgsPoints list to create a singular Qgs polygon geography object
                polygonList.append(qgsPoints)
                qgsPoly = qgis.core.QgsGeometry.fromPolygonXY(polygonList)
                output = Lake(lakeName, qgsPoly)
                return(output)
                
        except:
            pass
        
    #function to return Qgs Feature objects for polygon feature creation             
    def toQgsFeature(self):
        feat = qgis.core.QgsFeature()
        feat.setGeometry(self.geometry)
        feat.setAttributes([self.name, "Lake", self.area])
        return(feat)
    
    #returns information about the given object via print(obj)
    def __str__(self):
        return 'Feature Name: {0}, Feature Type: {1}, Feature Area: {2} sq_m'.format(self.name, "Lake", self.area)
    
# class Pond is derived from class ArealWaterbody and can be instantiated
class Pond(ArealWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Pond,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        try:
            #Boolean statement to test if the feature is actually a river
            if way['tags']['natural'] != 'water' or way['tags']['water'] != 'pond':
                return None 
            
            #If the way is a stream, proceed with class objection creation
            else:
                #If the way does not have a name, assign it the name 'unknown'
                if  way['tags'].get('name'):
                   pondName = way['tags']['name']
                else:
                    pondName = 'unknown'   
                #list of nodes which compose the provided way
                nodeList = way['nodes']
                
                #Empty List to add the Qgs Geography Points.
                qgsPoints = []
                
                #Empty List which the populated qgsPoints list will be appended 
                polygonList = []
                #References the node dictionary for the lat/long of each node in the way
                #Then creates a QGS Point object to place in the qgsPoints list
                for node in nodeList:
                    lat = allNodes[node]['lat']
                    lon = allNodes[node]['lon']
                    qgsPoint = qgis.core.QgsPointXY(lon, lat)
                    qgsPoints.append(qgsPoint)
                    
                #uses the qgsPoints list to create a singular Qgs polygon geography object
                polygonList.append(qgsPoints)
                qgsPoly = qgis.core.QgsGeometry.fromPolygonXY(polygonList)
                output = Pond(pondName, qgsPoly)
                return(output)
                
        except:
            pass
        
    #function to return Qgs Feature objects for polygon feature creation             
    def toQgsFeature(self):
        feat = qgis.core.QgsFeature()
        feat.setGeometry(self.geometry)
        feat.setAttributes([self.name, "Pond", self.area])
        return(feat)
    
    #returns information about the given object via print(obj)
    def __str__(self):
        return 'Feature Name: {0}, Feature Type: {1}, Feature Area: {2} sq_m'.format(self.name, "Pond", self.area)

# class Reservior is derived from class ArealWaterbody and can be instantiated
class Reservoir(ArealWaterbody):
    
    # constructor (calls LinearWaterbody constructor to initialize name, geometry, and length instance variables)
    def __init__(self, name, geometry):
        super(Reservoir,self).__init__(name, geometry)

    # override the fromOSMWay(...) static class function
    def fromOSMWay(way, allNodes):
        try:
            #Boolean statement to test if the feature is actually a river
            if way['tags']['natural'] != 'water' or way['tags']['water'] != 'reservoir':
                return None 
            
            #If the way is a stream, proceed with class objection creation
            else:
                #If the way does not have a name, assign it the name 'unknown'
                if  way['tags'].get('name'):
                   reservoirName = way['tags']['name']
                else:
                    reservoirName = 'unknown'   
                #list of nodes which compose the provided way
                nodeList = way['nodes']
                
                #Empty List to add the Qgs Geography Points.
                qgsPoints = []
                
                #Empty List which the populated qgsPoints list will be appended 
                polygonList = []
                
                #References the node dictionary for the lat/long of each node in the way
                #Then creates a QGS Point object to place in the qgsPoints list
                for node in nodeList:
                    lat = allNodes[node]['lat']
                    lon = allNodes[node]['lon']
                    qgsPoint = qgis.core.QgsPointXY(lon, lat)
                    qgsPoints.append(qgsPoint)
                    
                #uses the qgsPoints list to create a singular Qgs polygon geography object
                polygonList.append(qgsPoints)
                qgsPoly = qgis.core.QgsGeometry.fromPolygonXY(polygonList)
                output = Reservoir(reservoirName, qgsPoly)
                return(output)
                
        except:
            pass
        
    #function to return Qgs Feature objects for polygon feature creation             
    def toQgsFeature(self):
        feat = qgis.core.QgsFeature()
        feat.setGeometry(self.geometry)                 
        feat.setAttributes([self.name, "Reservoir", self.area])
        return(feat)
    
    #returns information about the given object via print(obj)
    def __str__(self):
        return 'Feature Name: {0}, Feature Type: {1}, Feature Area: {2} sq_m'.format(self.name, "Reservoir", self.area)