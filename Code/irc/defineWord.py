#!/usr/bin/python3
import urllib
from bs4 import BeautifulSoup
import random


def define(word):
    defs = []
    url = "http://www.merriam-webster.com/dictionary/{}".format(word)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    head = soup.find("div", id="headword")
    if head:
        for p in head.find_all("p"):
            defs.append(p.text)
    return defs


key = open("/home/krowbar/.secret/key").readline().rstrip()


def defWord(word, short=True):
    defs = []
    url = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{}?key={}".format(
        word, key
    )
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html5lib")
    entry = soup.find("entry")
    if entry:
        for d in entry.find_all("dt"):
            defs.append(d.text)
    if short:
        return " ".join(defs)
    else:
        return defs
