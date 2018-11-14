import Tkinter as tk
import sqlite3 as sq
import datetime
from pollDb import *

master_headers = ["ISBN","Title","Subtitle","Author, Last","Author, First",
"2nd Author, Last", "2nd Author, First","3rd Author, Last","3rd Author, First",
"4th Author, Last","4th Author, First", "5th Author, Last", "5th Author, First",
"Publication Date", "Genre", "Subgenre", "Series", "Edition", "Position in Series",
"Format", "Publisher", "Owner"]

def create_connection():
    db = sq.connect("PittsFamilyLibrary.db")
    return db, db.cursor()

def close_connection(db):
    db.commit()
    db.close()

def getBasicData():

    db, c = create_connection()

    getAllBooks='''SELECT ISBN, Title, Publication_Date,
            Genre, Series FROM books ORDER BY Title'''

    c.execute(getAllBooks)
    booksData = list(c.fetchall())
    for i in range(len(booksData)):
        booksData[i] = list(booksData[i])

    authorsData =[]
    for i in range(len(booksData)):
        getAllAuthors = '''SELECT Author_Last, Author_First FROM authors WHERE
            ISBN = %d''' % (booksData[i][0])
        c.execute(getAllAuthors)
        authors = list(c.fetchall()[0])

        booksData[i] = booksData[i][:2] + authors + booksData[i][2:]

    close_connection(db)

    return booksData

def getAllData():
    pass

def setup():

    def make_intro_buttons():

        button_labels = ["Show All Books","Add a Book","Search","Quit"]

        show_book_button = tk.Button(button_frame, text=button_labels[0],width=14,
                                command = build_results_pane)
        add_book_button = tk.Button(button_frame, text = button_labels[1],width=14,
                                command = build_add_pane)
        search_button = tk.Button(button_frame, text = button_labels[2],width = 14,
                                command = build_search_pane)
        quit_button = tk.Button(button_frame, text= button_labels[3],width=14,
                                    command=quit)

        show_book_button.grid(row=0,column=0,padx=5,pady=5)
        add_book_button.grid(row=1,column=0,padx=5,pady=5)
        search_button.grid(row=2,column=0,padx=5,pady=5)
        quit_button.grid(row=4, column =0,padx=5,pady=5)

    global root; root = tk.Tk()
    root.title("This is the changed version of Alexandria, on the Testing Branch")
    global master; master = tk.Frame(root, bg="LightGoldenrod2")
    master.grid()


    global button_frame; button_frame = tk.Frame(master,bg="LightGoldenrod2")
    button_frame.grid(row=0,column=0)
    global data_frame; data_frame = tk.Frame(master,width=1500,height=450,bg="LightGoldenrod2")
    data_frame.grid(row=0,column=1)
    data_frame.grid_propagate(False)

    make_intro_buttons()

    root.mainloop()

def build_results_pane():

    def build_data_header():

        data_labels = [("ISBN",13),("Title",32),("Author, Last",16),
                        ("Author, First",16), ("Publication Year",16), ("Genre",12),
                        ("Series",12)]

        for i in range(len(data_labels)):
            x = tk.Label(data_frame, text=data_labels[i][0], bg="light blue")
            x.grid(row=0, column=i, padx=5, pady=5, ipadx = 5)

    for widget in data_frame.winfo_children():
        widget.destroy()

    build_data_header()

    records = getBasicData()

    for i in range(len(records)):
        for j in range(len(records[i])):

            x = tk.Label(data_frame, text = records[i][j], bg = "plum2")
            x.grid(row = i+1, column = j, padx = 5, pady = 5)

