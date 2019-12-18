import os
import sys
import tkinter as tk
import tkinter.ttk as ttk

#Local Imports
from BSGG.UtilitiesBSGG.BSCGLogging import BSCGDebugInit
from BSGG.UtilitiesBSGG.BSCGLogging import LoggingInfoBSCG
from BSGG.UtilitiesBSGG.FileIO import SliderSetBackup
from BSGG.UtilitiesBSGG.FileIO import SliderRevertCheck
from BSGG.UtilitiesBSGG.FileIO import GetFileList
from BSGG.ParsingBSGG.XMLIO import ParseSliderGroupXML


class PresetApp:
    #Init Class Variables
    presetFilesList=[]
    groupFilesList=[]

    

    

    def __init__(self):
        #Initialize Variables
        #Preset OutfitGroup List
        self.g_GroupOutfitTreeviewTuple=[]
        #Debug Init
        BSCGDebugInit()
        #Paths listed here for seperate troubleshooting of the module

        sliderPresetPath="c:/Users/ndaley/Documents/GitHub/BodySlide-Group-Generator/BodySlide_Sample/SliderPresets/"
        sliderGroupPath="c:/Users/ndaley/Documents/GitHub/BodySlide-Group-Generator/BodySlide_Sample/SliderGroups/"

        #Generate lists of paths to .xml and .osp files in the SliderSet Folder(DEBUG done)
        LoggingInfoBSCG("PRESET CORE: Reading SliderSet and SliderGroup files")
        

        #Backup Preset and Group Files
        SliderSetBackup(sliderPresetPath)
        SliderSetBackup(sliderGroupPath)
        
        #Write out Preset and Group File Lists
        sliderPresetXMLPaths=GetFileList(sliderPresetPath,'*.xml')
        sliderGroupPaths=GetFileList(sliderGroupPath,'*.xml')

        
        #Initialize left (Preset) Tree , and right (Group) Tree
        #Read in the Preset and Group files
        LoggingInfoBSCG("PRESET CORE: Parsing SliderGroup XML")
        for GroupFile in sliderGroupPaths:
            #XMLEncodingConfirm(setXML)
            fileWithExtension=os.path.basename(GroupFile)
            fileWithoutExtension=os.path.splitext(fileWithExtension)[0] 
            currentGroup=ParseSliderGroupXML(GroupFile)
            self.g_GroupOutfitTreeviewTuple.extend(currentGroup)


        #Read in Preset Files and poplulate Left Tree with Preset->List of Groups in Preset

        #Initialize Root And TK Application
        self.root = tk.Tk()

        
        self.tree = ttk.Treeview()
        self.tree.pack()
        for i in range(10):
            self.tree.insert("", "end", text="Item %s" % i)
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.root.mainloop()
    
   

    def CreateGroupTreeview(self,PresetGroupTuple):

        return GroupTreeiviewStatus
    
    #Original __init__ for reference
    def Original__init__(self):
        self.root = tk.Tk()
        self.tree = ttk.Treeview()
        self.tree.pack()
        for i in range(10):
            self.tree.insert("", "end", text="Item %s" % i)
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.root.mainloop()

    def OnDoubleClick(self, event):
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item,"text"))

if __name__ == "__main__":
    app = PresetApp()