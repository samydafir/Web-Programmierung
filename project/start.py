#!/usr/bin/python

import cgi, cgitb
cgitb.enable()
import requests, json
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
data = json.loads(response.content)
for question in data["results"]:
    result.append([question["question"], question["correct_answer"], question["incorrect_answers"]])


if len(result[0][2]) == 1:
    curr_template = templates.get_template("questions_boolean.html")
    print(curr_template.render(question=result[0][0], answer1=result[0][1],
        answer2=result[0][2][0], questions=json.dumps(data["results"])))
else:
    curr_template = templates.get_template("questions_multiple.html")
    print(curr_template.render(question=result[0][0], answer1=result[0][1],
        answer2=result[0][2][0], answer3=result[0][2][1],
        answer4=result[0][2][2], questions=json.dumps(data["results"])))
