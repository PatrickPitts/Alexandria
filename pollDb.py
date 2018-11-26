import sqlite3 as sq

def create_connection(database):
    conn = sq.connect(database)
    return conn

db = "Alexandria.db"
y = create_connection(db)
cur = y.cursor()

settings = {"tableLength":9999,
            "columnWidth":13}

def showSettings():
    for thing in settings:
        print thing

class getHeaders():
    x = []
    def __init__(self, c, table):
        self.x = []
        get = "PRAGMA table_info(%s);" % table

        c.execute(get)

        for thing in c.fetchall():
            self.x.append(thing[1])

    def display(self):
        print "\nfor table %s:\n\n" % table
        for item in self.x:
            print "%s" % thing
        print "\n"

    def get(self):
        return self.x

class getTables():
    x = []
    def __init__(self, c):
        self.x = []
        get = "SELECT name FROM sqlite_master WHERE type='table';"
        c.execute(get)

        for thing in c.fetchall():
            self.x.append(thing[0])

    def display(self):
        print "\n"
        for item in self.x:
            print "%s" % item
        print "\n"

    def get(self):
        return self.x

def showHeaders(c, arr=[]):
    if len(arr) == 0:
        tables = getTables(c).get()
        for table in tables:
            print "\nThe fields in %s are:\n" % table
            for thing in getHeaders(c, table):
                print thing
            print "__________________"
        return
    else:
        for table in arr:
            print "\nThe fields in %s are:\n" % table
            for thing in getHeaders(c, table):
                print thing
            print "__________________"
        return

def displayTable(c, table, maxNumRows = settings["tableLength"]):
    colWidth = settings["columnWidth"]

    get = "SELECT * FROM %s" % table
    c.execute(get)
    data = c.fetchall()


    headers = getHeaders(c,table).get()

    print "\nShowing data from %s: \n" % table
    top = "    |"
    for header in headers:
        toAdd = header
        if len(toAdd) > colWidth:
            toAdd = toAdd[:colWidth-1]+"-"
        else:
            while len(toAdd) < colWidth:
                toAdd += " "
        top += toAdd + "|"
    print top
    print "-"*((colWidth+1)*len(headers)+5)

    maxLen = len(data)
    if maxLen > maxNumRows:
        maxLen = maxNumRows


    for i in range(maxLen):
        record = data[i]
        txt = str(i+1)
        while len(txt)<4:
            txt += ' '
        txt += "|"
        for entry in record:
            add = "%s" % str(entry)

            if len(add) > colWidth:
                add = add[:colWidth-1]+"-"
            else:
                while len(add) < colWidth:
                    add += " "

            txt += add + "|"

        print txt

def engine(cur):
    print "\nWhat would you like to do?"
    command = raw_input(">>>")

    if "get tables" in command.lower():
        getTables(cur).display()

    elif "quit" in command:
        y.close()
        quit()

    elif "display" in command.lower():
        tables = getTables(cur).get()

        print "\nwhich table of the following would you like to display?"
        getTables(cur).display()
        print "or print 'all'!\n"
        command = raw_input(">>>")
        if command in tables:
            displayTable(cur, command)
        elif command in 'all':
            for table in tables:
                displayTable(cur, table)
        else:
            print "I didn't get that. Back to main menu.\n"

    elif "test" in command.lower():
        displayTable(cur,"Books")
    else:
        print "That's not a valid command!"

def main():

    while True:
        engine(cur)
    y.close()


if __name__ == "__main__":
    main()
