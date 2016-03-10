import urllib
from bs4 import BeautifulSoup
import random


(userId,token) = open("/home/krowbar/.secret/s4token").readline().rstrip().split(',')

def get_acros(word):
  acros = []
  url = "http://www.stands4.com/services/v2/abbr.php?uid=%s&tokenid=%s&term=%s" % (userId, token, word)
  soup = BeautifulSoup(urllib.urlopen(url).read(), 'html5lib')
  results = soup.find_all('result')
  #there are lots of cases where the same definition is repeated multiple times under different categories. this is dumb so we should do a little more work
  defs = []
  for r in results:
      rdef = r.find('definition').text
      match = next((x for x in defs if x['definition'] == rdef), None)
      if match is not None:
          #if we find a match, add the category to the existing categories and increase the score
          match['categories'].append(((r.find('parentcategoryname').text + '\\') if r.find('parentcategoryname') else '') + r.find('categoryname').text)
          match['score'] = str(float(match['score']) + float(r.find('score').text))
      else: #add a new item
          defs.append({\
                  'term': r.find('term').text,\
                  'definition': r.find('definition').text,\
                  'categories': [((r.find('parentcategoryname').text + '\\') if r.find('parentcategoryname') else '') + r.find('categoryname').text],\
                  'score': r.find('score').text\
                  });

  for d in sorted(defs, key=lambda x:float(x['score']), reverse=True):
      #print d;
      acros.append(("%s: \"%s\" (%s, score: %s)" % \
              (d['term'], d['definition'], ', '.join(d['categories']), d['score'])\
              ).encode('ascii', 'ignore'))
  return acros
