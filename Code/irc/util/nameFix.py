#!/usr/bin/python3

import json

names = {
    "jumblesal": "jumblesale",
    "hardmath1": "kc",
    "hardmath123": "kc",
    "bendorphan": "endorphant",
    "endorphan": "endorphant",
    "synergian": "synergiance",
}

def fixName(name):
    return names[name] if name in names else name

def get_name(name):
    names_file = "/home/jumblesale/Code/canonical_names/canonical_names.json"
    try:
        with open(names_file) as names_data:
            names = json.load(names_data)
            try:
                return names[name]["userName"]
            except KeyError:
                return name
    except IOError:
        return name  # if we didn't already
