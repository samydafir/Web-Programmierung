#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb
cgitb.enable()
import sqlite3, re, hashlib
import uuid

def validate_user(username):
    pattern = "^[0-9a-zA-Z#!]+$"
    matches = re.match(pattern, username)
    if matches:
        return username.strip()
    else:
        return False

def validate_pw(pw):
    pattern = "^[0-9a-zA-Z#!]+$"
    matches = re.match(pattern, pw)

    if  matches:
        salt = "9fYQxrcOyhnk7AoCDvQF"
        password = hashlib.sha256(pw.strip() + "" + salt).hexdigest()
        return password
    else:
        return False

db = sqlite3.connect("quizzit.db", isolation_level=None)
cursor = db.cursor()
data = cgi.FieldStorage()

if "username" in data and "password" in data:
    username = validate_user(data["username"].value)
    password = validate_pw(data["password"].value)
else:
    username = False
    password = False

print "Content-type: text/html"

if username != False and password != False:

    session_id = str(uuid.uuid4())

    query = """SELECT username, password
               FROM users
               WHERE username=?"""

    cursor.execute(query, [username])
    result = cursor.fetchone()

    if result != None and result[1] == password:
        set_login = """UPDATE users
                     SET sessionid=?, loggedin=?
                     WHERE username=?"""
        cursor.execute(set_login, [session_id, 1, username])

        print 'Set-Cookie: session_id=' + str(session_id) + "; Max-Age=86400";
        print 'Set-Cookie: username=' + str(username) + "; Max-Age=86400";
        print

        print (True)
    else:
        print
        print(False)

else:
    print
    print(False)

cursor.close()
db.close()
