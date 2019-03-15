#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

def getDuo():
    url = "https://www.theyfightcrime.org/"
    html = BeautifulSoup(requests.get(url).content, "html.parser")
    return html.findAll('p')[1].text
