#!/usr/bin/python3
from bs4 import BeautifulSoup
import random
import re
import requests

def tumble(url):
    # Find the max pages
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    pages = soup.findAll("span", "page-numbers")[0].text.split("/")[
        1
    ]  # this could totally fail several ways
    tries = 3
    while True:
        try:
            page = random.randrange(1, int(pages) + 1)

            # Parse a page
            soup = BeautifulSoup(
                requests.get("{}/page/{}".format(url, page)).content, "html.parser"
            )
            article = random.choice(soup.findAll("article"))
            quote = article.find("blockquote").text.replace("\n", "")
            if len(article.find("footer").findAll("ul")) > 1:
                quote += re.sub(
                    "\n+", " ", article.find("footer").findAll("ul")[0].text
                )
                # the hash tags
                quote += (
                    "("
                    + re.sub("\n+", " ", article.find("footer").findAll("ul")[1].text)
                    + ")"
                )
                # and the date and notes
            else:
                quote += (
                    "("
                    + re.sub("\n+", " ", article.find("footer").findAll("ul")[0].text)
                    + ")"
                )
                # just the date and notes

            return quote
        except:  # sometimes we fail. let's retry a few times
            if tries == 0:
                return ""
            else:
                tries -= 1
        break
