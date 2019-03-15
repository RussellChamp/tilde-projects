#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

# These seem to get the same result each time we run them. I think TVTropes
# has some anti-scraping mechanism
def getTrope():
    url = "https://tvtropes.org"
    html = BeautifulSoup(requests.get(url).content, "html.parser")
    return url + html.find('a', { 'class': 'button-random-trope' })['href']

def getMedia():
    url = "https://tvtropes.org"
    html = BeautifulSoup(requests.get(url).content, "html.parser")
    return url + html.find('a', { 'class': 'button-random-media' })['href']
