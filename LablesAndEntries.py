import Tkinter as tk

def BasicBuild(master, lables, locations, BackgroundColor = "white", EntWidth = 16):
    entries = []
    master.title("Title updated on labtop")

    for i in range(len(lables)):
        col = 2*locations[i][1]
        x = tk.Label(master, text = lables[i], bg = BackgroundColor)
        x.grid(row=locations[i][0],column=col-1,padx=5,pady=5)

        entries.append(tk.Entry(master, width = EntWidth))
        entries[i].grid(row=locations[i][0],column=col,padx=5,pady=5)


    return master, entries
