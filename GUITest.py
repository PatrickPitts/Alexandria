import Tkinter as tk

root = tk.Tk()

master = tk.Frame(root, bg = "blue", width = 5000, height = 5000)
master.grid()

def Hello():
    print("Hello World!")

menubar = tk.Menu(root)
menubar.add_command(label="Hello", command = Hello)
menubar.add_command(label="Quit", command = quit)
root.config(menu=menubar)

Outer = tk.Frame(master, bg = "red", width = 1500, height=5200)
Outer.grid()
for i in range(5):
    color="white"
    if i%2 == 0:
        color = "khaki1"
    else:
        color = "LightGoldenrod2"

    x = tk.Frame(Outer,bg = color,width=1000, height = 20)
    x.grid(row=i, column = 0)
    x.grid_propagate(False)

    l = tk.Label(x, text = i, bg=color)
    l.grid()
#
# fr1 = tk.Frame(root, bg = "red",width = 100, height = 100)
# fr1.grid(row =0, column =0)
# fr1.grid_propagate(False)
#
# l = tk.Label(fr1, text = "0")
# l.grid()
#
# fr2 = tk.Frame(root, bg = "blue",width = 100, height = 100)
# fr2.grid(row=0, column=1)
# fr2.grid_propagate(False)
#
# l = tk.Label(fr2, text = "1")
# l.grid()

root.mainloop()
