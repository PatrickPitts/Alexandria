import tkinter as tk
import sqlite3 as sq
import pollDb as PDB
import LabelsAndEntries as LAE
import build_db as BDB


class Book():
    # an object that represents a book, to be worked with programmaticallyself.
    # typcally, a Book object is created to collect and aggregate relevant data
    # on a book identified by it's ISBN number. That data is then pulled from the books
    # object, usually to fill in the UI.
    def __init__(self, isbn):

        self.isbn = isbn

        self.Authors = []
        self.CondensedAuthorNames = []
        self.BasicInfo = []
        self.FullBookInfo = []

        self.cmd = '''SELECT Books.ISBN, Books.Title, Books.Subtitle,
        Books.Publication_Date, Books.Genre, Books.Subgenre, Books.Series,
        Books.Position_in_Series, Books.Format, Books.Publisher, Books.Owner, Books.Edition,
        Authors.Author_First, Authors.Author_Middle, Authors.Author_Last
            FROM BookToAuthors
                INNER JOIN Authors ON
                    Authors.Author_ID = BookToAuthors.Author_ID
                INNER JOIN BOOKS ON
                    Books.ISBN = BookToAuthors.ISBN WHERE Books.ISBN is %d''' % self.isbn

        cur.execute(self.cmd)

        self.DataResults = cur.fetchall()

        # [ISBN 0, Title 1, Subtitle 2, Pub Date 3, Genre 4, Subgenre 5,
        # Series 6, Pos. in Series 7, Book Format 8, Publisher 9, Owner 10]

        self.BookData = list(self.DataResults[0][:12])

        for i in range(len(self.DataResults)):
            self.Authors.append(self.DataResults[i][12:15])

        for ListOfNames in self.Authors:
            self.name = ""
            for i in range(len(ListOfNames)):
                if ListOfNames[i] != u'None':
                    self.name += ListOfNames[i] + " "
            self.CondensedAuthorNames.append(self.name[:-1])

        self.BasicInfo += self.BookData[:2]
        self.BasicInfo.append(self.CondensedAuthorNames[0])
        self.BasicInfo += self.BookData[3:5]
        self.BasicInfo.append(self.BookData[6])

        self.FullBookInfo = self.BookData

        for name in self.CondensedAuthorNames:
            self.FullBookInfo.append(name)

    def GetBasicData(self):
        return self.BasicInfo

    def GetFullBookData(self):
        return self.FullBookInfo


def test():
    cmd = "SELECT * from Books where ISBN IS 3"
    cur.execute(cmd)
    print(cur.fetchall())
    pass


def create_connection():
    # A function that generates a connection to the Alexandria.db database,
    # which stores the book data for the library. Returns a connection object to the
    # database itself, which is required to shut down the connection later, and
    # a cursor object which is required to interact with the database.

    db = sq.connect("Alexandria.db")
    return db, db.cursor()


def CloseConnection(db):
    # A function that takes a connection object, commits any changes to the
    # connected database, then closes the connection.

    db.commit()
    db.close()


