import Tkinter as tk
import sqlite3 as sq
import datetime
from pollDb import *
import LablesAndEntries as LAE
import build_db as BDB


def create_connection():
    # A function that generates a connection to the Alexandria.db database,
    # which stores the book data for the library. Returns a connection object to the
    # database itself, which is required to shut down the connection later, and
    # a cursor object which is required to interact with the database.

    db = sq.connect("Alexandria.db")
    return db, db.cursor()

def close_connection(db):
    # A function that takes a connection object, commits any changes to the
    # connected database, then closes the connection.

    db.commit()
    db.close()

def CleanupRoot():
    #Strips all geometry and added visuals from the root frame,
    #adds essential visual tools meant for every frame (ie menus)
    #pathing the way for more visauls without any clutter
    for widget in root.winfo_children():
        widget.destroy()
    BuildMenus()

def BuildMenus():
    menubar = tk.Menu(root)
    SearchMenu = tk.Menu(menubar, tearoff = 0)
    SearchMenu.add_command(label = "Search by ISBN", command = BuildSearchPane)
    SearchMenu.add_command(label = "Search by Title", command = BuildSearchPane)

    TestMenu = tk.Menu(menubar, tearoff = 0)
    TestMenu.add_command(label = "Test Function", command = quit)
    TestMenu.add_command(label = "Reset Database", command = BDB.main)


    menubar.add_cascade(label="Search",menu = SearchMenu)
    menubar.add_command(label="Add", command = BuildAddPane)
    menubar.add_cascade(label = "TEST", menu = TestMenu)
    root.config(menu=menubar)

def GetAuthorsFromISBN(isbn):
    # A function that takes in an ISBN number, and returns a list of tuples,
    # each of which holds the first and last name of an author associated with
    # that ISBN

    db, c = create_connection()

    getID = "SELECT Author_ID from BookToAuthors WHERE ISBN = %d" % isbn
    c.execute(getID)
    AuthorIDsAsTuples = c.fetchall()

    AuthorIDList = []
    for tup in AuthorIDsAsTuples:
        AuthorIDList.append(tup[0])

    if len(AuthorIDList) > 1:
        AuthorIDTuple = tuple(AuthorIDList)
        getNames = "SELECT Author_First, Author_Last from Authors WHERE Author_ID IN %s" % str(AuthorIDTuple)
    elif len(AuthorIDList) == 1:
        getNames = "SELECT Author_First, Author_Last from Authors WHERE Author_ID = %d" % AuthorIDList[0]
    else:
        msg = "Failed to access authors with ISBN %d" % isbn
        print(msg)
        return
    c.execute(getNames)
    AuthorNames = list(c.fetchall())
    close_connection(db)
    return AuthorNames

def GetBasicData():

    db, c = create_connection()


    getAllBooks='''SELECT ISBN, Title, Publication_Date,
            Genre, Series FROM books ORDER BY Title'''

    c.execute(getAllBooks)
    booksData = list(c.fetchall())
    for i in range(len(booksData)):
        booksData[i] = list(booksData[i])

    authorsData =[]
    for i in range(len(booksData)):
        HeadlineAuthor = GetAuthorsFromISBN(booksData[i][0])[0]
        booksData[i] = booksData[i][:2]  +list(HeadlineAuthor) + booksData[i][2:]

    close_connection(db)

    return booksData

def BuildMainMenu():
    #Creates the main menu pane. This pane holds buttons that will implement the
    #functionality of the program, and will be implemented in all "back to menu"
    #buttons in other panes.
    CleanupRoot()


    master = tk.Frame(root, width = 500, height = 500, bg = "LightGoldenrod2")
    master.grid()
    master.grid_propagate(0)

    def MakeIntroButtons():

        button_labels = ["Show All Books","Add a Book","Search","Quit"]

        show_book_button = tk.Button(master, text=button_labels[0],width=14,
                                command = BuildResultsPane)
        add_book_button = tk.Button(master, text = button_labels[1],width=14,
                                command = BuildAddPane)
        search_button = tk.Button(master, text = button_labels[2],width = 14,
                                command = BuildSearchPane)
        quit_button = tk.Button(master, text= button_labels[3],width=14,
                                    command=quit)

        show_book_button.grid(row=0,column=0,padx=5,pady=5)
        add_book_button.grid(row=1,column=0,padx=5,pady=5)
        search_button.grid(row=2,column=0,padx=5,pady=5)
        quit_button.grid(row=4, column =0,padx=5,pady=5)

    MakeIntroButtons()

def Setup():
    #Builds the starting frames and Tkinter windows, in which all other functionality is built
    global root; root = tk.Tk()
    root.title("Alexandria")
    root.geometry("+0+0")


    BuildMainMenu()
    root.mainloop()

def BuildResultsPane():

    CleanupRoot()
    master = tk.Frame(root, bg = "LightGoldenrod2")
    master.grid()

    ButtonFrame = tk.Frame(master, bg = "LightGoldenrod2")
    ButtonFrame.grid(row = 0, column = 0)

    DataFrame = tk.Frame(master, bg = "LightGoldenrod2")
    DataFrame.grid(row = 0, column = 1)

    BackButtton = tk.Button(ButtonFrame,text = "Back", command = BuildMainMenu)
    BackButtton.grid(padx = 5, pady = 5)

    def BuildDataHeader():

        data_labels = [("ISBN",13),("Title",32),("Author, Last",16),
                        ("Author, First",16), ("Publication Year",16), ("Genre",12),
                        ("Series",12)]

        for i in range(len(data_labels)):
            x = tk.Label(DataFrame, text=data_labels[i][0], bg="light blue")
            x.grid(row=0, column=i, padx=5, pady=5, ipadx = 5)



    BuildDataHeader()

    records = GetBasicData()

    for i in range(len(records)):
        for j in range(len(records[i])):

            x = tk.Label(DataFrame, text = records[i][j], bg = "plum2")
            x.grid(row = i+1, column = j, padx = 5, pady = 5)

