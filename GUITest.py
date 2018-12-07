import Tkinter as tk

root = tk.Tk()

master = tk.Frame(root, bg = "blue", width = 500, height = 500)
master.grid()

def Hello():
    print("Hello World!")

menubar = tk.Menu(master)
menubar.add_command(label="Hello", command = Hello)
menubar.add_command(label="Quit", command = quit)
root.config(menu=menubar)
root.mainloop()
