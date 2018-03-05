import sqlite3
import os
from flask import g, request

#Path to the SQLite database
DATABASE = 'database.db'
app = None

def init_db(a_app):
    global app
    app = a_app
    return None

def db_exist():
    return os.path.isfile(DATABASE)

#Get the DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_table(conn, create_table_sql):
    try:
        co = conn.cursor()
        co.execute(create_table_sql)
    except Error as e:
        print (e)
    return None

def create_database_and_initialize_tables():



    sql_create_diary_users_table = """ CREATE TABLE IF NOT EXISTS diary_users (
                                    id INTEGER PRIMARY KEY,
                                    username text NOT NULL,
                                    password text NOT NULL,
                                    fullname text NOT NULL,
                                    age INTEGER NOT NULL
    ); """

    sql_create_diary_entries_table = """ CREATE TABLE IF NOT EXISTS diary_entries (
                                    id INTEGER PRIMARY KEY,
                                    title text NOT NULL,
                                    publish_date text NOT NULL,
                                    public INTEGER NOT NULL,
                                    text INTEGER NOT NULL,
                                    userid INTEGER NOT NULL
    ); """



    ##Insert into diary_users CREATE TABLE IF NOT EXISTS diary_users (
     #                               id INTEGER PRIMARY KEY,
     #                               username text NOT NULL,
     #                               password text NOT NULL,
     #                               fullname text NOT NULL,
     #                               age INTEGER NOT NULL
    #); """

    sql_create_user_token_table = """ CREATE TABLE IF NOT EXISTS user_token (
                                    token text PRIMARY KEY,
                                    userid INTEGER NOT NULL
    ); """

    sql_create_diary_users_default_row = """Insert into diary_users(username, password, fullname, age) VALUES('username1','pbkdf2:sha256:50000$KO1A6v5C$98b2af0bc9270c458062b8b1aeb510b0d0a06dfa7a28167ee79044f513e8d9d6','user full name','15');"""

    sql_create_user_token_default_row = """Insert or replace into user_token(token, userid) VALUES('11111111-1111-1111-1111-111111111111','1');"""

    sql_create_diary_entries_default_row1 = """Insert or replace into diary_entries(title, publish_date, public, text, userid) VALUES('Title of public entry 1','2013-02-27T13:37:00+00:00', 1, 'This is content of public entry 1',1);"""

    sql_create_diary_entries_default_row2 = """Insert or replace into diary_entries(title, publish_date, public, text, userid) VALUES('Title of public entry 2','2013-02-27T13:37:00+11:11', 1, 'This is content of public entry 2',1);"""

    sql_create_diary_entries_default_row3 = """Insert or replace into diary_entries(title, publish_date, public, text, userid) VALUES('Title of private entry 3','2013-02-27T13:37:00+22:22', 0, 'This is content of public entry 1',1);"""

    sql_create_diary_entries_default_row4 = """Insert or replace into diary_entries(title, publish_date, public, text, userid) VALUES('Title of private entry 4', '2013-02-27T13:37:00+22:33', 0, 'This is content of public entry 2',1);"""

    with app.app_context():
        conn = get_db()
        if conn is not None:
            #create the diary_users TABLE
            create_table(conn, sql_create_diary_users_table)
            create_table(conn, sql_create_user_token_table)
            create_table(conn, sql_create_diary_entries_table)
            conn.cursor().execute(sql_create_diary_users_default_row)
            conn.cursor().execute(sql_create_user_token_default_row)
            conn.cursor().execute(sql_create_diary_entries_default_row1)
            conn.cursor().execute(sql_create_diary_entries_default_row2)
            conn.cursor().execute(sql_create_diary_entries_default_row3)
            conn.cursor().execute(sql_create_diary_entries_default_row4)
            conn.commit()
            initalise = True
        else:
            print("[*] Error, cannot create the database connection!!")
        return
