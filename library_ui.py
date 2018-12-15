import Tkinter as tk
import sqlite3 as sq
import datetime
import pollDb as PDB
import LablesAndEntries as LAE
import build_db as BDB

def test():
    print(GetBasicData())
    print(GetBasicData("isbn",9781593275679))

    pass

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

def SearchByISBN():
    # TODO: Implement search functionality
    def ExecuteISBNSearch():
        #results = GetBasicData("isbn")
        pass

    SearchPane = tk.Toplevel(bg = "khaki1")
    SearchPane.title("Search By ISBN")

    l = tk.Label(SearchPane, text = "ISBN: ", bg = "khaki1", width = 20)
    l.grid(row = 0, column = 0, padx = 5, pady = 5)

    SearchEntry = tk.Entry(SearchPane, width = 13)
    SearchEntry.grid(row=0, column = 1, padx = 5, pady = 5)

    SearchButton = tk.Button(SearchPane, text = "Search!", command = lambda x = SearchEntry.get(): GetBasicData("isbn",x))
    SearchButton.grid(row=1, column = 1, padx = 5, pady = 5)

def CleanupRoot():
    #Strips all geometry and added visuals from the root frame,
    #adds essential visual tools meant for every frame (ie menus)
    #pathing the way for more visauls without any clutter
    for widget in root.winfo_children():
        widget.destroy()
    BuildMenus()

def BuildMenus():
    #This function builds the Menu widget for the main window
    menubar = tk.Menu(root)
    SearchMenu = tk.Menu(menubar, tearoff = 0)
    SearchMenu.add_command(label = "Search by ISBN", command = SearchByISBN)
    SearchMenu.add_command(label = "Search by Title", command = BuildSearchPane)

    TestMenu = tk.Menu(menubar, tearoff = 0)
    TestMenu.add_command(label = "Test Function", command = test)
    TestMenu.add_command(label = "Reset Database", command = BDB.main)
    TestMenu.add_command(label = "Poll Database", command = PDB.main)


    menubar.add_cascade(label="Search",menu = SearchMenu)
    menubar.add_command(label="Add", command = BuildAddPane)
    menubar.add_cascade(label = "TEST", menu = TestMenu)
    menubar.add_command(label = "QUIT", command = quit)
    root.config(menu=menubar)

def FullBookDisplay(isbn):
    ResultsPane = tk.Toplevel(bg= "khaki1")
    l = tk.Label(ResultsPane, text = isbn)
    l.grid()

def GetAuthorsFromISBN(isbn):
    # A function that takes in an ISBN number, and returns a list of tuples,
    # each of which holds the first, middle, and last name of an author
    # associated with that ISBN

    db, c = create_connection()

    getID = "SELECT Author_ID from BookToAuthors WHERE ISBN = %d" % isbn
    c.execute(getID)
    AuthorIDsAsTuples = c.fetchall()

    AuthorIDList = []
    for tup in AuthorIDsAsTuples:
        AuthorIDList.append(tup[0])

    if len(AuthorIDList) > 1:
        AuthorIDTuple = tuple(AuthorIDList)
        getNames = "SELECT Author_First, Author_Middle, Author_Last from Authors WHERE Author_ID IN %s" % str(AuthorIDTuple)
    elif len(AuthorIDList) == 1:
        getNames = "SELECT Author_First, Author_Middle, Author_Last from Authors WHERE Author_ID = %d" % AuthorIDList[0]
    else:
        msg = "Failed to access authors with ISBN %d" % isbn
        print(msg)
        return
    c.execute(getNames)
    AuthorNames = list(c.fetchall())
    close_connection(db)
    return AuthorNames

