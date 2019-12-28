from bs4 import BeautifulSoup
import pandas as pd
import requests


def CompileTabularData(url, statID, latitude, longitude):
    try:
        #if the website is available, get and export the data table to a list
        if requests.get(url).status_code != 404:
            res = requests.get(url)
            soup = BeautifulSoup(res.content,'lxml')
            table = soup.find_all('table')[3]
            df = pd.read_html(str(table), header=[2])[0] #obtains correct data frame in lieu of mutliple headers
            dfIndex = df.iloc[:-3] #removes the bottom headers on the page
            
            #adds the lat/lon and stationID to each entry for easier formatting
            outputList = []
            tableList = dfIndex.values.tolist()
            for line in tableList:
                addList = []
                
                addList.append(statID)
                addList.append(latitude)
                addList.append(longitude)
                outputList.append(addList)
                
                #converts each entry into a string or nulls into -1
                for item in line:
                    if item != item:
                        item = '-1'
                        addList.append(item)
                    else:
                        addList.append(str(item)) #arcpy insert cursor automatically corrects the data types in a later step

            return(outputList)
    except:
        pass
        
