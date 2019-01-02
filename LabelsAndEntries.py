import tkinter as tk

#code is unchanged, but now there are some comments!

def LEBuild(master, labels, locations, BackgroundColor = "white", EntryWidths = []):

    entries = []

    if len(EntryWidths) is not len(labels):
        EntryWidths = []
        for i in range(len(labels)):
            EntryWidths.append(16)

    for i in range(len(labels)):
        col = 2*locations[i][1]
        x = tk.Label(master, text = labels[i], bg = BackgroundColor, anchor = tk.E)
        x.grid(row=locations[i][0]-1,column=col-1,padx=5,pady=5)

        entries.append(tk.Entry(master, width = EntryWidths[i]))
        entries[i].config(justify = tk.LEFT)
        entries[i].grid(row=locations[i][0]-1,column=col,padx=5,pady=5,sticky=tk.W)


    return entries

def LabelBuild(master, labels, locations, BackgroundColor = "white", LableWidths = [],st = None):

        for i in range(len(labels)):
            x = tk.Label(master, text = labels[i], bg = BackgroundColor)
            x.grid(row =locations[i][0]-1, column = locations[i][1]-1, padx=5, pady=5, sticky = st)

def EntriesToTuple(entries):
    #Takes a list of Tkinter Entry objects, and returnts of just
    #the string literal contents of the list
    ReturnList = []
    for item in entries:
        ReturnList.append(item.get())

    return tuple(ReturnList)