def build_add_pane():

    # A method that takes the add_fields Entries, gets the text from them,
    # and inputs them into a String that represents an SQL command that will
    # input that data into PittsFamilyLibrary.db database, books table
    def insert_book_data():

        def check_null(text):
            if not text:
                return "NULL"
            return text

        def minAuthorsFill(arr):
            flag = True
            for word in arr:
                if word is not 'NULL':
                    flag = False
            if flag:
                arr[1] = 'Anonymous'
            return arr


        db, c = create_connection()

        booksData = []
        authorsData = []
        for entry in bookFields:
            booksData.append(check_null(entry.get()))
        for entry in authFields:
            authorsData.append(check_null(entry.get()))
        authorsData = minAuthorsFill(authorsData)

        authorsData.append(booksData[2])#booksData[2] is the ISBN number

        sql1 = '''INSERT INTO books (Title, Subtitle, ISBN,
        Series, Position_in_Series, Genre, Subgenre, Publication_Date, Publisher,
        Format, Owner) VALUES '''
        sql1 += "("
        for thing in booksData:
            sql1 += "'" + thing + "', "

        sql1 = sql1[:-2] + ")"

        for i in range(len(authorsData)/2):
            if authorsData[i] is not "NULL" or authorsData[i+5] is not "NULL":
                sql2 = '''INSERT INTO authors(Author_First, Author_Last, ISBN) Values''' + "("
                sql2 += "'" + authorsData[i] + "', '" + authorsData[i+5] + "'," + authorsData[-1] + ")"
                c.execute(sql2)


        c.execute(sql1)
        close_connection(db)
        build_results_pane()

    # Clears the data_frame to make way for new
    for widget in data_frame.winfo_children():
        widget.destroy()

    # List that will store the Entry widgets for future reference
    bookFields = []
    authFields = []

    #(row, column, Text Field)
    #Stores the geometry and text information for the labels in the "Add A Book" pane
    x = tk.Label(data_frame, text = "ADD A BOOK TO THE LIBRARY", bg = "LightBlue")
    x.grid(row = 0, column = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10, columnspan = 3)
    label_data = [(1,0,"Title: "),(1,2,"Subtitle: "),(1,4,"ISBN: "),
        (2,0,"Author, First: "),(2,2,"Author, First: "),(2,4,"Author, First: "),
        (2,6,"Author, First: "),(2,8,"Author, First: "),(3,0,"Author, Last: "),
        (3,2,"Author, Last: "),(3,4,"Author, Last: "),(3,6,"Author, Last: "),
        (3,8,"Author, Last: "),(4,0,"Series: "),(4,2,"Series # : "),(5,0,"Genre: "),
        (5,2,"Subgenre: "),(6,0,"Publication Year: "),(6,2,"Publisher: "),(6,4,"Format: "),
        (7,0,"Owner: ")]

    #(row, column, Entry width)
    #Stores geometry and width infromation for the Entries in the "Add A Book" pane
    booksEntryData = [(1,1,32),(1,3,32),(1,5,13),(4,1,16),(4,3,16),
        (5,1,16),(5,3,16),(6,1,12),(6,3,16),(6,5,16),(7,1,6)]

    authorEntryData = [(2,1,16),(2,3,16),(2,5,16),(2,7,16),(2,9,16),(3,1,16),(3,3,16),(3,5,16),(3,7,16),(3,9,16)]

    # Loops that takes the the entry_data and label_data and builds the data pane
    for i in range(len(booksEntryData)-2):
        t = tk.Entry(data_frame, width = booksEntryData[i][2])
        t.grid(row = booksEntryData[i][0], column = booksEntryData[i][1])
        bookFields.append(t)

    var = tk.StringVar(data_frame); var.set("Mass Market PB")
    t = tk.OptionMenu(data_frame, var, "Mass Market PB", "Trade PB","Hard Back")
    t.grid(row = 6, column = 5)
    bookFields.append(var)

    var = tk.StringVar(data_frame); var.set("Patrick & Shelby")
    t = tk.OptionMenu(data_frame, var, "Patrick & Shelby","John & Kathy")
    t.grid(row = 7, column = 1)
    bookFields.append(var)

    for i in range(len(authorEntryData)):
        t = tk.Entry(data_frame, width = authorEntryData[i][2])
        t.grid(row = authorEntryData[i][0], column = authorEntryData[i][1])
        authFields.append(t)

    for i in range(len(label_data)):
        x = tk.Label(data_frame, text = label_data[i][2], bg = "LawnGreen")
        x.grid(row = label_data[i][0], column= label_data[i][1], padx = 10, pady = 10)

    b = tk.Button(data_frame,text = "Submit", command = insert_book_data)
    b.grid(row = 8, column = 0)

def build_search_pane():
    for widget in data_frame.winfo_children():
        widget.destroy()
    def search():
        pass

    # List that will store the Entry widgets for future reference
    search_fields = []
    search_values = ["","","","","","","","","","","","","","","","","","","","",""]
    x = tk.Label(data_frame, text = "SEARCH", bg = "LightBlue")
    x.grid(row = 0, column = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)

    #(row, column, Text Field)
    #Stores the geometry and text information for the labels in the "Search" pane
    label_data = [(1,0,"Title: "),(1,2,"Subtitle: "),(1,4,"ISBN: "),
        (2,0,"Author, First: "),(2,2,"Author, First: "),(2,4,"Author, First: "),
        (2,6,"Author, First: "),(2,8,"Author, First: "),(3,0,"Author, Last: "),
        (3,2,"Author, Last: "),(3,4,"Author, Last: "),(3,6,"Author, Last: "),
        (3,8,"Author, Last: "),(4,0,"Series: "),(4,2,"Series # : "),(5,0,"Genre: "),
        (5,2,"Subgenre: "),(6,0,"Publication Year: "),(6,2,"Publisher: "),(6,4,"Format: "),
        (7,0,"Owner: ")]
    #(row, column, Entry width)
    #Stores geometry and width infromation for the Entries in the "Add A Book" pane
    entry_data = [(1,1,32),(1,3,32),(1,5,13),(2,1,16),(2,3,16),(2,5,16),(2,7,16),
        (2,9,16),(3,1,16),(3,3,16),(3,5,16),(3,7,16),(3,9,16),(4,1,16),(4,3,16),
        (5,1,16),(5,3,16),(6,1,12),(6,3,16),(6,5,16),(7,1,6)]

    # Loop that takes the the entry_data and label_data and builds the data pane
    for i in range(21):
        x = tk.Label(data_frame, text = label_data[i][2], bg = "plum2")
        x.grid(row = label_data[i][0], column= label_data[i][1], padx = 10, pady = 10)

        t = tk.Entry(data_frame, width = entry_data[i][2])
        t.grid(row = entry_data[i][0], column = entry_data[i][1])
        search_fields.append(t)
    b = tk.Button(data_frame, width = 14,text = "Search!", command = search)
    b.grid(row = 8, column = 0, pady = 10)

def main():

    setup()
    root.mainloop()

if __name__ == '__main__':
    main()
