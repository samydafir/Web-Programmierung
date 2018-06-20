#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb
cgitb.enable()
import sqlite3, re, hashlib

print "Content-type: text/html"
print

def validate_user(username):
    pattern = "^[0-9a-zA-Z#!]+$"
    matches = re.match(pattern, username)
    if matches:
        return username.strip()
    else:
        return False


def validate_pw(pw, pw_repeat):
    pattern = "^[0-9a-zA-Z#!]+$"
    matches = re.match(pattern, pw) and re.match(pattern, pw_repeat) and pw == pw_repeat

    if  matches:
        salt = "9fYQxrcOyhnk7AoCDvQF"
        password = hashlib.sha256(pw.strip() + "" + salt).hexdigest()
        return password
    else:
        return False



db = sqlite3.connect("quizzit.db", isolation_level=None)
cursor = db.cursor()
data = cgi.FieldStorage()


if "username" in data and "password" in data and "password_repeat" in data:
    username = validate_user(data["username"].value)
    password = validate_pw(data["password"].value, data["password_repeat"].value)
else:
    username = False
    password = False

query = """SELECT COUNT(username)
           FROM users
           WHERE username=?"""

cursor.execute(query, [username])
result = cursor.fetchone()[0]


if int(result) == 0 and username != False and password != False:
    insert_query = """INSERT INTO users
                      VALUES (?, ?, 0, 0)"""
    cursor.execute(insert_query, [username, password])

    print(True)
else:
    print(False)

cursor.close()
db.close()
