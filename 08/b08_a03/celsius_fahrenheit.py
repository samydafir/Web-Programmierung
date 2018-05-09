#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, re
from mako.template import Template
from mako.lookup import TemplateLookup


print "Content-type: text/html"
print

templates = TemplateLookup(directories=['templates/'], module_directory='modules/',
  output_encoding='utf-8', encoding_errors='replace')

def print_form(error_type, error_message):
    curr_template = templates.get_template("form.html")
    print(curr_template.render(error=error_type, error_msg=error_message))


data = cgi.FieldStorage()
if 'celsius' not in data:
    print_form(" ", " ")


try:
    info = cgi.FieldStorage()
    celsius = info["celsius"].value
    #Commented out to force usage of try-catch
    #celsius = celsius.strip()
    #pattern = "^-?[0-9]+([,\.][0-9]+)?$"
    #matches = re.match(pattern, celsius)
    matches = True
    if matches:
        celsius = float(celsius.replace(",", "."))
        fahrenheit = celsius * 1.8 + 32
        curr_template = templates.get_template("success.html")
        print(curr_template.render(C=celsius, F=fahrenheit, style="btn btn-success btn-block"))
    else:
        print_form("error", "Only numbers are accepted. Please try again (RegEx failed).")

except ValueError:
	print_form("error", "Only numbers are accepted. Please try again (ValueError raised).")


