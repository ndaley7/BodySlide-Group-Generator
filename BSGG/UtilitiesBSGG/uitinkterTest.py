import tkinter as tk
import tkinter.ttk as ttk

#Paths listed here for seperate troubleshooting of the module

SliderPresetPath="c:/Users/ndaley/Documents/GitHub/BodySlide-Group-Generator/BodySlide_Sample/SliderPresets"
SliderGroupPath="c:/Users/ndaley/Documents/GitHub/BodySlide-Group-Generator/BodySlide_Sample/SliderGroups"

class PresetApp:
    def __init__(self):
        #Initialize Root
        self.root = tk.Tk()

        #Initialize left (Preset) Tree , and right (Group) Tree

        #Read in Preset Files and poplulate Left Tree with Preset->List of Groups in Preset
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