#!/usr/bin/python3
import json
import random
import requests

def getRandom(query = "randomlists"):
    query = query.lower().replace(' ', '-')
    message = ""
    request = requests.get("https://www.randomlists.com/data/{}.json".format(query))
    if request.status_code == 404:
        request = requests.get("https://www.randomlists.com/data/random-{}.json".format(query))
    if request.status_code == 404:
        message = "No results found. Try"
        request = requests.get("https://www.randomlists.com/data/randomlists.json")

    jdata = json.loads(request.content)
    items = list()

    if 'RandL' in jdata:
        items = list(jdata['RandL']['items'])
    elif 'data' in jdata:
        items = list(jdata['data'])

    item = random.choice(items)
    if 'name' in item:
        message += " " + item['name']
    if 'detail' in item:
        message += ": " + item['detail']
    if 'subtle' in item:
        message += " (" + item['subtle'] + ")"
    if message == "":
        message = item

    return message.strip()
