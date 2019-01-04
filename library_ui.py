import tkinter as tk
import sqlite3 as sq
import LabelsAndEntries as LaE

import pollDb as Pdb
import build_db as bdb


class Book:
    # an object that represents a book, to be worked with programmatically.
    # typically, a Book object is created to collect and aggregate relevant data
    # on a book identified by it's ISBN number. That data is then pulled from the Book
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

        self.book_data = {
            "ISBN": self.DataResults[0][0],
            "Title": self.DataResults[0][1],
            "Subtitle": self.DataResults[0][2],
            "Publication Date": self.DataResults[0][3],
            "Genre": self.DataResults[0][4],
            "Subgenre": self.DataResults[0][5],
            "Series": self.DataResults[0][6],
            "Position in Series": self.DataResults[0][7],
            "Format": self.DataResults[0][8],
            "Publisher": self.DataResults[0][9],
            "Owner": self.DataResults[0][10],
            "Edition": self.DataResults[0][11]
        }

        # [ISBN 0, Title 1, Subtitle 2, Pub Date 3, Genre 4, Subgenre 5,
        # Series 6, Pos. in Series 7, Book Format 8, Publisher 9, Owner 10, Edition 11]

        self.BookData = list(self.DataResults[0][:12])

        for i in range(len(self.DataResults)):

            ins_1 = "Author First %d" % (i+1)
            ins_2 = "Author Middle %d" % (i+1)
            ins_3 = "Author Last %d" % (i+1)

            self.book_data[ins_1] = self.DataResults[i][12]
            self.book_data[ins_2] = self.DataResults[i][13]
            self.book_data[ins_3] = self.DataResults[i][14]

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

    def get_basic_data(self):
        return self.BasicInfo

    def get_full_book_data(self):
        return self.FullBookInfo

    def delete_book_data(self):
        cmd = "DELETE FROM Books WHERE ISBN is %d" % self.isbn
        cur.execute(cmd)

        cmd = "SELECT Author_ID from BookToAuthors WHERE ISBN is %d" % self.isbn
        cur.execute(cmd)
        auth_id = cur.fetchone()[0]

        cmd = "DELETE FROM BookToAuthors WHERE ISBN IS %d" % self.isbn
        cur.execute(cmd)

        cmd = "SELECT ISBN FROM BookToAuthors where Author_ID IS %d" % auth_id
        cur.execute(cmd)

        if not cur.fetchall():
            cmd = "DELETE FROM Authors WHERE Author_ID is %d" % auth_id
            cur.execute(cmd)
        db.commit()


def test():
    # b = Book(1111111111111)

    pass


def create_connection():
    # A function that generates a connection to the Alexandria.db database,
    # which stores the book data for the library. Returns a connection object to the
    # database itself, which is required to shut down the connection later, and
    # a cursor object which is required to interact with the database.

    d = sq.connect("Alexandria.db")
    return d, d.cursor()


def close_connection(d):
    # A function that takes a connection object, commits any changes to the
    # connected database, then closes the connection.

    d.commit()
    d.close()


