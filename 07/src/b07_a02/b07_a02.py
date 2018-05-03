#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi

print "Content-type: text/html\n"
print

file = open("/tmp/counter.txt", "r+") 

data = cgi.FieldStorage()
try:
    number = int(file.read())
except ValueError:
    number = 1


if "action" in data.keys():
    file.seek(0)
    file.truncate()
    
    if data['action'].value == 'increment':
	number += 1
    else:
	number = 1

    file.write(str( number))

file.close()

html = """
<html>
<head>
<meta charset=“utf-8”>
<title></title>
<link href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4' crossorigin='anonymous'>
<link rel="stylesheet" href="b07_a02.css">
</head>
<body>
<h1>
{currcount}
</h1>
<form method="get" action="b07_a02.cgi">
<input type="submit" class="btn btn-primary" name="action" value="increment">
<input type="submit" class="btn btn-primary" name="action" value="reset">
</form>
</body>
</html>
"""

html = html.format(currcount=number)
print (html)
