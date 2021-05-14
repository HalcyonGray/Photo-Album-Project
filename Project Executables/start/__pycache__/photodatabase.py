import sqlite3
from sqlite3 import Error
import imquality.brisque as brisque
from PIL import Image
import os  # for testing


# SQLITE studio is useful for checking the database
# probably should create global database location variable or  have gui save it and input location on ever def call
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
    database = r"photodata.db"

    # we are using a many to many realation strategy
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


def uploadphoto(task):
    try:
        database = r"photodata.db"
        conn = create_connection(database)

        sql = ''' INSERT INTO photos(filelocation, quality) VALUES(?,?)'''
        img = Image.open(task)
        quality = brisque.score(img)
        phototask = (task, abs(quality))
        cur = conn.cursor()
        cur.execute(sql, phototask)
        conn.commit()
        createtags(conn, ('notag',))
        insertphoto2(task, 'notag')

        return cur.lastrowid
    except:
        sql = ''' SELECT id FROM photos WHERE filelocation=?'''

        cur = conn.cursor()
        cur.execute(sql, (task,))
        conn.commit()

        return cur.fetchone()[0]


def findphoto(conn, task):
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


def insertphoto(photolocation, tags):
    database = r"photodata.db"
    conn = create_connection(database)
    cur = conn.cursor()

    formatphoto = (photolocation)
    formattag = ([tags])

    photoid = findphoto(conn, formatphoto)
    tagid = createtags(conn, formattag)
    outputalldb()
    deletereference2(photolocation, 'notag')
    outputalldb()

    try:
        sql = ''' INSERT INTO reference(photoid, tagid) VALUES(?,?)'''
        task = (photoid, tagid)
        cur.execute(sql, task)
        conn.commit()
    except:
        print("reference insert duplicate")


def insertphoto2(photolocation, tags):  # to prevent loop
    database = r"photodata.db"
    conn = create_connection(database)
    cur = conn.cursor()

    formatphoto = (photolocation)
    formattag = ([tags])

    photoid = findphoto(conn, formatphoto)
    tagid = createtags(conn, formattag)

    try:
        sql = ''' INSERT INTO reference(photoid, tagid) VALUES(?,?)'''
        task = (photoid, tagid)
        cur.execute(sql, task)
        conn.commit()
    except:
        print("reference insert duplicate")


def outputquery(tags):
    database = r"photodata.db"
    conn = create_connection(database)

    sql = ''' SELECT photos.id, filelocation FROM photos INNER JOIN reference ON photos.id = reference.photoid INNER JOIN tags ON reference.tagid = tags.id WHERE tagname=?'''
    returrnstack = []
    task = tags
    cur = conn.cursor()
    cur.execute(sql, (task,))
    conn.commit()

    for row in cur:
        returrnstack.append((row[0], row[1]))
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
        returrnstack.append((row[0], row[1]))
    return returrnstack


def outputalloftag(tag):
    database = r"photodata.db"
    conn = create_connection(database)

    sql = ''' SELECT filelocation, tags.tagname FROM photos INNER JOIN reference ON photos.id = reference.photoid INNER JOIN tags ON reference.tagid = tags.id WHERE tagname=? ORDER BY filelocation ASC'''
    returrnstack = []
    cur = conn.cursor()
    cur.execute(sql, (tag,))
    conn.commit()

    for row in cur:
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
        conn.commit()
        cur.execute(sql3, (row[0],))
        conn.commit()


def deletetag(tag):
    database = r"photodata.db"
    conn = create_connection(database)

    sql1 = ''' SELECT id FROM tags where tagname = ?'''
    sql2 = ''' DELETE FROM tags WHERE id = ?'''
    sql3 = ''' DELETE FROM reference WHERE tagid = ?'''
    sql4 = ''' SELECT COUNT(1) FROM reference WHERE photoid = ?'''
    cur = conn.cursor()
    cur.execute(sql1, (tag,))
    tagstack = outputquery(tag)
    for row in cur:
        cur.execute(sql2, (row[0],))
        conn.commit()
        cur.execute(sql3, (row[0],))
        conn.commit()
    for photo in tagstack:
        cur.execute(sql4, (photo[0],))
        exist = cur.fetchone()
        if (exist[0] == 0):
            insertphoto2(photo[1], 'notag')


def deletereference(photolocation, tag):
    database = r"photodata.db"
    conn = create_connection(database)

    sql1 = ''' SELECT id FROM tags where tagname = ?'''
    sql2 = ''' SELECT id FROM photos where filelocation = ?'''
    sql3 = ''' DELETE FROM reference WHERE tagid = ? AND photoid = ?'''
    sql4 = ''' SELECT COUNT(1) FROM reference WHERE photoid = ?'''
    cur = conn.cursor()
    cur.execute(sql1, (tag,))
    r1 = cur.fetchone()
    cur.execute(sql2, (photolocation,))
    r2 = cur.fetchone()
    cur.execute(sql3, (r1[0], r2[0]))
    conn.commit()
    cur.execute(sql4, (r2[0],))
    exist = cur.fetchone()
    if (exist[0] == 0):
        insertphoto2(photolocation, 'notag')


def deletereference2(photolocation, tag):  # to prevent loop
    database = r"photodata.db"
    conn = create_connection(database)

    sql1 = ''' SELECT id FROM tags where tagname = ?'''
    sql2 = ''' SELECT id FROM photos where filelocation = ?'''
    sql3 = ''' DELETE FROM reference WHERE tagid = ? AND photoid = ?'''
    cur = conn.cursor()
    cur.execute(sql1, (tag,))
    r1 = cur.fetchone()
    cur.execute(sql2, (photolocation,))
    r2 = cur.fetchone()
    cur.execute(sql3, (r1[0], r2[0]))
    conn.commit()


# testing
if __name__ == '__main__':  # testing
    Createdatabase()
    uploadphoto(r'F:\halcyon\4812.jpg')
    outputalldb()
    insertphoto(r'F:\halcyon\4812.jpg', 'test')
    outputalldb()
    deletereference(r'F:\halcyon\4812.jpg', 'notag')
    outputalldb()