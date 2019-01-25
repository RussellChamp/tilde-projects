#!/usr/bin/python3
from bs4 import BeautifulSoup
import random
import requests


def get_philosophy(word, max_steps=20):
    step_words = [word]
    steps = 0

    url = "https://en.wikipedia.org/wiki/%s" % word
    while steps < max_steps:
        print("url: {}".format(url))
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        title = soup.find("h1", id="firstHeading")
        content = soup.find("div", id="mw-content-text")
        if not content:
            break
        item = [
            item
            for item in content.find_all("a")
            if not item.get("class")
            and not item.get("target")
            and item.get("title")
            and not "Wikipedia:" in item.get("title")
            and not "Category:" in item.get("title")
            and not "Help:" in item.get("title")
            and not "Portal:" in item.get("title")
            and not "Special:" in item.get("title")
            and not "Talk:" in item.get("title")
            and not "Template:" in item.get("title")
            and not "File:" in item.get("title")
            and "Edit section:" not in item.get("title")
            and "Commons:" not in item.get("title")
            and not item.get("title") in step_words
        ][0]
        step_words.append(item.get("title"))
        # print item.get('title') + "\n"
        url = "https://en.wikipedia.org{}".format(item.get("href"))
        steps += 1
    return step_words


def containsAny(str, set):
    return 1 in [c in str for c in set]


def get_philosophy_lower(word, max_steps=20):
    step_words = [word]
    steps = 0

    url = "https://en.wikipedia.org/wiki/{}".format(word.replace(" ", "%20"))
    while steps < max_steps:
        print("url: {}".format(url))
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        if soup.find(id="noarticletext"):
            step_words.append("(not found)")
            break

        title = soup.find("h1", id="firstHeading")
        content = soup.find("div", id="mw-content-text")
        if not content:
            break
        links = [
            item
            for item in content.find_all("a")
            if not item.get("class")
            and item.text
            and item.text[0].islower()
            and not containsAny(item.text, ":()")
            and item.get("title")
            and not containsAny(item.get("title"), ":()")
            and not item.get("title") in step_words
        ]
        if not links:
            step_words.append("(dead end)")
            break
        item = links[0]  # grab the first good link item
        # print "Checking %s %s" % (item.get('title'), item.text)
        step_words.append(item.get("title"))
        if item.get("title") == "Philosophy":
            break
        # print item.get('title') + "\n"
        url = "https://en.wikipedia.org%s" % item.get("href")
        steps += 1
    return step_words
