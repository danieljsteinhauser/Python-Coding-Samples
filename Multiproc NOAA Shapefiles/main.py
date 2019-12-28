#Internal Libraries
from bs4 import BeautifulSoup
import pandas as pd
import requests, arcpy, multiprocessing, os
from shutil import make_archive
from time import time

#Supplied Modules
from workerTab import CompileTabularData
from workerFeat import FeatureCreation
from workerInsert import InsertWeatherData


#Allows for Overwriting Shapefiles
arcpy.env.overwriteOutput = True

#Hardcoded url with the full weather station xml data
url = 'https://w1.weather.gov/xml/current_obs/index.xml'

#Empty Lists to be used in WebScraping
stationList = [] #will contain basic info for compiling fullStationList
fullStationList = [] #will contain all tabular data for each station

#File Paths
workspace = r'C:\Users\14102\Documents\Python3Scripts\Steinhauser_Final\Shapefiles'

#Gets Python install path for use with Multiprocessing steps
def get_install_path():
    ''' Return 64bit python install path from registry (if installed and registered),
        otherwise fall back to current 32bit process install path.
    '''
    if sys.maxsize > 2**32: return sys.exec_prefix #We're running in a 64bit process
  
    #We're 32 bit so see if there's a 64bit install
    path = r'SOFTWARE\Python\PythonCore\2.7'
  
    from _winreg import OpenKey, QueryValue
    from _winreg import HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_64KEY
  
    try:
        with OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_READ | KEY_WOW64_64KEY) as key:
            return QueryValue(key, "InstallPath").strip(os.sep) #We have a 64bit install, so return that.
    except: return sys.exec_prefix #No 64bit, so return 32bit path 
    
#compiles a stationList with [url, latitude, longitude, station_id] from .xml page
def CompileStationList(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml-xml")
    
    htmlURL = soup.find_all('html_url')
    latitude = soup.find_all('latitude')
    longitude = soup.find_all('longitude')
    stationID = soup.find_all('station_id')

    for i in range(0, len(stationID)):

        dataList = []
        
        htmlText = htmlURL[i].get_text()
        dataList.append(htmlText)
        
        statID = stationID[i].get_text()
        dataList.append(statID)

        latitudeText = latitude[i].get_text()
        dataList.append(latitudeText)

        longitudeText = longitude[i].get_text()
        dataList.append(longitudeText)

        stationList.append(dataList)
            
#Uses the stationList URL to test if the weather data is available. If so, appends it to a fullStationList
def mp_TableGet(stationList):
    
    # Create and run multiprocessing pool.
    multiprocessing.set_executable(os.path.join(get_install_path(), 'pythonw.exe'))
    cpuNum = multiprocessing.cpu_count()  # determine number of cores to use
    
  
    with multiprocessing.Pool(processes=cpuNum) as tPool: # Create the pool object 
        res = tPool.starmap(CompileTabularData, stationList)  # run jobs in job list; res is a list with return values of the worker function
        fullStationList.append(res) #appends return values to fullStationList
        multiprocessing.Barrier(cpuNum) #Prevents looping through fullStationList in next step until fully compiled

#Creates shapefiles using the stationId as a unique name    
def mp_FeatureCreate(fullStationList): 
    jobs = []
    
    # Create and run multiprocessing pool.
    multiprocessing.set_executable(os.path.join(get_install_path(), 'pythonw.exe')) 
    cpuNum = multiprocessing.cpu_count()  # determine number of cores to use
    
    for station in fullStationList:
        for data in station:
            if data != None:
                #catches formating anomalies 
                try:
                    stList = []
                    statID = data[0][0]
                    stList.append(statID)
                    jobs.append(stList)
                except(ValueError,IndexError):
                    pass
    print('There are ' + str(len(jobs)) + ' shapefiles to create. Creating shapefiles...\n')
    multiprocessing.Barrier(cpuNum) #holds off on multiprocessing until all cores are available 
    
    with multiprocessing.Pool(processes=cpuNum) as fPool: # Create the pool object 
        res = fPool.starmap(FeatureCreation, jobs)  # run jobs in job list; res is a list with return values of the worker function  
    fPool.close()
    fPool.join()
    
#Inserts the tabular data from the fullStationList into the Shapefiles
def mp_DataInsert(fullStationList):
    jobs = []
    
    # Create and run multiprocessing pool.
    multiprocessing.set_executable(os.path.join(get_install_path(), 'pythonw.exe')) 
    cpuNum = multiprocessing.cpu_count()  # determine number of cores to use
    
    #Compiles a list of lists each containing valid station data
    for station in fullStationList:
        for data in station:
            if data != None:
                jobs.append([data])
   
    multiprocessing.Barrier(cpuNum) #holds off on multiprocessing until all cores are available
    with multiprocessing.Pool(processes=cpuNum) as uPool: # Create the pool object 
        res = uPool.starmap(InsertWeatherData, jobs)  # run jobs in job list; res is a list with return values of the worker function  
    uPool.close()
    uPool.join()  
 
##Main Code Block##
if __name__ == '__main__':
    startTime = time()
    
    print('\nCompiling the station list...\n')
    CompileStationList(url)
    
    print('Grabbing the available tabular data for each station...\n')
    mp_TableGet(stationList)
    
    print('Compiling list of shapefiles to create...\n')
    mp_FeatureCreate(fullStationList)
    
    print('Inserting the tabular data...\n')
    mp_DataInsert(fullStationList)
    
    print('Creating .zip file...\n')
    make_archive(workspace, 'zip', 'Shapefiles_djsFinal')
    
    print('The script has completed. It took approximately...')
    print ("--- %s seconds ---" % (time() - startTime))