def GetBasicData(*command):

    db, c = create_connection()
    if not command:
        GetBooks='''SELECT ISBN, Title, Publication_Date,
        Genre, Series FROM books ORDER BY Title'''

    elif command[0] is "isbn":
        GetBooks = '''SELECT ISBN, Title, Publication_Date,
        Genre, Series FROM books WHERE isbn IS %d ORDER BY Title''' % command[1]

    elif command[0] is "genre":
        GetBooks = '''SELECT ISBN, Title, Publication_Date, Genre,
        Genre, Series FROM books WHERE genre IN %r ORDER BY Title''' % command[1]

    c.execute(GetBooks)
    booksData = list(c.fetchall())
    for i in range(len(booksData)):
        booksData[i] = list(booksData[i])

    authorsData =[]
    for i in range(len(booksData)):
        HeadlineAuthorTuple = GetAuthorsFromISBN(booksData[i][0])[0]
        HeadlineAuthor = [""]
        for x in HeadlineAuthorTuple:
            if x != u'None':
             HeadlineAuthor[0] += x + " "
        booksData[i] = booksData[i][:2]  + HeadlineAuthor + booksData[i][2:]

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

    DataFrame = tk.Frame(root, bg = "LightGoldenrod2")
    DataFrame.grid(row = 1, column = 0)

    HeaderFrame = tk.Frame(root, bg = "LightBlue")
    HeaderFrame.grid(row = 0, column = 0)

    LabelWidths = [13,64,16,16,16,32,2]

    DataLabels = ["ISBN","Title","Headline Author", "Publication Year", "Genre","Series",""]

    for i in range(len(DataLabels)):
        x = tk.Label(HeaderFrame, text=DataLabels[i], bg="LightBlue", width = LabelWidths[i])
        x.grid(row=0, column=i)

    records = GetBasicData()
    MoreButtons = []
    for i in range(len(records)):
        if i%2 == 0:
            color = "LightGoldenrod2"
        else:
            color = "khaki1"

        f = tk.Frame(DataFrame, bg = color)
        f.grid()
        NumFields = len(records[i])
        for j in range(NumFields):

            l = tk.Label(f, text = records[i][j], width = LabelWidths[j], bg = color)
            l.grid(row = i+1, column = j)
        ISBNToPass = records[i][0]
        MoreButtons.append(tk.Button(f, text = "...", command = lambda x = ISBNToPass: FullBookDisplay(x)))
        MoreButtons[i].grid(row = i+1, column = NumFields + 1)
def InsertBookData():
    #Method that gathers the data from the the Add A Book pane,
    #checks for duplicate data, and inserts it into the Alexandria database
    db, cur = create_connection()

    flag = InsertDataSanitationChecks(db, cur)
    if flag:
        print("Passed Sanitation Checks, Inserting (Not)")

        #AuthorsData will be in a repeating format of
        #(Author_First, Author_Middle, Author_Last, repeat those 3 for each author)
        AuthorData = LAE.EntriesToTuple(AuthorFields)

        #BookData will be in the format of
        #(Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
        #Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        BookData = LAE.EntriesToTuple(BookFields)
        for i in range(0, len(AuthorData), 3):
            #checks to see if the entered Author data is already in the database.
            first = AuthorData[i]
            if not first:
                first = "None"
            middle = AuthorData[i+1]
            if not middle:
                middle = "None"
            last = AuthorData[i+2]
            if not last:
                last = "None"
            cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                    Author_Middle IS %r AND
                    Author_Last IS %r''' %(first, middle, last)

            cur.execute(cmd)
            AuthorID = cur.fetchall()
            #this if statement will execute if the author name set is not already in
            #the database
            if not AuthorID:
                print("That author isnt in the database!")
                cmd = ''' INSERT INTO Authors(Author_First, Author_Middle, Author_Last)
                    VALUES(%r, %r, %r)''' % (first, middle, last)
                cur.execute(cmd)
                cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                        Author_Middle IS %r AND
                        Author_Last IS %r''' %(first, middle, last)

                cur.execute(cmd)
                AuthorID = cur.fetchall()
            cmd = '''INSERT INTO BookToAuthors (Author_ID, ISBN) VALUES
            (%r, %r)''' % (AuthorID[0][0], BookData[2])
            cur.execute(cmd)
            #(Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
            #Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        cmd = '''INSERT INTO Books (Title, Subtitle, ISBN, Series, Position_in_Series,
                Genre, Subgenre, Publication_Date, Publisher, Format, Owner) VALUES
                %s '''%(BookData,)
        cur.execute(cmd)



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
    if len(isbn) is not 13 or len(isbn) is not 10:
        ErrorText.config(text = "ISBN needs to be either 10 or 13 characters long")
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
