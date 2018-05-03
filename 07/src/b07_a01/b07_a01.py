#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, subprocess, re

print "Content-type: text/html\n"
print

data = cgi.FieldStorage()
try:
    process = subprocess.Popen(["cal", "-h", data['month'].value, data['year'].value], stdout=subprocess.PIPE)
    output = process.stdout.read()
except:
    output = 'Input nicht vorhanden oder im falschen Format'

html = """
<html>
<head>
<meta charset=“utf-8”>
<title></title>
<link href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4' crossorigin='anonymous'>
<link rel="stylesheet" href="b07_a01.css">
</head>
<body>
<pre>
{cal}
</pre>
</body>
</html>
"""

html = html.format(cal=output)
print (html)
