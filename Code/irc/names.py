#!/usr/bin/python
import json

names_file = "/home/jumblesale/Code/canonical_names/canonical_names.json"


def get_name(name):
    try:
        with open(names_file) as names_data:
            names = json.load(names_data)
            try:
                return names[name]["userName"]
            except KeyError:
                return name
    except IOError:
        return name  # if we didn't already
