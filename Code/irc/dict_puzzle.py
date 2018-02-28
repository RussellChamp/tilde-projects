#!/usr/bin/python
import random
import inflect

p = inflect.engine()
dictionary = "/usr/share/dict/american-english-small"

def get_puzzle():
    dict_words = [word.rstrip() for word in open(dictionary).readlines() if "'" not in word]
    words = random.sample(dict_words, 3)
    key = random.randrange(0,3) #get values 1-3
    puzzle = "When alphebetized, what is the " + p.ordinal(p.number_to_words(key+1)) + " in " + ", ".join(words)
    words.sort()
    answer = words[key]
    return [answer, puzzle]
