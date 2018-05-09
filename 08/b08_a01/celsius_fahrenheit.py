#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, re

print "Content-type: text/html"
print

def printErrorMsg():
    print """<h3>Seriously.....numbers only!</h3>
                <a href='celsius_fahrenheit.html'>Try Again</a>"""

try:
	info = cgi.FieldStorage()
	celsius = info["celsius"].value
	celsius = celsius.strip()
	pattern = "^-?[0-9]+([,\.][0-9]+)?$"
	matches = re.match(pattern, celsius)
	if matches:
	    celsius = float(celsius.replace(",", "."))
	    fahrenheit = celsius * 1.8 + 32

	    html = """
	    <html>
	    <head>
	    <meta charset=“utf-8”>
	    <title>Input Validation</title>
	    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
	    <link rel="stylesheet" href="celsius_fahrenheit.css">
	    </head>
	    <body>
	    <h1>Congratulation</h1>
	    <h3>The given value has been successfully converted:</h3>
	    {C}°C -> {F}°F
	    </body>
	    </html>
	    """

	    html = html.format(C=celsius, F=fahrenheit)
	    print html
	else:
	    printErrorMsg()

except ValueError:
	printErrorMsg()


