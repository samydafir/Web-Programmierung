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
        }

        main {
            margin: 2%;
        }
        </style>
        <body>
        <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
        <a class="navbar-brand logo" href="index.html">QuizzIT</a>
        <div class="navbar-collapse">
        <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="index.html">Back</a>
        </li>
        </ul>
        </div>
        </nav>
        """

print"<main><h1>Leaderboard</h1><br>"

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
        </main>
        </body>
        </html>"""
cursor.close()
db.close()
