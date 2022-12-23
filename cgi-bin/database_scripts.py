#!/usr/bin/env python

import sqlite3
import cgi


form = cgi.FieldStorage()

names = form.getvalue("names")
coming = form.getvalue("coming")
message = form.getvalue("message")
guestNumber = form.getvalue("guestNumber")
key = form.getvalue("key")

ALL_KEYS = ["coma", "mafra", "italos", "test", "test2"]

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect("users.db")
        return conn
    except Exception as e:
        print(e)
        return None


def create_table():
    query = "CREATE TABLE IF NOT EXISTS user (id integer PRIMARY KEY AUTOINCREMENT, names text NOT NULL, message text, guestnumber int, coming BOOLEAN NOT NULL CHECK (coming IN (0, 1)), key text NOT NULL UNIQUE);"

    try:
        conn = create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute(query)
            print(f"Created Table")
    except Exception as e:
        print(e)


def insert_into_db(names, coming, message, guestNumber, key):

    

    query = "INSERT INTO user(names, message, guestnumber, coming, key) VALUES(?,?,?,?,?)"
    if coming not in [0,1]:
        print(f"coming not set as boolean [0,1]!")
        return
    checked_key = check_key(key)
    print(f"Checked Key: {checked_key}")
    if checked_key is False or checked_key is None:
        return
    if checked_key == 1:
        update_entry(names, message, guestNumber, coming, key)
        return
    values = (names, message, guestNumber, coming, key)
    try:
        
        conn = create_connection()
        create_table()
        if conn is not None:
            c = conn.cursor()
            c.execute(query, values)
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)


def get_all_entries():
    query = "SELECT * FROM user;"
    try:
        conn = create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            print(rows)
            conn.close()
    except Exception as e:
        print(e)


def get_all_coming_guests():
    query = "SELECT * FROM user WHERE coming = 1;"
    try:
        conn = create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            print(rows)
            conn.close()
    except Exception as e:
        print(e)
    

def get_user_from_key(key):
    if key not in ALL_KEYS:
        print(f"Wrong key entered!")
        return False

    query = f"SELECT * FROM user WHERE key = \'{key}\';"
    try:
        conn = create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute(query)
            user = c.fetchall()  # 1, if key already exists in table. 0, else.
            conn.close()
            return user

    except Exception as e:
        print(e)
        return None
        

def check_key(key):

    if key not in ALL_KEYS:
        print(f"Wrong key entered!")
        return False

    query = f"SELECT count(key) FROM user WHERE key = \'{key}\';"
    try:
        conn = create_connection()
        if conn is not None:
            c = conn.cursor()
            c.execute(query)
            key_already_exists = c.fetchone()[0]  # 1, if key already exists in table. 0, else.
            conn.close()
            if key_already_exists == 1:
                print(f"Key already exists in Database!")
            else:
                print(f"Key is good!")
            return key_already_exists # Either 0 or 1
        return None
    except Exception as e:
        return None
        print(e)


def update_entry(names, message, guestNumber, coming, key):
    print(f"Trying to update key: {key}")
    query = f"UPDATE user SET names = ?, message = ?, guestNumber = ?, coming = ?, key = ? WHERE key = \'{key}\';"
    try:
        conn = create_connection()
        if conn is not None:
            values = (names, message, guestNumber, coming, key)
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            conn.close()
            print(f"Entry has been updated!")

    except Exception as e:
        print(e)


#conn = create_connection()
#insert_into_db("Corinna und Mario", "Very Excited!", 2, 1, "coma")
#insert_into_db("Marius und Franzi", "Super Excited!", 2, 1, "mafra")
#insert_into_db("Annika, Francesco & Bella", "All 3 of us are coming", 3, 1, "italos")
#insert_into_db("John & Jane", "We are getting married on the same day.", 0, 0, "test")
print(f"Coming:")
get_all_coming_guests()
print(f"All Replys:")
get_all_entries()
print(f"Is Key present?")
print(get_user_from_key("coma"))