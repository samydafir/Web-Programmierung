#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb
cgitb.enable()
import sqlite3, re
import os, Cookie

def validate_user_session(username):
    pattern = "^[0-9a-zA-Z#!-]+$"
    matches = re.match(pattern, username)
    if matches:
        return username.strip()
    else:
        return False

db = sqlite3.connect("quizzit.db", isolation_level=None)
cursor = db.cursor()

cookie_present = False

if "HTTP_COOKIE" in os.environ:
    cookies = os.environ["HTTP_COOKIE"]
    c = Cookie.SimpleCookie()
    c.load(cookies)

    try:
        username = validate_user_session(c["username"].value)
        session_id_received = validate_user_session(c["session_id"].value)

        cookie_present = True
    except KeyError:
        cookie_present = False


if cookie_present == True:

    print "Content-type: text/html"
    print "Set-Cookie: username=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
    print "Set-Cookie: session_id=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
    print
    
    get_user = """SELECT username, sessionid
               FROM users
               WHERE username=? AND sessionid=?"""

    cursor.execute(get_user, [username, session_id_received])

    true_user = cursor.fetchone()

    if true_user is not None:
        terminate_session = """UPDATE users SET sessionid=''
                               WHERE username=? and sessionid=?"""

        cursor.execute(terminate_session, [username, session_id_received])

    remove_answers = """DELETE FROM answers
                WHERE sessionid=?"""

    cursor.execute(remove_answers, [session_id_received])


cursor.close()
db.close()
