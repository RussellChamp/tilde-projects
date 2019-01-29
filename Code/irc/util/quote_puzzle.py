#!/usr/bin/python3

import json
import requests
import random
import re

quotefile = "/home/karlen/irc/quotes.txt"
chuckfile = "/home/krowbar/Code/irc/data/chuck.txt"
chuckApi = "https://api.icndb.com/jokes/random"

def get_quote():
    quotes = open(quotefile, "r").read().split("---")
    quote, attr = random.choice(quotes).strip().splitlines()
    quote = quote[:200]  # get only the first 200 chars
    word = random.choice([q for q in quote.split(" ") if len(q) > 1])
    quote = quote.replace(word, re.sub(r"[a-zA-Z]", "_", word))
    return [word, 'Fill in the blank: "' + quote + '" ' + attr]

def get_chuck():
    #chucks = open(chuckfile, "r").readlines()
    #chuck = random.choice(chucks).rstrip()[:200] # get only the first 200 chars
    # ha ha! let's see if we can confus login
    chuck = json.loads(requests.get(chuckApi).content.decode())['value']['joke'][:200]
    word = random.choice([w for w in chuck.split(" ") if len(w) > 1 and w.lower() != "chuck" and w.lower() != "norris"])
    chuck = chuck.replace(word, re.sub(r"[a-zA-Z]", "_", word)).replace("&quot;", "\"")
    return [word, 'Fill in the blank: "{}"'.format(chuck)] 