def search():

    def build_search_command():

        # The rest of the code in the Execute Search function relies on this
        # select command returning these exact parameters, in this order. If changes
        # are to be made to this SQL Command, then many other changes in this
        # function will need to be made as well.
        cmd = '''SELECT Books.ISBN FROM BookToAuthors
                INNER JOIN Authors ON
                    Authors.Author_ID = BookToAuthors.Author_ID
                INNER JOIN BOOKS ON
                    Books.ISBN = BookToAuthors.ISBN WHERE '''

        for i in range(len(search_entries) - 1):
            search_values = search_entries[i].get()
            if search_values:
                try:
                    search_values = int(search_values)
                    cmd += "Books.%s IS %d AND " % (sql_search_options[i], search_values)

                except ValueError:

                    cmd += "Books.%s IS %r AND " % (sql_search_options[i], search_values)

        author_name = search_entries[-1].get()
        author_name_list = author_name.split()
        # AuthorTableColumns = ["Author_First", "Author_Middle", "Author_Last"]

        for name in author_name_list:
            cmd += '''(Authors.Author_First IS %r
                OR Authors.Author_Middle IS %r
                OR Authors.Author_Last IS %r) OR  ''' % (name, name, name)

        results = []
        try:
            for row in cur.execute(cmd[:-5]):
                results.append(row[0])
            if 0 < len(results):
                results = list(set(results))
                build_basic_results_pane(get_basic_data(results))
            else:
                build_basic_results_pane(get_basic_data())
        except sq.OperationalError:
            build_basic_results_pane(get_basic_data())

    search_pane = tk.Toplevel(bg=MainColor)
    search_options = ["ISBN:", "Title:", "Subtitle:",
                      "Publication Date:", "Genre:", "Subgenre:", "Series:", "Edition:",
                      "Publisher:", "Format:", "Position in Series:", "Owner:", "Author Name:"]

    search_loc = [(1, 1), (2, 1), (3, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
                  (11, 1), (12, 1), (13, 1), (4, 1)]
    search_entries_widths = [16, 32, 32, 6, 16, 16, 32, 4, 16, 6, 4, 16, 32]
    search_entries = LaE.LEBuild(search_pane, search_options, search_loc, BackgroundColor=MainColor,
                                 EntryWidths=search_entries_widths)

    search_button = tk.Button(search_pane, text="Search!", command=build_search_command)
    search_button.grid(column=5)

    sql_search_options = []
    for thing in search_options:
        sql_search_options.append(thing.replace(" ", "_").replace(":", ""))


def cleanup_root():
    # Strips all geometry and added visuals from the root frame,
    # adds essential visual tools meant for every frame (ie menus)
    # making way for more visuals without any clutter
    for widget in root.winfo_children():
        widget.destroy()
    build_menus()


def build_menus():
    # This function builds the Menu widget for the main window
    menu_bar = tk.Menu(root)

    search_menu = tk.Menu(menu_bar, tearoff=0)
    search_menu.add_command(label="Comprehensive Search", command=search)

    test_menu = tk.Menu(menu_bar, tearoff=0)
    test_menu.add_command(label="Test Function", command=test)
    test_menu.add_command(label="Reset Database", command=bdb.main)
    test_menu.add_command(label="Poll Database", command=Pdb.main)

    menu_bar.add_cascade(label="Search", menu=search_menu)
    menu_bar.add_command(label="Add", command=BuildAddPane)
    menu_bar.add_cascade(label="TEST", menu=test_menu)
    menu_bar.add_command(label="QUIT", command=quit)
    root.config(menu=menu_bar)


def full_book_display(isbn):
    results_pane = tk.Toplevel(bg=MainColor)

    top_left = tk.Frame(results_pane, bg=SecondaryColor)
    top_left.grid(row=0, column=0, padx=5, pady=5)

    bottom_left = tk.Frame(results_pane, bg=SecondaryColor)
    bottom_left.grid(row=1, column=0, padx=5, pady=5)

    top_right = tk.Frame(results_pane, bg=SecondaryColor)
    top_right.grid(row=0, column=1, columnspan=3, padx=5, pady=5)

    b = Book(isbn)
    book_data, author_data = b.get_full_book_data()[:12], b.get_full_book_data()[12:]

    num_authors = len(author_data)

    labels1 = ["Title:", "Subtitle:", "Series:", "Position in Series:", "Edition:"]
    labels2 = ["Publisher:", "Publication Date:", "Format:", "ISBN:"]
    labels3 = ["Author(s):", "Genre:", "Subgenre:", "Owner:"]

    data1 = [book_data[1], book_data[2], book_data[6], book_data[7], book_data[11]]
    data2 = [book_data[9], book_data[3], book_data[8], book_data[0]]
    data3 = []
    for name in author_data:
        data3.append(name)
    data3.append(book_data[4])
    data3.append(book_data[5])
    data3.append(book_data[10])

    label1_loc = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    label2_loc = [(1, 1), (2, 1), (3, 1), (4, 1)]
    label3_loc = [(1, 1), (num_authors + 1, 1), (num_authors + 2, 1), (num_authors + 3, 1)]

    data1_loc = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]
    data2_loc = [(1, 2), (2, 2), (3, 2), (4, 2)]
    data3_loc = []

    for i in range(1, num_authors + 1):
        data3_loc.append((i, 2))
    data3_loc.append((num_authors + 1, 2))
    data3_loc.append((num_authors + 2, 2))
    data3_loc.append((num_authors + 3, 2))

    LaE.LabelBuild(top_left, labels1, label1_loc, BackgroundColor=SecondaryColor)
    LaE.LabelBuild(bottom_left, labels2, label2_loc, BackgroundColor=SecondaryColor)
    LaE.LabelBuild(top_right, labels3, label3_loc, BackgroundColor=SecondaryColor)

    LaE.LabelBuild(top_left, data1, data1_loc, BackgroundColor=SecondaryColor)
    LaE.LabelBuild(bottom_left, data2, data2_loc, BackgroundColor=SecondaryColor)
    LaE.LabelBuild(top_right, data3, data3_loc, BackgroundColor=SecondaryColor)


