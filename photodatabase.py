import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\sqlite\db\pythonsqlite.db" #must create C:\sqlite\db\  folders first 


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


if __name__ == '__main__':
    main()