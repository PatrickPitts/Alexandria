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
        self.basic_book_info = []
        self.full_book_info = []

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
        # Series 6, Pos. in Series 7, Book Format 8, Publisher 9, Owner 10, Edition 11,
        # Author First 12, Author Middle 13, Author Last 14]
        # self.DataResults will  be a tuple containing a list this information from the database in this order.
        # If there is more than one Author, DataResults will contain multiple lists, each of which will have different
        # author name data, but otherwise will contain the same information

        self.book_data = {
            "ISBN": self.DataResults[0][0],
            "Title": self.DataResults[0][1],
            "Subtitle": self.DataResults[0][2],
            "Publication Year": self.DataResults[0][3],
            "Genre": self.DataResults[0][4],
            "Subgenre": self.DataResults[0][5],
            "Series": self.DataResults[0][6],
            "Position in Series": self.DataResults[0][7],
            "Format": self.DataResults[0][8],
            "Publisher": self.DataResults[0][9],
            "Owner": self.DataResults[0][10],
            "Edition": self.DataResults[0][11]
        }

        for i in range(len(self.DataResults)):

            ins = "Author %d" % (i+1)

            name = ""
            for item in self.DataResults[i][12:15]:
                if item != u'None':
                    name += item + " "

            self.book_data[ins] = name

    def get_basic_data(self):

        for item in basic_data:
            if item == "Headline Author":
                item = "Author 1"
            self.basic_book_info.append(self.book_data[item])

        return self.basic_book_info

    def get_full_book_data(self):

        self.full_book_info = []

        for key in self.book_data:
            self.full_book_info.append(self.book_data[key])

        return self.full_book_info

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

    def get_title(self):
        return self.book_data["Title"]


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
    menu_bar.add_command(label="Add", command=build_add_pane)
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


def confirm_delete(b):

    def delete_and_close():
        b.delete_book_data()
        db.commit()
        confirm.destroy()
        build_basic_results_pane(get_basic_data())

    confirm = tk.Toplevel(bg=MainColor)

    txt = "Are you sure you want to delete %s from your collection?" % b.get_title()
    msg = tk.Label(confirm, text=txt, bg=MainColor)
    msg.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    delete_button = tk.Button(confirm, text="Delete", command=delete_and_close)
    delete_button.grid(row=1, column=0, padx=10, pady=10)

    cancel_button = tk.Button(confirm, text="Cancel", command=confirm.destroy)
    cancel_button.grid(row=1, column=1, padx=10, pady=10)


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
            msg = tk.Label(f, text=records[i][j], width=label_widths[j], bg=color)
            msg.grid(row=i + 1, column=j)

        isbn_to_pass = records[i][0]

        more_buttons.append(tk.Button(f, text="More...", width=6,
                                      command=lambda q=isbn_to_pass: full_book_display(q)))
        more_buttons[i].grid(row=i + 1, column=count_of_book_data + 1, padx=10)

        delete_buttons.append(tk.Button(f, text="Delete...", width=9,
                                        command=lambda b=Book(isbn_to_pass): confirm_delete(b)))
        delete_buttons[i].grid(row=i + 1, column=count_of_book_data + 2, padx=10)


