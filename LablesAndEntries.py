import Tkinter as tk

#code is unchanged, but now there are some comments!

def LEBuild(master, labels, locations, BackgroundColor = "white", EntWidth = 16):
    entries = []
#    master.title("Title updated on laptop")

    for i in range(len(labels)):
        col = 2*locations[i][1]
        x = tk.Label(master, text = labels[i], bg = BackgroundColor)
        x.grid(row=locations[i][0],column=col-1,padx=5,pady=5)

        entries.append(tk.Entry(master, width = EntWidth))
        entries[i].grid(row=locations[i][0],column=col,padx=5,pady=5)


    return entries

def LabelBuild(master, labels, locations, BackgroundColor = "white"):

    for i in range(len(labels)):
        x = tk.Label(master, text = labels[i], bg = BackgroundColor)
        x.grid(row =locations[0], column = locations[1])

def EntriesToTuple(entries):
    #Takes a list of Tkinter Entry objects, and returnts of just
    #the string literal contents of the list
    ReturnList = []
    for item in entries:
        ReturnList.append(item.get())

    return tuple(ReturnList)
