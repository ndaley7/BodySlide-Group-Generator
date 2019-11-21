#Import of Modules used
import os



#Tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *


#Local Application Imports
from ParsingBSGG.XMLIO import CreateConfigBSGGXML

#root = Tk()

 


def BodySlidePathSelect():
    #Init

    #Boolean
    bodyslideDirFound= False
    enableErrorLogging=False

    #Request Bodyslide Folder

    while (bodyslideDirFound==False):
        filename =  filedialog.askdirectory(initialdir = "/",title = "Select BodySlide Folder")

        #Check for existance of SliderGroups,SliderSets,SliderPresets,SliderCategories
        sliderCategoriesFound=os.path.isdir(filename+"/SliderCategories")
        print("SliderCategories= "+ str(sliderCategoriesFound))
        sliderGroupsFound=os.path.isdir(filename+"/SliderGroups")
        print("SliderGroups= "+ str(sliderGroupsFound))
        sliderPresetsFound=os.path.isdir(filename+"/SliderPresets")
        print("SliderPresets= "+ str(sliderPresetsFound))
        sliderSetsFound=os.path.isdir(filename+"/SliderSets")
        print("SliderSets= "+ str(sliderSetsFound))
        
        #Boolean Check for Creation
        if(sliderCategoriesFound and sliderGroupsFound and sliderPresetsFound and sliderSetsFound):
            #Toggle Found Boolean
            bodyslideDirFound=True

            #Check for Desired Error Log Status
            enableErrorLogging=messagebox.askyesno("Title","Would you like to enable Debug Logging?")

            #Create the ConfigBSGG.xml file
            CreateConfigBSGGXML(filename,enableErrorLogging)
            stringhold="placeholder"
        else:
            stringplace="placeholder"
        


        