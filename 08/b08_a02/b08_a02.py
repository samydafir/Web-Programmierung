#!/usr/bin/python
# -*- coding: utf-8 -*-

from mako.template import Template
from mako.lookup import TemplateLookup

templates = TemplateLookup(directories=['templates/'], module_directory='modules/', 
  output_encoding='utf-8', encoding_errors='replace')

curr_template = templates.get_template("output.html")

print "Content-type: text/html\n" 
print

print(curr_template.render(teststring="test", style="btn btn-success btn-block"))
