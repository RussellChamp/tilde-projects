#!/usr/bin/python3
import random
import re

dictDir = "/usr/share/dict/"

def getBanter(morphWord="bant", dictName="words"):
    with open(dictDir + dictName, "r") as dict:
        # get rid of all the words with apostrophes
        words = list(filter(lambda word: re.search(r"^[^']*$", word), dict.readlines()))

        head = getBanterHead(words, morphWord)
        tail = getBanterTail(words, morphWord)

        if head == "" and tail == "":
            return "" # dang, we just failed
        else:
            # pick randomly between non-empty strings
            return random.choice([w for w in [head, tail] if w != ""])

def getBanterHead(words, morphWord):
    morphHead = morphWord[0:-1]
    morphLast = morphWord[-1]

    filtered = list(filter(lambda word: re.search(morphHead, word), words))
    if len(filtered) == 0:
        return "" # nothing applicable found

    word = random.choice(filtered).strip("\n")
    end = word.find(morphHead) + len(morphHead)
    if end == len(word):
        return word + morphLast
    else:
        if "aeiou".find(word[end]) > -1:  # just append 't'
            return word[:end] + morphLast + word[end:]
        else:  # replace the letter with 'b'
            return word[:end] + morphLast + word[end + 1 :]

def getBanterTail(words, morphWord):
    morphTail = morphWord[1:]
    morphFirst = morphWord[0]

    filtered = list(filter(lambda word: re.search(morphTail, word), words))
    if len(filtered) == 0:
        return "" # nothing applicable found

    word = random.choice(filtered).strip("\n")
    start = word.find(morphTail)
    if start == 0:
        return morphFirst + word
    else:
        if "aeiou".find(word[start]) > -1:  # just append a 'b'
            return word[:start] + morphFirst + word[start:]
        else:  # replace the letter with 'b'
            return word[: start - 1] + morphFirst + word[start:]