def insert_book_data():
    # Method that gathers the data from the the Add A Book pane,
    # checks for duplicate data, and inserts it into the Alexandria database

    flag = insert_data_sanitation_checks()
    if flag:
        print("Passed Sanitation Checks, Inserting (Not)")

        # AuthorsData will be in a repeating format of
        # (Author_First, Author_Middle, Author_Last, repeat those 3 for each author)
        author_data = LaE.EntriesToTuple(AuthorFields)

        # book_data will be in the format of
        # (Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
        # Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        book_data = LaE.EntriesToTuple(BookFields)
        for i in range(0, len(author_data), 3):
            # checks to see if the entered Author data is already in the database.
            first = author_data[i]
            if not first:
                first = "None"
            middle = author_data[i + 1]
            if not middle:
                middle = "None"
            last = author_data[i + 2]
            if not last:
                last = "None"
            cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                    Author_Middle IS %r AND
                    Author_Last IS %r''' % (first, middle, last)

            cur.execute(cmd)
            author_id = cur.fetchall()
            # this if statement will execute if the author name set is not already in
            # the database
            if not author_id:
                print("That author isnt in the database!")
                cmd = ''' INSERT INTO Authors(Author_First, Author_Middle, Author_Last)
                    VALUES(%r, %r, %r)''' % (first, middle, last)
                cur.execute(cmd)
                cmd = '''SELECT Author_ID FROM Authors WHERE Author_First IS %r AND
                        Author_Middle IS %r AND
                        Author_Last IS %r''' % (first, middle, last)

                cur.execute(cmd)
                author_id = cur.fetchall()
            cmd = f'''INSERT INTO BookToAuthors (Author_ID, ISBN) VALUES
            ({author_id[0][0]!r}, {book_data[2]!r})'''
            cur.execute(cmd)
            # (Title, Subtitle, ISBN Number, Series Name, Position in Series, Genre,
            # Subgenre, Publication Year, Publisher, Book Format, Book Owner)
        cmd = '''INSERT INTO Books (Title, Subtitle, ISBN, Series, Position_in_Series,
                Genre, Subgenre, Publication_Date, Publisher, Format, Owner) VALUES
                %s ''' % (book_data,)
        cur.execute(cmd)
        db.commit()

    else:
        print("Problems with data, double check data")


def insert_data_sanitation_checks():
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


def build_add_pane():
    # A method that takes the add_fields Entries, gets the text from them,
    # and inputs them into a String that represents an SQL command that will
    # input that data into Alexandria.db database, books table

    cleanup_root()

    global NumAuthors
    NumAuthors = 1
    global AuthorFields
    AuthorFields = []
    global BookFields
    global ErrorText

    def more_authors():
        global NumAuthors
        global AuthorFields
        auth_labels = ["Author, First: ", "Middle: ", "Last: "]
        auth_locations = [(NumAuthors + 1, 1), (NumAuthors + 1, 2), (NumAuthors + 1, 3)]
        AuthorFields += LaE.LEBuild(author_frame, auth_labels, auth_locations, BackgroundColor="thistle")
        NumAuthors += 1

    def build_main_menu():
        build_basic_results_pane(get_basic_data())

    master = tk.Frame(root, bg=SecondaryColor)
    master.grid()

    button_frame = tk.Frame(master, bg=SecondaryColor)
    button_frame.grid(row=0, column=0)

    data_frame = tk.Frame(master, bg=SecondaryColor)
    data_frame.grid(row=0, column=1)

    right_frame = tk.Frame(master, bg=SecondaryColor)
    right_frame.grid(row=0, column=2)

    author_frame = tk.Frame(right_frame, bg=SecondaryColor)
    author_frame.grid(row=1, column=0)

    author_button_frame = tk.Frame(right_frame, bg=SecondaryColor)
    author_button_frame.grid(row=0, column=0)

    back_button = tk.Button(button_frame, text="Back", command=build_main_menu)
    back_button.grid(row=1, column=0)

    insert_button = tk.Button(button_frame, text="Add Book!", padx=10, pady=10, command=insert_book_data)
    insert_button.grid(row=2, column=0, pady=20)

    more_authors_button = tk.Button(author_button_frame, text="Another Author", command=more_authors,
                                    padx=10, pady=10)
    more_authors_button.grid(row=0, column=1)

    x = tk.Label(button_frame, text="ADD A BOOK TO THE LIBRARY", bg="LightBlue")
    x.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10)

    book_label_texts = ["Title: ", "Subtitle: ", "ISBN: ", "Series: ", "Series #: ",
                        "Genre: ", "Subgenre: ", "Publication Year: ", "Publisher: "]
    book_label_locations = [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (5, 1), (5, 2), (7, 1), (7, 2), (7, 3)]

    BookFields = LaE.LEBuild(data_frame, book_label_texts, book_label_locations, BackgroundColor="thistle")
    x = tk.Label(data_frame, text="Format: ", bg="thistle")
    x.grid(row=7, column=5)

    format_option = tk.StringVar(data_frame)
    format_option.set("Mass Market PB")
    t = tk.OptionMenu(data_frame, format_option, "Mass Market PB", "Trade PB", "Hard Back")
    t.grid(row=7, column=6)
    BookFields.append(format_option)

    x = tk.Label(data_frame, text="Owner: ", bg="thistle")
    x.grid(row=9, column=1)

    owner_option = tk.StringVar(data_frame)
    owner_option.set("Patrick & Shelby")
    t = tk.OptionMenu(data_frame, owner_option, "Patrick & Shelby", "John & Kathy")
    t.grid(row=9, column=2)
    BookFields.append(owner_option)

    ErrorText = tk.Label(data_frame, text="", bg=SecondaryColor, fg="red", font="bold")
    ErrorText.grid(row=10, column=1, columnspan=5)

    more_authors()


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
