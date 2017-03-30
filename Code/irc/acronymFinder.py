import urllib
from bs4 import BeautifulSoup
import random
import string

dict = '/usr/share/dict/american-english'
(userId,token) = open("/home/krowbar/.secret/s4token").readline().rstrip().split(',')

def get_acros(word, silly, short):
  acros = []
  url = "http://www.stands4.com/services/v2/abbr.php?uid=%s&tokenid=%s&term=%s" % (userId, token, word)
  soup = BeautifulSoup(urllib.urlopen(url).read(), 'html5lib')
  results = soup.find_all('result')
  #there are lots of cases where the same definition is repeated multiple times under different categories. this is dumb so we should do a little more work
  defs = []
  for r in results:
      rdef = r.find('definition').text
      match = next((x for x in defs if x['definition'].lower() == rdef.lower()), None)
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
      if short is True:
        acros.append("\"%s\"" % d['definition'])
      else:
        acros.append(("%s: \"%s\" (%s, score: %s)" % \
              (d['term'], d['definition'], ', '.join(d['categories']), d['score'])\
              ).encode('ascii', 'ignore'))
  if silly is True:
      newDef = []
      words = open(dict, 'r').readlines()
      try:
          for idx,letter in enumerate(word):
              newWord = random.choice(\
                      filter(lambda w: (idx is 0 or not w.strip().lower().endswith('\'s'))\
                      and w.lower().startswith(letter.lower()), words)\
                      ).strip()
              print str(idx) + ' -> ' + newWord
              newDef.append(newWord)
          newWord = string.capwords(' '.join(newDef))
          if short is True:
            acros.append("\"%s\"" % newWord)
          else:
            acros.append(("%s: \"%s\" (%s, score: %s)" % \
                  (word.upper(), newWord, 'Tilde.town Original', '0')\
                  ).encode('ascii', 'ignore'))
      except IndexError:
          acros.append("Future hazy, try again later: Tilde.town Error");
  if short is True:
    shortList = acros[0:5]
    if len(acros) > 5:
      shortList.append(acros[-1])
    return [word.upper() + ': ' + ', '.join(shortList)]
  else:
    return acros
