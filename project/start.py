#!/usr/bin/python

import cgi, cgitb
cgitb.enable()
import requests, json
import sqlite3, re, os, Cookie
from random import shuffle

from mako.template import Template
from mako.lookup import TemplateLookup


print "Content-type: text/html"
print

def validate_topic(form):
    if "topic" not in form:
        return "any"

    topic = form["topic"].value

    if topic == "any":
        return "any"
    else:
        try:
            temp = int(topic)
            if(temp >= 8 and temp <= 32):
                return temp
            return "any"
        except ValueError:
            return "any"

def validate_diff(form):
    if "diff" not in form:
        return "easy"

    diff = form["diff"].value
    if diff == "easy" or diff == "medium" or diff == "hard":
        return diff.strip()
    return "easy"

def validate_type(form):
    if "type" not in form:
        return "multiple"

    type = form["type"].value
    if type == "boolean" or type == "multiple":
        return type.strip()
    return "multiple"

def validate_amount(amount):
    if "amount" not in form:
        return 1

    amount = form["amount"].value
    try:
        amount = int(amount)
        if amount <= 25 and amount >= 1:
            return amount
        else:
            return 1
    except ValueError:
        return 1

def validate_user_session(username):
    pattern = "^[0-9a-zA-Z#!-]+$"
    matches = re.match(pattern, username)
    if matches:
        return username.strip()
    else:
        return False


templates = TemplateLookup(directories=['templates/'], module_directory='modules/',
  output_encoding='utf-8', encoding_errors='replace')


form = cgi.FieldStorage()

topic = validate_topic(form)
diff = validate_diff(form)
type = validate_type(form)
amount = validate_amount(form)



if topic == "any":
    parameters = {"amount": amount, "difficulty": diff, "type": type}
else:
    parameters = {"amount": amount, "category": topic, "difficulty": diff, "type": type}

response = requests.get("https://opentdb.com/api.php", params=parameters)

result = []
correct = []
data = json.loads(response.content)
for question in data["results"]:
    all_answers = question["incorrect_answers"]
    all_answers.append(question["correct_answer"])
    shuffle(all_answers)
    result.append([question["question"], all_answers])
    correct.append(question["correct_answer"])

db = sqlite3.connect("quizzit.db", isolation_level=None)
cursor = db.cursor()
logged_in = False

if "HTTP_COOKIE" in os.environ:
    cookies = os.environ["HTTP_COOKIE"]
    c = Cookie.SimpleCookie()
    c.load(cookies)

    try:
        username = validate_user_session(c["username"].value)
        session_id_received = validate_user_session(c["session_id"].value)

        delete_prev = """DELETE FROM answers
                         WHERE sessionid=?"""
        cursor.execute(delete_prev, [session_id_received])

        insert_answer = """INSERT INTO answers
                           VALUES (?, ?)"""

        cursor.execute(insert_answer, [session_id_received, str(correct).strip("[]")])
        logged_in = True
    except KeyError:
        logged_in = False

if logged_in:
    correct_answers = '\"\"'
else:
    correct_answers = json.dumps(correct)

if len(result[0][1]) == 2:
    curr_template = templates.get_template("questions_boolean.html")
    print(curr_template.render(question=result[0][0], answer1=result[0][1][0],
        answer2=result[0][1][1], questions=json.dumps(result),
        correct=correct_answers))
else:
    curr_template = templates.get_template("questions_multiple.html")
    print(curr_template.render(question=result[0][0], answer1=result[0][1][0],
    answer2=result[0][1][1], answer3=result[0][1][2],
    answer4=result[0][1][3], questions=json.dumps(result),
    correct=correct_answers))