def Search():
    def BuildSearchCommand():

        # The rest of the code in the Execute Search function relies on this
        # select command returning these exact parameters, in this order. If changes
        # are to be made to this SQL Command, then many other changes in this
        # funciton will need to be made as well.
        cmd = '''SELECT Books.ISBN FROM BookToAuthors
                INNER JOIN Authors ON
                    Authors.Author_ID = BookToAuthors.Author_ID
                INNER JOIN BOOKS ON
                    Books.ISBN = BookToAuthors.ISBN WHERE '''

        for i in range(len(SearchEntries) - 1):
            SearchValue = SearchEntries[i].get()
            if SearchValue:
                try:
                    SearchValue = int(SearchValue)
                    cmd += "Books.%s IS %d AND " % (SQLSearchOptions[i], SearchValue)

                except ValueError:

                    cmd += "Books.%s IS %r AND " % (SQLSearchOptions[i], SearchValue)

        AuthorName = SearchEntries[-1].get()
        AuthorNameList = AuthorName.split()
        AuthorTableColumns = ["Author_First", "Author_Middle", "Author_Last"]

        for name in AuthorNameList:
            cmd += '''(Authors.Author_First IS %r
                OR Authors.Author_Middle IS %r
                OR Authors.Author_Last IS %r) OR  ''' % (name, name, name)

        try:
            cur.execute(cmd[:-5])
            Results = list(cur.fetchall())[0]
            BuildBasicResultsPane(GetBasicData(Results))

        except sq.OperationalError:
            BuildBasicResultsPane(GetBasicData())

    SearchPane = tk.Toplevel(bg=MainColor)
    SearchOptions = ["ISBN:", "Title:", "Subtitle:",
                     "Publication Date:", "Genre:", "Subgenre:", "Series:", "Edition:",
                     "Publisher:", "Format:", "Position in Series:", "Owner:", "Author Name:"]

    SearchLoc = [(1, 1), (2, 1), (3, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
                 (11, 1), (12, 1), (13, 1), (4, 1)]
    SearchEntriesWidths = [16, 32, 32, 6, 16, 16, 32, 4, 16, 6, 4, 16, 32]
    SearchEntries = LAE.LEBuild(SearchPane, SearchOptions, SearchLoc, BackgroundColor=MainColor,
                                EntryWidths=SearchEntriesWidths)

    SearchButton = tk.Button(SearchPane, text="Search!", command=BuildSearchCommand)
    SearchButton.grid(column=5)

    SQLSearchOptions = []
    for thing in SearchOptions:
        SQLSearchOptions.append(thing.replace(" ", "_").replace(":", ""))


def CleanupRoot():
    # Strips all geometry and added visuals from the root frame,
    # adds essential visual tools meant for every frame (ie menus)
    # pathing the way for more visauls without any clutter
    for widget in root.winfo_children():
        widget.destroy()
    BuildMenus()


def BuildMenus():
    # This function builds the Menu widget for the main window
    menubar = tk.Menu(root)
    SearchMenu = tk.Menu(menubar, tearoff=0)
    # SearchMenu.add_command(label = "Search by ISBN", command = Search)
    # SearchMenu.add_command(label = "Search by Title", command = quit)
    SearchMenu.add_command(label="Comprehensive Search", command=Search)

    TestMenu = tk.Menu(menubar, tearoff=0)
    TestMenu.add_command(label="Test Function", command=test)
    TestMenu.add_command(label="Reset Database", command=BDB.main)
    TestMenu.add_command(label="Poll Database", command=PDB.main)

    menubar.add_cascade(label="Search", menu=SearchMenu)
    menubar.add_command(label="Add", command=BuildAddPane)
    menubar.add_cascade(label="TEST", menu=TestMenu)
    menubar.add_command(label="QUIT", command=quit)
    root.config(menu=menubar)


def FullBookDisplay(isbn):
    ResultsPane = tk.Toplevel(bg=MainColor)

    TopLeft = tk.Frame(ResultsPane, bg=SecondaryColor)
    TopLeft.grid(row=0, column=0, padx=5, pady=5)

    BottomLeft = tk.Frame(ResultsPane, bg=SecondaryColor)
    BottomLeft.grid(row=1, column=0, padx=5, pady=5)

    TopRight = tk.Frame(ResultsPane, bg=SecondaryColor)
    TopRight.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

    b = Book(isbn)
    BookData, AuthorData = b.GetFullBookData()[:12], b.GetFullBookData()[12:]

    NumAuthors = len(AuthorData)

    Labels1 = ["Title:", "Subtitle:", "Series:", "Position in Series:", "Edition:"]
    Labels2 = ["Publisher:", "Publication Date:", "Format:", "ISBN:"]
    Labels3 = ["Author(s):", "Genre:", "Subgenre:", "Owner:"]

    Data1 = [BookData[1], BookData[2], BookData[6], BookData[7], BookData[11]]
    Data2 = [BookData[9], BookData[3], BookData[8], BookData[0]]
    Data3 = []
    for name in AuthorData:
        Data3.append(name)
    Data3.append(BookData[4]);
    Data3.append(BookData[5]);
    Data3.append(BookData[10])

    Label1Loc = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    Label2Loc = [(1, 1), (2, 1), (3, 1), (4, 1)]
    Label3Loc = [(1, 1), (NumAuthors + 1, 1), (NumAuthors + 2, 1), (NumAuthors + 3, 1)]

    Data1Loc = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]
    Data2Loc = [(1, 2), (2, 2), (3, 2), (4, 2)]
    Data3Loc = []
    for i in range(1, NumAuthors + 1):
        Data3Loc.append((i, 2))
    Data3Loc.append((NumAuthors + 1, 2));
    Data3Loc.append((NumAuthors + 2, 2));
    Data3Loc.append((NumAuthors + 3, 2))

    LAE.LabelBuild(TopLeft, Labels1, Label1Loc, BackgroundColor=SecondaryColor)
    LAE.LabelBuild(BottomLeft, Labels2, Label2Loc, BackgroundColor=SecondaryColor)
    LAE.LabelBuild(TopRight, Labels3, Label3Loc, BackgroundColor=SecondaryColor)

    LAE.LabelBuild(TopLeft, Data1, Data1Loc, BackgroundColor=SecondaryColor)
    LAE.LabelBuild(BottomLeft, Data2, Data2Loc, BackgroundColor=SecondaryColor)
    LAE.LabelBuild(TopRight, Data3, Data3Loc, BackgroundColor=SecondaryColor)


