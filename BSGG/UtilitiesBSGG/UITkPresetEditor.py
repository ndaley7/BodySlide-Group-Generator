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

import tkinter as tk
import tkinter.ttk

def select():
    curItems = tree.selection()
    tk.Label(root, text="\n".join([str(tree.item(i)['values']) for i in curItems])).pack()

root = tk.Tk()
tree = tkinter.ttk.Treeview(root, height=10)

tree["columns"]=("one","two","three")
tree.column("#0", width=270, minwidth=270, stretch=tk.YES)
tree.column("one", width=150, minwidth=150, stretch=tk.YES)
tree.column("two", width=400, minwidth=200)
tree.column("three", width=80, minwidth=50, stretch=tk.YES)

tree.heading("#0",text="Name",anchor=tk.W)
tree.heading("one", text="Date modified",anchor=tk.W)
tree.heading("two", text="Type",anchor=tk.W)
tree.heading("three", text="Size",anchor=tk.W)

#Level 1
folder1=tree.insert("", 1, "", text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
tree.insert("", 2, "", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
# Level 2
tree.insert(folder1, "end", "", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
tree.insert(folder1, "end", "", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
tree.insert(folder1, "end", "", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))

tree.pack(side=tk.TOP,fill=tk.X)

tree.bind("<Return>", lambda e: select())

root.mainloop()