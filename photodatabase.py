import sqlite3
from sqlite3 import Error

#SQLITE studio is useful for checking the database
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def Createdatabase():
    database = r"C:\sqlite\db\photodata.db" #must create C:\sqlite\db\  folders first 


    #we are using a many to many strategy
    sql_create_photos_table = """ CREATE TABLE IF NOT EXISTS photos (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        filelocation text NOT NULL,
                                        quality float
                                    ); """
    
    sql_create_reference_table = """ CREATE TABLE IF NOT EXISTS reference (
                                        refid integer PRIMARY KEY,
                                        photoid integer NOT NULL,
                                        tagid integer NOT NULL,
                                        FOREIGN KEY (photoid) REFERENCES photos (id),
                                        FOREIGN KEY (tagid) REFERENCES tags (id)
                                    ); """

    sql_create_tags_table = """CREATE TABLE IF NOT EXISTS tags (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    tagname text NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_photos_table)
        create_table(conn, sql_create_reference_table)
        create_table(conn, sql_create_tags_table)
    else:
        print("Error! cannot create the database connection.")


def createphoto(conn, task):
    sql = ''' INSERT INTO photos(filelocation) VALUES(?)''' #add quality when implemented

    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid


def insertphoto(photolocation): #add tags later
    database = r"C:\sqlite\db\photodata.db"
    conn = create_connection(database)
    photo= ([photolocation])#add quality after location when implemented
    #tags add here
    createphoto(conn, photo)


#def outputquery(tags):

#def outputall():

if __name__ == '__main__': #testing
    Createdatabase()
    test = 'test'
    insertphoto(test)
