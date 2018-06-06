#!/usr/bin/python

import xml.etree.ElementTree as ET
import json

tree = ET.parse("simple.xml")
root = tree.getroot()
dict = {}


def xml_to_dict(node):

    if len(node) > 0:
        temp = {}
        temp_array = []
        for child in node:
            temp_array.append(xml_to_dict(child))
        temp[node.tag] = temp_array
    else:
        temp = {}
        temp[node.tag] = node.text

    return temp



dict = {root.tag: xml_to_dict(root)}
print json.dumps(dict, indent=4, sort_keys=True)
with open("data_file.json", "w") as write_file:
    json.dump(dict, write_file, indent=4, sort_keys=True)
