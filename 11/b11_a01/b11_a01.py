#!/usr/bin/python

import xml.etree.ElementTree as ET
import json

def duplicate_keys(node):
    keys = set()
    for child in node:
        if child.tag in keys:
            return True;
        else:
            keys.add(child.tag)
    return False


def xml_to_dict(node):

    dup = duplicate_keys(node)

    temp = {}
    if len(node) > 0:
        temp_array = []
        for child in node:
            if dup:
                temp_array.append({child.tag: xml_to_dict(child)})
            else:
                temp[child.tag] = xml_to_dict(child)

        if dup:
            temp[node.tag] = temp_array

    else:
        temp[node.tag] = node.text

    return temp

tree = ET.parse("simple.xml")
root = tree.getroot()

dict = xml_to_dict(root)
print json.dumps(dict, indent=2, sort_keys=False)
with open("data_file.json", "w") as write_file:
    json.dump(dict, write_file, indent=2, sort_keys=False)
