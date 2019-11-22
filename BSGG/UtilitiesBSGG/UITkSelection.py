"""
    This file is part of:
    NIND's BodySlide Utilites
    by NIND

    Created to work with BodySlide 2 and Outfit Studio
    by Ousnius

    This software is provided 'as-is', without any express or implied
    warranty. In no event will the authors be held liable for any
    damages arising from the use of this software.

    Permission is granted to anyone to use this software for any
    purpose, including commercial applications, and to alter it and
    redistribute it freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must
    not claim that you wrote the original software. If you use this
    software in a product, an acknowledgment in the product documentation
    would be appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and
    must not be misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""
from BSGG.__main__ import g_DebugEnabled

#Import of Modules used
import os



#Tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Tk


#Local Application Imports
from ..ParsingBSGG.XMLIO import CreateConfigBSCGXML



#Create and Hide Root window
Tk().withdraw()

 

#This function opens a Tkinter folder select dialog to enable selection of the Bodyslide folder.  
#Loops until the four "Slider" folders are found in the same subdirectory
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
            enableErrorLogging=messagebox.askyesno("BodySlide Custom Grouper","Would you like to enable Debug Logging?")

            #Create the ConfigBSGG.xml file
            CreateConfigBSCGXML(filename,enableErrorLogging)
            
        else:
            messagebox.showinfo("BodySlide Custom Grouper","Slider Folder(s) not Detected.\n See Terminal/Console")

#Renders a TKinter dialog with a custom question and title.  Returns True/False
def CustomYesNoTF(stringTitle,stringContent):
   
    #Display Yes/No Dialog
    result=messagebox.askyesno(stringTitle,stringContent)

    return result

#Renders a TKinter dialog with a custom message and Title
def CustomOK(stringTitle,stringContent):
   
    #Display Okay Dialog
    messagebox.showinfo(stringTitle,stringContent)

    
            
        


        