#!/usr/bin/python
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
from optparse import OptionParser
import fileinput
import random
import re
import subprocess
import time
import datetime

import formatter
import get_users
import mentions
import pretty_date
import inflect
from rhymesWith import getRhymes
from rhymesWith import rhymeZone
from defineWord import defWord
from rainbow import makeRainbow
import welch
import evil
import tumblr
import xkcdApropos
import wikiphilosophy
import acronymFinder
import util
from whosaid import whoSaid

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default='127.0.0.1',
                  help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default='#bot_test',
                  help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default='tildebot',
                  help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

p = inflect.engine()

def ping(pong):
  ircsock.send("PONG {}\n".format(pong))

def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def hello():
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

def score_banter(channel, user, messageText):
    score = 5
    with open("banterscores.txt", "r") as banterfile:
        bantz = banterfile.readlines()
        words = messageText.strip("\n").split(" ")
        for word in words:
            for bant in bantz:
                bword = bant.strip("\n").split("|")
                if re.sub('[^a-z0-9]+','',word.lower()) == bword[0]:
                    score += int(bword[1])

    score += messageText.count('!') * 2   #hype is banter
    score -= messageText.count('!!!') * 6 #too much hype is not banter
    score += messageText.count('#') * 3   #hashs are mad bantz
    score -= messageText.count('##') * 6  #but too many is garbage

    names = ['mate', 'lad', 'my best boy']
    compliment = ['top-drawer', 'top-shelf', 'bangin\'', 'legendary', 'smashing', 'incredible', 'impeccable', 'stunning']

    msg = ""
    if score > 100:
        msg = "Truely " + random.choice(compliment).capitalize() + ", " + random.choice(names) \
                + "! That was some #banter! You earned a " + str(score) + " for that!"
    elif score > 50:
        msg = random.choice(compliment).capitalize() + " #banter! You get a " + str(score) + " from me!"
    elif score > 10:
        msg = random.choice(["acceptible", "reasonable", "passable"]).capitalize() + " #banter. You get a " + str(score)
    else:
        msg = "That " + random.choice(["was hardly", "was barely", "wasn't", "won't pass for", "was awful"]) \
                + " #banter" + random.choice([", lad",", lah",", boy","",""]) + ". I'll give you a " + str(score) + ". Maybe try again?"

    ircsock.send("PRIVMSG " + channel + " :" + msg + "\n")

def get_new_banter(channel, user):
    with open("/usr/share/dict/words", "r") as dict:
        words = filter(lambda word:re.search(r"^[^']*$", word), dict.readlines())
        if(random.randint(0,1)): #look for *ant words
            words = filter(lambda word:re.search(r"ant", word), words)
            random.shuffle(words)
            word = words[0].strip("\n")
            start = word.find('ant')
            if(start == 0):
                word = 'b' + word
            else:
                if('aeiou'.find(word[start]) > -1): #just append a 'b'
                    word = word[:start] + 'b' + word[start:]
                else: #replace the letter with 'b'
                    word = word[:start-1] + 'b' + word[start:]
        else: #look for ban* words
            words = filter(lambda word:re.search(r"ban", word), words)
            random.shuffle(words)
            word = words[0].strip("\n")
            end = word.find('ban') + 3
            if(end == len(word)):
                word = word + 't'
            else:
                if('aeiou'.find(word[end]) > -1): #just append 't'
                    word = word[:end] + 't' + word[end:]
                else: #replace the letter with 'b'
                    word = word[:end] + 't' + word[end+1:]
        ircsock.send("PRIVMSG " + channel + " :" + user + ": Here, why don't you try '" + word + "'?\n")

def get_rhymes(channel, user, text):
    word = ""
    if(len(text.split(' ')) > 1):
        word = text.split(' ')[1]
    else:
        with open("/home/nossidge/poems/words_poetic.txt", "r") as words:
            word = random.choice(words.readlines()).strip("\n")
    rhymes = rhymeZone(word)
    if(len(rhymes) == 0):
        ircsock.send("PRIVMSG " + channel + " :" + user + ": Couldn't find anything that rhymes with '" + word + "' :(\n")
    else:
        ircsock.send("PRIVMSG " + channel + " :" + user + ": Here, these words rhyme with '" + word + "': " + ', '.join(rhymes) + "\n")