def GetBasicData(*ISBNList):
    if not ISBNList or len(ISBNList) == 0:
        GetBooks = '''SELECT ISBN FROM books ORDER BY Title'''
        cur.execute(GetBooks)
        ISBNList = cur.fetchall()

    booksData = []
    for isbn in ISBNList:
        b = Book(isbn[0])
        booksData.append(b.GetBasicData())

    return booksData


def Setup():
    # Builds the starting frames and Tkinter windows, in which all other functionality is built
    global root;
    root = tk.Tk()
    root.title("Alexandria")
    root.geometry("+0+0")


def BuildBasicResultsPane(records):
    # This function takes the records list as created by the
    # GetBasicData function, and generates the display that shows all that data
    CleanupRoot()

    DataFrame = tk.Frame(root, bg=SecondaryColor)
    DataFrame.grid(row=1, column=0)

    HeaderFrame = tk.Frame(root, bg="LightBlue")
    HeaderFrame.grid(row=0, column=0)

    LabelWidths = [13, 64, 16, 16, 16, 32, 2]
    DataLabels = ["ISBN", "Title", "Headline Author", "Publication Year", "Genre", "Series", ""]

    MoreButtons = []

    for i in range(len(DataLabels)):
        x = tk.Label(HeaderFrame, text=DataLabels[i], bg="LightBlue", width=LabelWidths[i])
        x.grid(row=0, column=i)

    for i in range(len(records)):

        CountOfBookData = len(records[i])

        if i % 2 == 0:
            color = SecondaryColor
        else:
            color = MainColor

        f = tk.Frame(DataFrame, bg=color)
        f.grid()
        for j in range(CountOfBookData):
            l = tk.Label(f, text=records[i][j], width=LabelWidths[j], bg=color)
            l.grid(row=i + 1, column=j)
        ISBNToPass = records[i][0]
        MoreButtons.append(tk.Button(f, text="...", command=lambda x=ISBNToPass: FullBookDisplay(x)))
        MoreButtons[i].grid(row=i + 1, column=CountOfBookData + 1)