def get_basic_data(*results):
    isbn_list = []
    if not results or len(results) == 0:
        cmd = '''SELECT ISBN FROM books ORDER BY Title'''
        for row in cur.execute(cmd):
            isbn_list.append(row[0])
    else:
        for row in results[0]:
            isbn_list.append(row)

    books_data = []
    for num in isbn_list:
        b = Book(num)
        books_data.append(b.get_basic_data())

    return books_data


def setup():
    # Builds the starting frames and Tkinter windows, in which all other functionality is built
    global root
    root = tk.Tk()
    root.title("Alexandria")
    root.geometry("+0+0")


def build_basic_results_pane(records):
    # This function takes the records list as created by the
    # GetBasicData function, and generates the display that shows all that data
    cleanup_root()

    data_frame = tk.Frame(root, bg=SecondaryColor)
    data_frame.grid(row=1, column=0)

    header_frame = tk.Frame(root, bg="LightBlue")
    header_frame.grid(row=0, column=0)

    label_widths = [13, 64, 16, 16, 16, 32, 6]

    more_buttons = []
    delete_buttons = []

    for i in range(len(basic_data)):
        x = tk.Label(header_frame, text=basic_data[i], bg="LightBlue", width=label_widths[i])
        x.grid(row=0, column=i)

    # this extra header added to the header acts as a spacer to account for the extra width of each result frame,
    # ensuring that the header frame has Light Blue all the way across the frame, above the buttons of the
    # results.
    x = tk.Label(header_frame, text="", bg="LightBlue", width=25)
    x.grid(row=0, column=len(basic_data)+1, columnspan=2)

    for i in range(len(records)):

        count_of_book_data = len(records[i])

        if i % 2 == 0:
            color = SecondaryColor
        else:
            color = MainColor

        f = tk.Frame(data_frame, bg=color, height=3)
        f.grid()
        for j in range(count_of_book_data):
            l = tk.Label(f, text=records[i][j], width=label_widths[j], bg=color)
            l.grid(row=i + 1, column=j)

        isbn_to_pass = records[i][0]

        more_buttons.append(tk.Button(f, text="More...", width=6,
                                      command=lambda q=isbn_to_pass: full_book_display(q)))
        more_buttons[i].grid(row=i + 1, column=count_of_book_data + 1, padx=10)

        delete_buttons.append(tk.Button(f, text="Delete...", width=9,
                                        command=lambda b=Book(isbn_to_pass): b.delete_book_data()))
        delete_buttons[i].grid(row=i + 1, column=count_of_book_data + 2, padx=10)


def InsertBookData():
    # Method that gathers the data from the the Add A Book pane,
    # checks for duplicate data, and inserts it into the Alexandria database

    flag = InsertDataSanitationChecks()
    if flag:
        print("Passed Sanitation Checks, Inserting (Not)")

        # AuthorsData will be in a repeating format of
        # (Author_First, Author_Middle, Author_Last, repeat those 3 for each author)
        AuthorData = LaE.EntriesToTuple(AuthorFields)

        # BookData will be in the format of
        # (Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
        # Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        BookData = LaE.EntriesToTuple(BookFields)
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

    if len(str(isbn)) is not 13 and len(str(isbn)) is not 10:
        ErrorText.config(text="ISBN needs to be either 10 or 13 characters long")
        return False

    return True


def BuildAddPane():
    # A method that takes the add_fields Entries, gets the text from them,
    # and inputs them into a String that represents an SQL command that will
    # input that data into Alexandria.db database, books table

    cleanup_root()

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
        AuthorFields += LaE.LEBuild(AuthorFrame, AuthLabels, AuthLocations, BackgroundColor="thistle")
        NumAuthors += 1

    def BuildMainMenu():
        build_basic_results_pane(get_basic_data())

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

    BookFields = LaE.LEBuild(DataFrame, BookLabelTexts, BookLabelLocations, BackgroundColor="thistle")
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
    setup()
    build_basic_results_pane(get_basic_data())
    global db
    global cur
    global MainColor
    global SecondaryColor
    global basic_data
    root.mainloop()


if __name__ == '__main__':
    db, cur = create_connection()
    MainColor = "khaki1"
    SecondaryColor = "LightGoldenrod2"
    basic_data = ["ISBN", "Title", "Headline Author", "Publication Year", "Genre", "Series"]
    main()