def define_word(channel, user, text):
    word = ""
    defs = []
    if(len(text.split(' ')) > 1):
        word = text.split(' ')[1]
        defs = defWord(word)
    if(len(defs) == 0):
        ircsock.send("PRIVMSG " + channel + " :" + user + ": Couldn't find the definition of '" + word + "' :(\n")
    elif(isinstance(defs, list)):
        for entry in defs:
          ircsock.send("PRIVMSG " + channel + " :" + user + ": Define '" + word + "'" + entry[0:400] + "\n")
    else:
        ircsock.send("PRIVMSG " + channel + " :" + user + ": Define '" + word + "'" + defs[0:400] + "\n")

def make_rainbow(channel, user, text):
    rbword = makeRainbow(text[9:])
    ircsock.send("PRIVMSG " + channel + " :" + rbword + "\n")

def get_welch(channel):
    ircsock.send("PRIVMSG " + channel + " :" + welch.get_thing()[0:400] + "\n")

def get_evil(channel):
    evilThing = evil.get_thing()
    for line in [evilThing[i:i+400] for i in range(0, len(evilThing), 400)]:
         ircsock.send("PRIVMSG " + channel + " :" + line + "\n")

def get_tumble(url, channel):
    tumble = tumblr.tumble(url)
    for line in [tumble[i:i+400] for i in range(0, len(tumble), 400)]:
        ircsock.send("PRIVMSG " + channel + " :" + line + "\n")

def get_xkcd(channel, text):
    links = xkcdApropos.xkcd(text[6:])
    joined_links = ', '.join(links)
    for line in [joined_links[i:i+400] for i in range(0, len(joined_links), 400)]:
        ircsock.send("PRIVMSG " + channel + " :" + line + "\n")
    #res = xkcdApropos.xkcd(text[6:])
    #ircsock.send("PRIVMSG " + channel + " :" + res + "\n")

def get_wphilosophy(channel, text):
  steps = wikiphilosophy.get_philosophy_lower(text[17:])
  if not steps:
    ircsock.send("PRIVMSG " + channel + " :Couldn't find a wikipedia entry for " + text + "\n")
  else:
    joined_steps = ' > '.join(steps)
    if steps[-1] == 'Philosophy':
      joined_steps += "!!!"
    for line in [joined_steps[i:i+400] for i in range(0, len(joined_steps), 400)]:
      ircsock.send("PRIVMSG " + channel + " :" + line + "\n")

def figlet(channel, text):
    if not text:
        ircsock.send("PRIVMSG " + channel + " :No text given. :(\n")
    else:
        lines = subprocess.Popen(["figlet", "-w140"] + text.split(' '), shell=False, stdout=subprocess.PIPE).stdout.read()
        for line in lines.split('\n'):
            ircsock.send("PRIVMSG " + channel + " :" + line + "\n")
            time.sleep(0.4) #to avoid channel throttle due to spamming

def toilet(channel, text):
    if not text:
        ircsock.send("PRIVMSG " + channel + " :No text given. :(\n")
    else:
        lines = subprocess.Popen(["toilet", "-w140", "--irc"] + text.split(' '), shell=False, stdout=subprocess.PIPE).stdout.read()
        for line in lines.split('\n'):
            ircsock.send("PRIVMSG " + channel + " :" + line + "\n")
            time.sleep(0.4) #to avoid channel throttle due to spamming

def get_acronym(channel, text):
  if not text:
    ircsock.send("PRIVMSG " + channel + " :No text given :(\n")
  else:
    defs = acronymFinder.get_acros(text, True, True)
    for d in defs[0:5]: #only the first five. they are already sorted by 'score'
      ircsock.send("PRIVMSG " + channel + " :" + d.encode('utf-8') + "\n")
    if len(defs) > 5:
      ircsock.send("PRIVMSG " + channel + " :" + defs[-1] + "\n")

