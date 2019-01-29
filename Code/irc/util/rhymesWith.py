#!/usr/bin/python3
import requests

# from lxml.html import fromstring
from bs4 import BeautifulSoup
import random


def getRhymes(word):
    words = []
    url = "http://www.rhymer.com/RhymingDictionaryLast/%s.html" % word
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for t in soup.find_all("table", "table"):
        words.append(
            random.choice(
                [
                    w
                    for w in t.text.split("\n")
                    if w not in [u"", u"\xa0"] and "-" not in w
                ]
            )
        )
    return words


def rhymeZone(word):
    words = []
    url = (
        "http://rhymezone.com/r/rhyme.cgi?Word=%s&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
        % word
    )
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for t in soup.find_all("a", "d"):
        w = t.text.rstrip()
        if w not in [u"", u"\xa0"] and "?" not in t:
            words.append(w)
    random.shuffle(words)
    return words[0:5]