def InsertBookData():

    db, cur = create_connection()

    flag = InsertDataSanitationChecks(db, cur)
    if flag:
        print("Passed Sanitation Checks, Inserting (Not)")

        first = AuthorFields[0].get()
        if not first:
            first = "None"
        middle = AuthorFields[1].get()
        if not middle:
            middle = "None"
        last = AuthorFields[2].get()
        if not last:
            last = "None"
        print(first,middle,last)
        cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                Author_Middle IS %r AND
                Author_Last IS %r''' %(first, middle, last)

        print(cmd)
        cur.execute(cmd)

        if not cur.fetchall():
            pass


        close_connection(db)


    else:
        print("Problems with data, double check data")

def InsertDataSanitationChecks(db, cur):
    ErrorText.config(text = "")
    title = BookFields[0].get()
    isbn = BookFields[2].get()
    if not isbn or len(title) == 0:
        ErrorText.config(text = "You need at least a title and ISBN to add a book")
        return False

    cmd = "SELECT Title FROM Books WHERE ISBN = %d" % int(isbn)
    cur.execute(cmd)
    if cur.fetchall():
        ErrorText.config(text = "Cannot add repeat ISBN Numbers.")
        return False

    return True

def BuildAddPane():

    # A method that takes the add_fields Entries, gets the text from them,
    # and inputs them into a String that represents an SQL command that will
    # input that data into Alexandria.db database, books table


    CleanupRoot()

    global NumAuthors; NumAuthors = 1
    global AuthorFields; AuthorFields = []
    global BookFields
    global ErrorText

    def MoreAuthors():
        global NumAuthors; global AuthorFields
        AuthLabels = ["Author, First: ","Middle: ", "Last: "]
        AuthLocations = [(NumAuthors+1, 1), (NumAuthors+1, 2), (NumAuthors+1,3)]
        AuthorFields += LAE.LEBuild(AuthorFrame, AuthLabels, AuthLocations, BackgroundColor = "thistle")
        NumAuthors += 1

    master = tk.Frame(root, bg = "LightGoldenrod2")
    master.grid()

    ButtonFrame = tk.Frame(master, bg = "LightGoldenrod2")
    ButtonFrame.grid(row = 0, column = 0)

    DataFrame = tk.Frame(master, bg = "LightGoldenrod2")
    DataFrame.grid(row = 0, column = 1)

    RightFrame = tk.Frame(master, bg = "LightGoldenrod2")
    RightFrame.grid(row = 0, column = 2)

    AuthorFrame = tk.Frame(RightFrame, bg = "LightGoldenrod2")
    AuthorFrame.grid(row = 1, column = 0)

    AuthorButtonFrame = tk.Frame(RightFrame, bg = "LightGoldenrod2")
    AuthorButtonFrame.grid(row = 0, column = 0)

    BackButtton = tk.Button(ButtonFrame, text = "Back", command = BuildMainMenu)
    BackButtton.grid(row = 1, column = 0)

    InsertButton = tk.Button(ButtonFrame, text = "Add Book!", padx = 10, pady = 10, command = InsertBookData)
    InsertButton.grid(row = 2, column = 0, pady = 20)

    MoreAuthorsButton = tk.Button(AuthorButtonFrame, text = "Another Author", command = MoreAuthors,
            padx = 10, pady = 10)
    MoreAuthorsButton.grid(row = 0, column = 1)

    x = tk.Label(ButtonFrame, text = "ADD A BOOK TO THE LIBRARY", bg = "LightBlue")
    x.grid(row = 0, column = 0, padx = 10, pady = 10, ipadx = 10, ipady = 10)

    BookLabelTexts = ["Title: ", "Subtitle: ", "ISBN: ", "Series: ","Series #: ",
            "Genre: ","Subgenre: ", "Publication Year: ", "Publisher: "]
    BookLabelLocations = [(1,1),(1,2),(1,3),(3,1),(3,2),(5,1),(5,2),(7,1),(7,2),(7,3)]

    BookFields = LAE.LEBuild(DataFrame, BookLabelTexts, BookLabelLocations, BackgroundColor = "thistle")
    x = tk.Label(DataFrame, text = "Format: ", bg = "thistle")
    x.grid(row = 7, column = 5)

    FormatOption = tk.StringVar(DataFrame); FormatOption.set("Mass Market PB")
    t = tk.OptionMenu(DataFrame, FormatOption, "Mass Market PB", "Trade PB","Hard Back")
    t.grid(row = 7, column = 6)
    BookFields.append(FormatOption)

    x = tk.Label(DataFrame, text = "Owner: ", bg = "thistle")
    x.grid(row = 9, column = 1)

    OwnerOption = tk.StringVar(DataFrame); OwnerOption.set("Patrick & Shelby")
    t = tk.OptionMenu(DataFrame, OwnerOption, "Patrick & Shelby","John & Kathy")
    t.grid(row = 9, column = 2)
    BookFields.append(OwnerOption)

    ErrorText = tk.Label(DataFrame, text = "", bg = "LightGoldenrod2", fg = "red", font = "bold")
    ErrorText.grid(row = 10, column = 1, columnspan = 5)

    MoreAuthors()

def BuildSearchPane():
    CleanupRoot()


def main():

    Setup()
    BuildMainMenu()

    root.mainloop()

if __name__ == '__main__':
    main()
