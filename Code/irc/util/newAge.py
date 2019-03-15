#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

def ReionizeElectrons():
    url = "http://sebpearce.com/bullshit/"
    html = BeautifulSoup(requests.get(url).content, "html.parser")
    return html.findAll('p')[1].text
