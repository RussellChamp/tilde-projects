import duckduckgo
import urllib
from bs4 import BeautifulSoup

def xkcd(query):
    res = duckduckgo.get_zci('site:xkcd.com ' + query);
    title = "";
    try: #ddg returns a url for these searches. i want a title as well
        title = BeautifulSoup(urllib.urlopen(res).read(), 'html.parser').title.text
    except:
        pass #just swallow the error. maybe the result wasn't a url or something else bad happened
    return (((title + ' - ') if title else '') + res).encode('ascii', 'ignore')

def xkcd_links(query):
    url = "https://duckduckgo.com/html/?q=site%3Axkcd.com+" + query.replace(' ', '+')
    soup = BeautifulSoup(urllib.urlopen(url).read(), 'html.parser')
    links = filter(lambda a: a[0:8] == 'xkcd.com', [a.text.strip() for a in soup.find_all("div", class_="url")])
    def pretty_link(url):
         data = BeautifulSoup(urllib.urlopen('http://'+url).read(), 'html.parser')
         title = data.title.text if data.title else ''
         return (title + ' - ' + url) if title else url

    links = map(lambda url: pretty_link(url), links)
    return links
