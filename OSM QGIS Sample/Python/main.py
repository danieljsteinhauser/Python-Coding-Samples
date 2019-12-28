import sys, os, json
import qgis
import qgis.core

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox

import gui
import hydro_classes
import gpkgOutput
# =======================================================================
# QGIS Instantiation 
# =======================================================================
qgis_prefix = os.getenv("QGIS_PREFIX_PATH")      
qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True) 
qgs = qgis.core.QgsApplication([], False)
qgs.initQgis()

# =======================================================================
# QGIS Geoprocessing  
# =======================================================================
sys.path.append(r"C:\OSGeo4W64\apps\qgis\python\plugins") 
import processing 
from processing.core.Processing import Processing 
Processing.initialize() 
qgis.core.QgsApplication.processingRegistry().addProvider(qgis.analysis.QgsNativeAlgorithms())
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
def LocateJSON():  
    try:
        global jsonFile
        jsonFile, _ = QFileDialog.getOpenFileName(window, "Select a JSON file","","JSON (*.json)")
        ui.jsonTextBox.setText(jsonFile) #removes entire filename from textbox to increase readibility 
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: #0001\n\nFailure encountered during JSON file selection.\n\nPlease ensure that a valid JavaScript Object Notation (JSON) file is used.")
                                


def DefineLinearOutput():
    try:  
        global linearOutputGPKG
        linearOutputName, _ = QFileDialog.getSaveFileName(window, "Save file Location")
        linearOutputGPKG = linearOutputName + '.gpkg'
        ui.linearOutputTextbox.setText(linearOutputGPKG)
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: #0002\n\nFailure encountered during save location selection.\n\nPlease ensure that the selected file directory is valid and that only standard characters are used.")

def DefineAerialOutput():
    try:    
        global arealOutputGPKG
        arealOutputName, _ = QFileDialog.getSaveFileName(window, "Save file Location")
        arealOutputGPKG = arealOutputName + '.gpkg'
        ui.arealFeatureTextbox.setText(arealOutputGPKG)
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: #0003\n\nFailure encountered during save location selection.\n\nPlease ensure that the selected file directory is valid and that only standard characters are used.")

#Submit button sends frabicated node and way dictionaries to a function which
#takes the two output file paths and dictionaries to create the GPKGs
def SubmitButton():
    try:     
        gpkgOutput.returnOutput(jsonFile, linearOutputGPKG, arealOutputGPKG)
        QMessageBox.information(window, "All Done!", "The Creation of Your Geopackages is Complete.\n\nIf you do not see your files in the provided locations, please verify that your JSON file contains Open Street Map Data.")
    except:
        QMessageBox.information(window, "An Unexpected Error Has Occured!", "Error: #0004\n\nFailure encountered during JSON parsing.\n\nPlease ensure that all of the above fields have been assigned a value.")

# =======================================================================
# connect signals 
# =======================================================================

#ToolButtons
ui.jsonTB.clicked.connect(LocateJSON)
ui.linearOutputTB.clicked.connect(DefineLinearOutput)
ui.arealOutputTB.clicked.connect(DefineAerialOutput)

#Submit Push Button 
ui.submitPushButton.clicked.connect(SubmitButton)

# =======================================================================
# run app 
# =======================================================================
window.show()
sys.exit(app.exec_())

# =======================================================================
# Close QGIS
# =======================================================================
qgs.exitQgis()
sys.exit(exitcode)