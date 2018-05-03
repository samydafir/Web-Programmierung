#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import Cookie
import os
import cPickle as pickle

data = cgi.FieldStorage()
cookie = Cookie.SimpleCookie()
colour = "id0"

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    cookie.load(cookie_string)

if "colour_id" in cookie:
    colours = pickle.load(open("/tmp/pickle.p", "rb"))
    colour = cookie['colour_id'].value
    if "colour_id" in data.keys():
        cookie['colour_id'] = data['colour_id'].value
        colour = data['colour_id'].value

    colour = colours[colour]

else:
    colours = {"id0":"white", "id1":"red", "id2":"green", "id3":"orange", "id4":"purple"}
    pickle.dump(colours, open('/tmp/pickle.p', 'wb'))
    cookie['colour_id'] = colour
    cookie['colour_id']['expires'] = 60*60
    colour = colours[colour]

print(cookie)
print ("Content-type: text/html\n")
print


html = """
<html>
<head>
<meta charset=“utf-8”>
<title></title>
<link href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4' crossorigin='anonymous'>
<link rel="stylesheet" href="b07_a04.css">
</head>

<body style='background-color:{bgcolour};'>
<h1>
{bgcolour}
</h1>
<form method="get" action="b07_a04.cgi">
    <select class="form-control col-md-4" name="colour_id">
        <option value="id1">red</option>
        <option value="id2">green</option>
        <option value="id3">orange</option>
        <option value="id4">purple</option>
    </select>
<input type="submit" class="btn btn-success" name="change_colour" value="change colour">
</form>
</body>
</html>
"""

html = html.format(bgcolour=colour)
print (html)
