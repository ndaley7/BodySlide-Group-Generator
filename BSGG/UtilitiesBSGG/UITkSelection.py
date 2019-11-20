#Imports:



#Tk
from tkinter import filedialog
from tkinter import *


root = Tk()

 


def CreateConfigBSGGXML():

    bodyslideDirFound= False

    #Request Bodyslide Folder

    while (bodyslideDirFound==False):
        root.filename =  filedialog.askdirectory(initialdir = "/",title = "Select BodySlide Folder")
        #Check for existance of SliderGroups,SliderSets,SliderPresets