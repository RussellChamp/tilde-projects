#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

def getWisdom():
    url = "http://www.wisdomofchopra.com/iframe.php"
    html = BeautifulSoup(requests.get(url).content, "html.parser")
    return html.find("td", { "id": "quote" }).text
