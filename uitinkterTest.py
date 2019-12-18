import tkinter as tk
import tkinter.ttk as ttk

#Local Imports
from BSGG.UtilitiesBSGG.BSCGLogging import BSCGDebugInit
from BSGG.UtilitiesBSGG.BSCGLogging import LoggingInfoBSCG
from BSGG.UtilitiesBSGG.FileIO import GetFileList


class PresetApp:
    #Init Class Variables


    #Debug Init
    BSCGDebugInit()
    #Paths listed here for seperate troubleshooting of the module

    sliderPresetPath="c:/Users/ndaley/Documents/GitHub/BodySlide-Group-Generator/BodySlide_Sample/SliderPresets"
    sliderGroupPath="c:/Users/ndaley/Documents/GitHub/BodySlide-Group-Generator/BodySlide_Sample/SliderGroups"

    #Generate lists of paths to .xml and .osp files in the SliderSet Folder(DEBUG done)
    LoggingInfoBSCG("PRESET CORE: Reading SliderSet and SliderGroup files")
    
    sliderPresetXMLPaths=GetFileList(sliderPresetPath,'*.xml')
    sliderGroupPaths=GetFileList(sliderGroupPath,'*.xml')

    def __init__(self):
        #Initialize Variables
        

        #Setup Operations

        #Initialize left (Preset) Tree , and right (Group) Tree

        #Read in Preset Files and poplulate Left Tree with Preset->List of Groups in Preset

        #Initialize Root And TK Application
        self.root = tk.Tk()

        
        self.tree = ttk.Treeview()
        self.tree.pack()
        for i in range(10):
            self.tree.insert("", "end", text="Item %s" % i)
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.root.mainloop()
    
    
    
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