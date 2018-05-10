#!/usr/bin/python
# -*- coding: utf-8 -*-

from mako.template import Template
from mako.lookup import TemplateLookup

templates = TemplateLookup(directories=['templates/'], module_directory='modules/', 
  output_encoding='utf-8', encoding_errors='replace')

curr_template = templates.get_template("header.py")

curr_template.render() 

curr_template = templates.get_template("index.html")

print(curr_template.render(teststring="test", style="btn btn-success btn-block"))