def get_whosaid(channel, text):
  if not text:
    ircsock.send("PRIVMSG " + channel + " :No text given :(\n")
  else:
    result = whoSaid(text)
    date = datetime.date.fromtimestamp(result['timecutoff'])
    dateStr = date.strftime('%B %d')
    if not result['data']:
      msg = 'Nobody said \'%s\' since %s' % (text, dateStr)
    else:
      msg = 'Since %s, %s said \'%s\' %d times' % (dateStr, result['data'][0][0], text, result['data'][0][1])
      if len(result['data']) > 1:
        msg += ' and %s said it %d times' % (result['data'][1][0], result['data'][1][1])
    ircsock.send("PRIVMSG " + channel + " :" + msg + ".\n")

def get_notice(user, channel):
    ircsock.send("CNOTICE " + user + " " + channel + " :Notice me sempai!\n")

def get_water(user, channel, msg, botnick):
    if msg.find(botnick) == 0:
        ircsock.send("PRIVMSG " + channel + " :Fight me, " + user + "!\n")

def mug_off(channel):
    ircsock.send("PRIVMSG " + channel + " :u want some of this, m8?\n")

def rollcall(channel):
  ircsock.send("PRIVMSG "+ channel +" :U wot m8? I score all the top drawer #banter and #bantz on this channel! \
          Find new top-shelf banter with !newbanter, !rhymes, and !define. \
          Look up things with !acronym and !whosaid. \
          Make your chatter #legend with !rainbow, !toilet, and !figlet. \
          Find interesting things with !xkcd and !wiki-philosophy. \
          Get jokes with !welch and !evil\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :krowbar\n") # user authentication
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)
  joinchan("#bots")

def get_user_from_message(msg):
  try:
    i1 = msg.index(':') + 1
    i2 = msg.index('!')
    return msg[i1:i2]
  except ValueError:
    return ""

def listen(botnick):
  while 1:

    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip('\n\r')

    if ircmsg[:4] == "PING":
      ping(ircmsg.split(" ")[1])

    formatted = util.format_message(ircmsg)

    if "" == formatted:
      continue

    # print formatted

    split = formatted.split("\t")
    #time = split[0]
    user = split[1]
    command = split[2]
    channel = split[3]
    messageText = split[4]

    if ircmsg.find("#banter") != -1 or ircmsg.find("#bantz") != -1:
        score_banter(channel, user, messageText)

    if ircmsg.find(":!newbanter") != -1:
        get_new_banter(channel, user)

    if ircmsg.find(":!rhymes") != -1:
        get_rhymes(channel, user, messageText)

    if ircmsg.find(":!define") != -1:
        define_word(channel, user, messageText)

    if ircmsg.find(":!rainbow") != -1:
        make_rainbow(channel, user, messageText)

    if ircmsg.find(":!welch") != -1:
        get_welch(channel)

    if ircmsg.find(":!evil") != -1:
        get_evil(channel)

    if ircmsg.find(":!kjp") != -1:
        get_tumble('http://kingjamesprogramming.tumblr.com', channel)

    if ircmsg.find(":!help") != -1:
        get_tumble('http://thedoomthatcametopuppet.tumblr.com', channel)

    if ircmsg.find(":!xkcd") != -1:
        get_xkcd(channel, messageText)
    if ircmsg.find(":!wiki-philosophy") != -1:
        get_wphilosophy(channel, messageText);

    if ircmsg.find(":!figlet") != -1:
        figlet(channel, messageText[8:])

    if ircmsg.find(":!toilet") != -1:
        toilet(channel, messageText[8:])

    if ircmsg.find(":!acronym") != -1:
        get_acronym(channel, messageText[9:])

    if ircmsg.find(":!whosaid") != -1:
        get_whosaid(channel, messageText[9:])

    if ircmsg.find(":!notice") != -1:
        get_notice(user, channel)

    if ircmsg.find(":!water") != -1:
        get_water(user, channel, messageText[7:], botnick)


    if ircmsg.find(":!rollcall") != -1:
      rollcall(channel)

    if ircmsg.find(":" + botnick + ":") != -1:
        mug_off(channel)

    if ircmsg[:4] == "PING":
      ping(ircmsg.split(" ")[1])

    sys.stdout.flush()
    time.sleep(1)

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen(options.nick)
