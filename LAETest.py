import Tkinter as tk
import LablesAndEntries as lae

root = tk.Tk()

lables = ["1", "2", "3"]
loc = [(1,1),(1,2),(2,1)]

mainframe, entries = lae.BasicBuild(root,lables,loc)



def GetEntries():
    for ent in entries:
        print ent.get()

b = tk.Button(mainframe, text = "get", command = GetEntries)
b.grid(row= 4, column =0)

mainframe.mainloop()
