import sqlite3 as sq

def create_connection():
    db = sq.connect("TestDatabase.db")
    return db, db.cursor()

def close_connection(db):
    db.commit()
    db.close()

def MakeTable():
    db, cur = create_connection()
    cmd = '''CREATE TABLE Table1(
    A_String text,
    A_Number integer PRIMARY KEY)'''
    cur.execute(cmd)
    close_connection(db)

def InsertData():
    db, cur = create_connection()
    sql1 = '''INSERT INTO Table1(A_String, A_Number) VALUES
    ("TheQuickBrownFox", 1)'''
    sql2 = '''INSERT INTO Table1(A_String, A_Number) VALUES
    ("FooBar",2)'''
    sql3 = '''INSERT INTO Table1(A_String, A_Number) VALUES
    ("FooBar",3)'''
    sql4 = '''INSERT INTO Table1(A_String, A_Number) VALUES
    ("FooBar",4)'''
    cur.execute(sql3)
    cur.execute(sql4)
    close_connection(db)

def PollDatabase():
    db, cur = create_connection()
    cmd = '''SELECT a_Number from Table1 WHERE A_String IS "FooBar" AND
            A_Number IS 3'''
    cur.execute(cmd)
    print(cur.fetchall())
    close_connection(db)

def main():
    #InsertData()
    PollDatabase()
    #MakeTable()

if __name__ == "__main__":
    main()
