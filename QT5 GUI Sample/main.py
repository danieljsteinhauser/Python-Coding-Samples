import arcpy, sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox

import gui
import core_functions as f
                    
arcpy.env.overwriteOutput = True

#Empty lists used in combobox population
pointFieldList = []
countryNameList = []

#Hard-coded query fields for the countries and points shapefiles
polygonField = 'NAME'
pointField = 'shop'

# =======================================================================
# create app and main window + dialog GUI 
# =======================================================================
app = QApplication(sys.argv)
window = QWidget()

ui = gui.Ui_Form() #instantiation of my Ui_Form class
ui.setupUi(window)

#========================================================================
# GUI Event Handlers and Objects
# =======================================================================
def LocatePolygon():  
    global polygonFile
    try:
        ui.countryNameComboBox.clear()  #clears combo-box to allow for selection after error
        countryNameList = [] #clears list to allow for selection after error
        polygonFile, _ = QFileDialog.getOpenFileName(window, "Select a Shapefile","","Shapefile (*.shp)")
        filenameShorten = os.path.basename(polygonFile)
        ui.countryTextBox.setText(filenameShorten)
        f.CountryNameExtract(polygonFile, countryNameList)
        ui.countryNameComboBox.addItems(countryNameList)
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: 0001\n\nFailure encountered during polygon file selection.\n\nPlease ensure that a Country shapefile containing a field of 'NAME' is used.")
                                
def LocatePoint(): 
    ui.shopTypeComboBox.clear()
    global pointFile
    try:
        ui.shopTypeComboBox.clear()  #clears combo-box to allow for selection after error
        pointFieldList = [] #clears list to allow for selection after error
        pointFile, _ = QFileDialog.getOpenFileName(window, "Select a Shapefile","","Shapefile (*.shp)")
        filenameShorten = os.path.basename(pointFile)
        ui.pointsTextBox.setText(filenameShorten)
        f.PointFieldExtract(pointFile, pointField, pointFieldList)
        ui.shopTypeComboBox.addItems(pointFieldList)
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: 0002\n\nFailure encountered during point file selection.\n\nPlease ensure that a point shapefile containing a field of 'shop' is used.")


def DefineOutput():
    try:    
        global outputName
        outputName, _ = QFileDialog.getSaveFileName(window, "Save file Location")
        ui.outputTextBox.setText(outputName)
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: 0003\n\nFailure encountered during save location selection.\n\nPlease ensure that the selected file directory is valid and that only standard characters are used.")

def SubmitButton():
    
    try:
        polygonValue = ui.countryNameComboBox.currentText()
        
        if ui.allShopsCheckBox.isChecked() == True:
            pointValue = ''
        else:
            pointValue = ui.shopTypeComboBox.currentText()
              
        outputFile = (outputName + ".shp")
            
        f.FeatureExtract(polygonFile, pointFile, polygonField, pointField, polygonValue, pointValue, outputFile)
            
        if pointValue == '':
            QMessageBox.information(window, "Sucess!","A shapefile containing all shops within '{}' has been exported to {}".format(polygonValue, outputFile))
        else:
            QMessageBox.information(window, "Sucess!","A shapefile containing '{}' shops within '{}' has been exported to {}".format(pointValue, polygonValue, outputFile))
    
    except NameError:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: #0004\n\nFailure encountered during feature extraction.\n\nPlease ensure that all of the fields have been assigned a value.")
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: 0005\n\nFailure encountered during feature extraction.\n\nPlease ensure that none of the selected files are open in ArcMap or any other geospatial software.")
# =======================================================================
# connect signals 
# =======================================================================

#Submit Push Button 
ui.submitPushButton.clicked.connect(SubmitButton)

#ToolButtons
ui.countryTB.clicked.connect(LocatePolygon)
ui.pointsTB.clicked.connect(LocatePoint)
ui.outputTB.clicked.connect(DefineOutput)

# =======================================================================
# run app 
# =======================================================================
window.show()
sys.exit(app.exec_())