#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import Cookie
import os

data = cgi.FieldStorage()
cookie = Cookie.SimpleCookie()
cookie_set = "Visited previously. Cookie present"

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    cookie.load(cookie_string)

if "visited" not in cookie:
    cookie['visited'] = "yes"
    cookie['visited']['expires'] = 60*60
    cookie_set = "First time visit. Cookie created"
    print (cookie)

if "delete_cookie" in data.keys() and "visited" in cookie:
    cookie['visited'] = ""
    cookie['visited']['expires'] = "Thu, 01 Jan 1970 00:00:00 GMT"
    cookie_set = "Cookie deleted"
    print (cookie)

print ("Content-type: text/html\n")
print


html = """
<html>
<head>
<meta charset=“utf-8”>
<title></title>
<link href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4' crossorigin='anonymous'>
<link rel="stylesheet" href="b07_a03.css">
</head>
<body>
<h1>
{cookie}
</h1>
<form method="get" action="b07_a03.cgi">
<input type="submit" class="btn btn-primary" name="delete_cookie" value="delete_cookie">
</form>
</body>
</html>
"""

html = html.format(cookie=cookie_set)
print (html)
