import random
import re

quotefile = "/home/karlen/irc/quotes.txt"


def get_quote():
    quotes = open(quotefile, "r").read().split("---")
    quote, attr = random.choice(quotes).strip().splitlines()
    quote = quote[:200]  # get only the first 200 chars
    word = random.choice([q for q in quote.split(" ") if len(q) > 1])
    quote = quote.replace(word, re.sub(r"[a-zA-Z]", "_", word))
    return [word, 'Fill in the blank: "' + quote + '" ' + attr]
