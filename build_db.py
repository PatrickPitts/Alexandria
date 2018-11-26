import sqlite3 as sq

def create_connection(database):
    conn = sq.connect(database)
    return conn

def insert_table(conn):
    sql1 = ''' CREATE TABLE Books(
    ISBN integer PRIMARY KEY,
    Title text NOT NULL,
    Subtitle text DEFAULT NULL,
    Publication_Date date,
    Genre text,
    Subgenre text DEFAULT NULL,
    Series text,
    Edition integer,
    Position_in_Series integer DEFAULT NULL,
    Format text,
    Publisher text,
    Owner text)'''

    sql2 = ''' CREATE TABLE Authors(
    Author_ID integer PRIMARY KEY,
    Author_Last text,
    Author_First text,
    Author_Middle text)'''

    sql3 = ''' CREATE TABLE BookToAuthors(
    ISBN integer,
    Author_ID integer,
    FOREIGN KEY(ISBN) REFERENCES books(ISBN),
    FOREIGN KEY(Author_ID) REFERENCES authors(Author_ID))'''

    c = conn.cursor()
    c.execute(sql1)
    c.execute(sql2)
    c.execute(sql3)
    conn.commit()

def insert_data(conn):
    insert1 = '''INSERT INTO books(ISBN, Title, Publication_Date, Genre,
                    Subgenre, Series, Format, Publisher, Owner)
        VALUES (9781481451949,"Imposter Syndrome",2018-01-01,
            "Science Fiction", "Suspense", "The Arcadia Project","TPB","Saga Press","P&S")'''

    insert2 = '''INSERT INTO books(ISBN, Title, Publication_Date, Genre,
                    Series, Format, Publisher, Owner)
        VALUES (9781619635180,"A Court of Thorns and Roses",
                2016-05-01,"Fantasy","A Court of Thorns and Roses","TPB","Bloomsbury","P&S")'''

    insert3 = '''INSERT INTO books(ISBN, Title, Subtitle, Publication_Date,
                                Genre, Subgenre, Format, Publisher, Owner, Edition)
        VALUES (9781593275679,"How Linux Works","What Every Superuser Should Know",
                2015-01-01,"Computer Science","Linux","TPB","No Starch Press","P&S",2)'''

    aut1 = '''INSERT INTO authors(Author_ID, Author_First, Author_Last)
        VALUES (1,"Mishell","Baker")'''

    aut2 = '''INSERT INTO authors(Author_ID, Author_First, Author_Middle, Author_Last)
        VALUES (2,"Sarah", "J.","Maas")'''

    aut3 = '''INSERT INTO authors(Author_ID, Author_First, Author_Last)
        VALUES (3,"Brian","Ward")'''

    b2a1 = '''INSERT INTO BookToAuthors(ISBN, Author_ID)
        VALUES (9781481451949,1)'''

    b2a2 = '''INSERT INTO BookToAuthors(ISBN, Author_ID)
        VALUES (9781619635180,2)'''

    b2a3 = '''INSERT INTO BookToAuthors(ISBN, Author_ID)
    VALUES (9781593275679,3)'''

    c = conn.cursor()
    c.execute(insert1)
    c.execute(insert2)
    c.execute(insert3)
    c.execute(aut1)
    c.execute(aut2)
    c.execute(aut3)
    c.execute(b2a1)
    c.execute(b2a2)
    c.execute(b2a3)
    conn.commit()

def purge(conn):
    cur = conn.cursor()
    get = '''SELECT name FROM sqlite_master WHERE type='table';'''
    cur.execute(get)
    tables = cur.fetchall()
    for table in tables:
        drop = '''DROP TABLE %s'''% table
        cur.execute(drop)

def main():
    db = "Alexandria.db"
    x = create_connection(db)
    print("Deleting Current file Alexandria.db")
    purge(x)
    print("Creating new file Alexandria.db")
    insert_table(x)
    insert_data(x)
    x.close()
    print("File creation complete")


if __name__ == "__main__":
    main()
