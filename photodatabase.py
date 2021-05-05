import sqlite3
from sqlite3 import Error
import imquality.brisque as brisque
from PIL import Image
import os#for testing
#SQLITE studio is useful for checking the database
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
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
    database = r"photodata.db" #must create C:\sqlite\db\  folders first or change destination
    #database = r"C:\sqlite\db\photodata.db"


    #we are using a many to many realation strategy
    sql_create_photos_table = """ CREATE TABLE IF NOT EXISTS photos (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        filelocation text NOT NULL UNIQUE,
                                        quality float
                                    ); """
    
    sql_create_reference_table = """ CREATE TABLE IF NOT EXISTS reference (
                                        photoid integer NOT NULL,
                                        tagid integer NOT NULL,
                                        FOREIGN KEY (photoid) REFERENCES photos (id),
                                        FOREIGN KEY (tagid) REFERENCES tags (id),
                                        UNIQUE(photoid, tagid)
                                    ); """

    sql_create_tags_table = """CREATE TABLE IF NOT EXISTS tags (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    tagname text NOT NULL UNIQUE
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
    try:
        sql = ''' INSERT INTO photos(filelocation, quality) VALUES(?,?)'''

        print(task)
        img = Image.open(task)
        quality = brisque.score(img)
        print(quality)
        phototask = (task, abs(quality))
        cur = conn.cursor()
        cur.execute(sql, phototask)
        conn.commit()

        return cur.lastrowid
    except:
        sql = ''' SELECT id FROM photos WHERE filelocation=?'''


        cur = conn.cursor()
        cur.execute(sql, (task,))
        conn.commit()

        return cur.fetchone()[0]


def createtags(conn, task):
    try:
        sql = ''' INSERT INTO tags(tagname) VALUES(?)'''

        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()

        return cur.lastrowid
    
    except:
        sql = ''' SELECT id FROM tags WHERE tagname=?'''


        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()

        return cur.fetchone()[0]




def insertphoto(photolocation, tags): #add tags after photolocation
    database = r"photodata.db"    
    conn = create_connection(database)

    formatphoto= (photolocation)
    formattag= ([tags])

    photoid = createphoto(conn, formatphoto)
    tagid = createtags(conn, formattag)

    #reference table
    try:
        sql = ''' INSERT INTO reference(photoid, tagid) VALUES(?,?)'''
        task = (photoid, tagid)
        print(task)
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
    except:
        print("reference insert duplicate")


def outputquery(tags): 
    database = r"photodata.db"
    conn = create_connection(database)

    sql = ''' SELECT filelocation FROM photos INNER JOIN reference ON photos.id = reference.photoid INNER JOIN tags ON reference.tagid = tags.id WHERE tagname=?'''
    returrnstack = []
    task = tags
    cur = conn.cursor()
    cur.execute(sql, (task,))
    conn.commit()

    for row in cur:
        #print(row[0])
        returrnstack.append(row[0])
    return returrnstack

def outputalltags():
    database = r"photodata.db"
    conn = create_connection(database)

    sql = ''' SELECT tagname FROM tags ORDER BY tagname ASC'''
    returrnstack = []
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    for row in cur:
        #print(row[0])
        returrnstack.append(row[0])
    return returrnstack

def outputalldb(): 
    database = r"photodata.db"
    conn = create_connection(database)

    sql = ''' SELECT filelocation, tags.tagname FROM photos INNER JOIN reference ON photos.id = reference.photoid INNER JOIN tags ON reference.tagid = tags.id ORDER BY filelocation ASC'''
    returrnstack = []
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    for row in cur:
        print(row[0], "     ", row[1])
        returrnstack.append((row[0], row[1]))
    return returrnstack

def buildAlbum(tags): 
    database = r"photodata.db"
    conn = create_connection(database)

    sql = ''' SELECT filelocation FROM photos INNER JOIN reference ON photos.id = reference.photoid INNER JOIN tags ON reference.tagid = tags.id WHERE tagname=? ORDER BY quality ASC'''
    returrnstack = []
    cur = conn.cursor()
    cur.execute(sql, (tags,))
    conn.commit()

    for row in cur:
        print(row[0])
        returrnstack.append(row[0])
    return returrnstack

def deleteimage(photolocation):
    database = r"photodata.db"
    conn = create_connection(database)
    
    sql1 = ''' SELECT id FROM photos where filelocation = ?'''
    sql2 = ''' DELETE FROM photos WHERE id = ?'''
    sql3 = ''' DELETE FROM reference WHERE photoid = ?'''

    cur = conn.cursor()
    cur.execute(sql1, (photolocation,))
    for row in cur:
        cur.execute(sql2, (row[0],))
        cur.execute(sql3, (row[0],))
    conn.commit()

def deletetag(tag):
    database = r"photodata.db"
    conn = create_connection(database)
    
    sql1 = ''' SELECT id FROM tags where tagname = ?'''
    sql2 = ''' DELETE FROM tags WHERE id = ?'''
    sql3 = ''' DELETE FROM reference WHERE tagid = ?'''

    cur = conn.cursor()
    cur.execute(sql1, (tag,))
    for row in cur:
        cur.execute(sql2, (row[0],))
        cur.execute(sql3, (row[0],))
    conn.commit()


#testing
if __name__ == '__main__': #testing
    Createdatabase()
    test2 = "database_test"
    '''test = r'F:/halcyon/4812.jpg'
    insertphoto(test, test2)
    input()'''
    '''for root, dirs, files in os.walk("F:\halcyon"): #all .png in folder
        for file in files:
            if file.endswith(".jpg"):
                insertphoto(os.path.join(root, file), test2)'''
    '''print()
    input()
    outputquery(test2)
    input()
    print()
    outputalltags()
    input()
    print()
    outputalldb()
    input()
    for root, dirs, files in os.walk("F:\pictures"): #all .png in folder
        for file in files:
            if file.endswith(".png"):
                insertphoto(os.path.join(root, file), test2)
    input()'''
    buildAlbum(test2)
    #outputalldb()

    
