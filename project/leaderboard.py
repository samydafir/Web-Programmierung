#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb
cgitb.enable()
import sqlite3

print "Content-type: text/html"
print

print"""<html><head>
        <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Saira'>
        <link rel='stylesheet' href='css/bootstrap.min.css'>
        <title>Leaderboard</title></head>
        <style>
        body {
            font-family: 'Saira', sans-serif;
            margin: 2%;
        }
        </style>
        <body>
        """

print"<h1>Leaderboard</h1>"

db = sqlite3.connect("quizzit.db", isolation_level=None)
cursor = db.cursor()

query = """SELECT username, SUM(questions), SUM(result)
           FROM results"""

cursor.execute(query)

print"<table class='table table-striped'>"
print"<tr><th>user</th><th>answered questions</th><td>correct answers</td><td>correct answers (%)</td></tr>"
row = cursor.fetchone()

while row is not None:
    percent = float(row[2])/float(row[1]) * 100
    print"<tr><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td><td>"+str(row[2])+"</td><td>"+str(percent)+"</td></tr>"
    row = cursor.fetchone()

print"""</table>
        </body>
        </html>"""
cursor.close()
db.close()
