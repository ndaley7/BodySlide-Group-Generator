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
tree = tkinter.ttk.Treeview(root, height=4)

tree['show'] = 'headings'
tree['columns'] = ('Badge Name', 'Requirement', 'Cost', 'Difficulty')
tree.heading("#1", text='Badge Name', anchor='w')
tree.column("#1", stretch="no")
tree.heading("#2", text='Requirement', anchor='w')
tree.column("#2", stretch="no")
tree.heading("#3", text='Cost', anchor='w')
tree.column("#3", stretch="no")
tree.heading("#4", text='Difficulty', anchor='w')
tree.column("#4", stretch="no")
tree.pack()

tree.insert("", "end", values=["IT Badge", "Track Computer", "$1.50", "2"])
tree.insert("", "end", values=["Selfless Badge", "Track Yourself", "$100.50", "10"])
tree.insert("", "end", values=["Tracking Badge", "Track Animal", "$4.50", "7"])

tree.bind("<Return>", lambda e: select())

root.mainloop()