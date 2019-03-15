#!/usr/bin/python3

import json
import requests
import random
import re

quotefile = "/home/karlen/irc/quotes.txt"
wordsfile = "/usr/share/dict/words"
chuckfile = "/home/krowbar/Code/irc/data/chuck.txt"
chuckApi = "https://api.icndb.com/jokes/random"

def get_quote():
    quotes = open(quotefile, "r").read().split("---")
    quote, attr = random.choice(quotes).strip().splitlines()
    attempt = 10
    dict_words = open(wordsfile).read().split()
    while True:
        good_words = [w for w in quote.split() if w in dict_words and len(w) > 2]
        if len(good_words) > 3 or attempt is 0:
            break #either we got a good one or we gave up
        quote, attr = random.choice(quotes).strip().splitlines()
        attempt = attempt - 1

    quote = quote[:200]  # get only the first 200 chars
    word = random.choice([q for q in quote.split() if len(q) > 2 and q in dict_words] or [q for q in quote.split() if len(q) > 1])
    quote = quote.replace(word, re.sub(r"[a-zA-Z]", "_", word))
    return [word, 'Fill in the blank: "{}" {}'.format(quote, attr)]

def get_chuck():
    #chucks = open(chuckfile, "r").readlines()
    #chuck = random.choice(chucks).rstrip()[:200] # get only the first 200 chars
    # ha ha! let's see if we can confuse login
    chuck = json.loads(requests.get(chuckApi).content.decode())['value']['joke'][:200]
    word = random.choice([w for w in chuck.split(" ") if len(w) > 1 and w.lower() != "chuck" and w.lower() != "norris"])
    chuck = chuck.replace(word, re.sub(r"[a-zA-Z]", "_", word)).replace("&quot;", "\"")
    return [word, 'Fill in the blank: "{}"'.format(chuck)]
