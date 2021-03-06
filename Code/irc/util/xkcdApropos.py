#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import util.duckduckgo

def xkcd(query):
    res = util.duckduckgo.get_zci("site:m.xkcd.com " + query)
    title = ""
    try:  # ddg returns a url for these searches. i want a title as well
        title = BeautifulSoup(requests.get(res).content, "html.parser").title.text
    except:
        pass  # just swallow the error. maybe the result wasn't a url or something else bad happened
    return [(((title + " - ") if title else "") + res)]


# never mind, blocked by ddg
# def xkcd_links(query):
#    url = "https://duckduckgo.com/html/?q=site%3Axkcd.com+" + query.replace(' ', '+')
#    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
#    items = soup.find_all("a", class_="result__a")
#    print items
#    items = list(filter(lambda i: i[0:8] == 'xkcd.com',
#    [i.find(class_="result__title").text.strip() for i in items]))
#    print items
#    def pretty_link(item):
#         url = item.find(class_="result__url").text.strip()
#         title = item.find(class_="result__title").text.strip()
#         return (title + ' - ' + url) if title else url
#
#    links = map(lambda url: pretty_link(url), items)
#    return links