def InsertBookData():
    # Method that gathers the data from the the Add A Book pane,
    # checks for duplicate data, and inserts it into the Alexandria database

    flag = InsertDataSanitationChecks(db, cur)
    if flag:
        print("Passed Sanitation Checks, Inserting (Not)")

        # AuthorsData will be in a repeating format of
        # (Author_First, Author_Middle, Author_Last, repeat those 3 for each author)
        AuthorData = LAE.EntriesToTuple(AuthorFields)

        # BookData will be in the format of
        # (Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
        # Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        BookData = LAE.EntriesToTuple(BookFields)
        for i in range(0, len(AuthorData), 3):
            # checks to see if the entered Author data is already in the database.
            first = AuthorData[i]
            if not first:
                first = "None"
            middle = AuthorData[i + 1]
            if not middle:
                middle = "None"
            last = AuthorData[i + 2]
            if not last:
                last = "None"
            cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                    Author_Middle IS %r AND
                    Author_Last IS %r''' % (first, middle, last)

            cur.execute(cmd)
            AuthorID = cur.fetchall()
            # this if statement will execute if the author name set is not already in
            # the database
            if not AuthorID:
                print("That author isnt in the database!")
                cmd = ''' INSERT INTO Authors(Author_First, Author_Middle, Author_Last)
                    VALUES(%r, %r, %r)''' % (first, middle, last)
                cur.execute(cmd)
                cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                        Author_Middle IS %r AND
                        Author_Last IS %r''' % (first, middle, last)

                cur.execute(cmd)
                AuthorID = cur.fetchall()
            cmd = '''INSERT INTO BookToAuthors (Author_ID, ISBN) VALUES
            (%r, %r)''' % (AuthorID[0][0], BookData[2])
            cur.execute(cmd)
            # (Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
            # Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        cmd = '''INSERT INTO Books (Title, Subtitle, ISBN, Series, Position_in_Series,
                Genre, Subgenre, Publication_Date, Publisher, Format, Owner) VALUES
                %s ''' % (BookData,)
        cur.execute(cmd)
        db.commit()

    else:
        print("Problems with data, double check data")


def InsertDataSanitationChecks():
    ErrorText.config(text="")

    title = BookFields[0].get()
    isbn = int(BookFields[2].get())

    if not isbn or len(title) == 0:
        ErrorText.config(text="You need at least a title and ISBN to add a book")
        return False

    cmd = "SELECT Title FROM Books WHERE ISBN = %d" % isbn
    cur.execute(cmd)

    if cur.fetchall():
        ErrorText.config(text="Cannot add repeat ISBN Numbers.")
        return False

    if len(isbn) is not 13 and len(isbn) is not 10:
        ErrorText.config(text="ISBN needs to be either 10 or 13 characters long")
        return False

    return True


def BuildAddPane():
    # A method that takes the add_fields Entries, gets the text from them,
    # and inputs them into a String that represents an SQL command that will
    # input that data into Alexandria.db database, books table

    CleanupRoot()

    global NumAuthors;
    NumAuthors = 1
    global AuthorFields;
    AuthorFields = []
    global BookFields
    global ErrorText

    def MoreAuthors():
        global NumAuthors;
        global AuthorFields
        AuthLabels = ["Author, First: ", "Middle: ", "Last: "]
        AuthLocations = [(NumAuthors + 1, 1), (NumAuthors + 1, 2), (NumAuthors + 1, 3)]
        AuthorFields += LAE.LEBuild(AuthorFrame, AuthLabels, AuthLocations, BackgroundColor="thistle")
        NumAuthors += 1

    def BuildMainMenu():
        BuildBasicResultsPane(GetBasicData())

    master = tk.Frame(root, bg=SecondaryColor)
    master.grid()

    ButtonFrame = tk.Frame(master, bg=SecondaryColor)
    ButtonFrame.grid(row=0, column=0)

    DataFrame = tk.Frame(master, bg=SecondaryColor)
    DataFrame.grid(row=0, column=1)

    RightFrame = tk.Frame(master, bg=SecondaryColor)
    RightFrame.grid(row=0, column=2)

    AuthorFrame = tk.Frame(RightFrame, bg=SecondaryColor)
    AuthorFrame.grid(row=1, column=0)

    AuthorButtonFrame = tk.Frame(RightFrame, bg=SecondaryColor)
    AuthorButtonFrame.grid(row=0, column=0)

    BackButtton = tk.Button(ButtonFrame, text="Back", command=BuildMainMenu)
    BackButtton.grid(row=1, column=0)

    InsertButton = tk.Button(ButtonFrame, text="Add Book!", padx=10, pady=10, command=InsertBookData)
    InsertButton.grid(row=2, column=0, pady=20)

    MoreAuthorsButton = tk.Button(AuthorButtonFrame, text="Another Author", command=MoreAuthors,
                                  padx=10, pady=10)
    MoreAuthorsButton.grid(row=0, column=1)

    x = tk.Label(ButtonFrame, text="ADD A BOOK TO THE LIBRARY", bg="LightBlue")
    x.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)

    BookLabelTexts = ["Title: ", "Subtitle: ", "ISBN: ", "Series: ", "Series #: ",
                      "Genre: ", "Subgenre: ", "Publication Year: ", "Publisher: "]
    BookLabelLocations = [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (5, 1), (5, 2), (7, 1), (7, 2), (7, 3)]

    BookFields = LAE.LEBuild(DataFrame, BookLabelTexts, BookLabelLocations, BackgroundColor="thistle")
    x = tk.Label(DataFrame, text="Format: ", bg="thistle")
    x.grid(row=7, column=5)

    FormatOption = tk.StringVar(DataFrame);
    FormatOption.set("Mass Market PB")
    t = tk.OptionMenu(DataFrame, FormatOption, "Mass Market PB", "Trade PB", "Hard Back")
    t.grid(row=7, column=6)
    BookFields.append(FormatOption)

    x = tk.Label(DataFrame, text="Owner: ", bg="thistle")
    x.grid(row=9, column=1)

    OwnerOption = tk.StringVar(DataFrame);
    OwnerOption.set("Patrick & Shelby")
    t = tk.OptionMenu(DataFrame, OwnerOption, "Patrick & Shelby", "John & Kathy")
    t.grid(row=9, column=2)
    BookFields.append(OwnerOption)

    ErrorText = tk.Label(DataFrame, text="", bg=SecondaryColor, fg="red", font="bold")
    ErrorText.grid(row=10, column=1, columnspan=5)

    MoreAuthors()


def main():
    Setup()
    BuildBasicResultsPane(GetBasicData())
    global db;
    global cur;
    global MainColor;
    global SecondaryColor

    root.mainloop()


if __name__ == '__main__':
    db, cur = create_connection()
    MainColor = "khaki1";
    SecondaryColor = "LightGoldenrod2"
    main()
