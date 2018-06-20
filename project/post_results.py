#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb
cgitb.enable()
import sqlite3, re
import os, Cookie, json

print "Content-type: text/html"
print


def validate_user_session(username):
    pattern = "^[0-9a-zA-Z#!-]+$"
    matches = re.match(pattern, username)
    if matches:
        return username.strip()
    else:
        return False

db = sqlite3.connect("quizzit.db", isolation_level=None)
cursor = db.cursor()
data = cgi.FieldStorage()

save = False

if "HTTP_COOKIE" in os.environ:
    cookies = os.environ["HTTP_COOKIE"]
    c = Cookie.SimpleCookie()
    c.load(cookies)

    try:
        username = validate_user_session(c["username"].value)
        session_id_received = validate_user_session(c["session_id"].value)
        query = """SELECT sessionid
                   FROM users
                   WHERE username=?"""

        cursor.execute(query, [username])

        true_session_id = cursor.fetchone()[0]

        save = True
    except KeyError:
        save = False


if save == True and session_id_received == true_session_id:
    get_correct_answers = """SELECT answers FROM answers
                             WHERE sessionid=?"""

    cursor.execute(get_correct_answers, [true_session_id])
    correct_answers = cursor.fetchone()[0]
    correct_answers = json.dumps(correct_answers).split(",")
    received_answers = data.getlist("answers[]")
    if len(received_answers) == len(correct_answers):
        points = 0
        for i in range(len(received_answers)):
            if received_answers[i] == correct_answers[i].replace('"', '').replace("'", "").strip()[1:]:
                points += 1

        insert_results = """INSERT INTO results
                            VALUES (?, ?, ?)"""

        cursor.execute(insert_results, [username, len(correct_answers), points])

        delete_solution = """DELETE FROM answers
                             WHERE sessionid=?"""
        cursor.execute(delete_solution, [true_session_id])

        print (str(len(correct_answers)) + "," + str(points))


cursor.close()
db.close()
