#!/usr/bin/python
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
from optparse import OptionParser
import fileinput
import random

import formatter
import get_users
import mentions
import pretty_date
import inflect

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default='127.0.0.1',
                  help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default='#bot_test',
                  help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default='topicbot',
                  help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

p = inflect.engine()

def ping():
  ircsock.send("PONG :pingis\n")

def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def hello():
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

def get_topic(channel, user, time):
  #topic scores are saved as <USER>&^%<GETS SCORE>&^%<SETS SCORE>
  with open("topicscores.txt", "r") as scorefile:
    scores = scorefile.readlines()
  userscore = 1
  found = False
  with open("topicscores.txt", "w") as scorefile:
    for idx,score in enumerate(scores):
      data = score.strip("\n").split("&^%")
      if(data[0] == user):
        found = True
        userscore = int(data[1])+1
        scores[idx] = data[0] + "&^%" + str(userscore) + "&^%" + data[2] + "\n"
    scorefile.writelines(scores)
    if(not found):
      scorefile.write(user + "&^%1&^%0\n")


  with open("topics_" + channel + ".txt", "r") as topics:
    topic = topics.readlines()[-1].strip("\n").split("&^%", 3)
    ircsock.send("PRIVMSG "+ channel +" :I've told you " + p.number_to_words(userscore) + " times! It's \"" + topic[2] + "\" (Set by " + topic[1] + " " + pretty_date.pretty_date(int(topic[0])) + ")\n")

def count_topic(channel, user, time, msg):
  with open("topics_" + channel + ".txt", "a") as topics:
      topics.write(time + "&^%" + user + "&^%" + msg + "\n")
  with open("topicscores.txt", "r") as scorefile:
    scores = scorefile.readlines()
  userscore = 1
  found = False
  with open("topicscores.txt", "w") as scorefile:
    for idx,score in enumerate(scores):
      data = score.strip("\n").split("&^%")
      if(data[0] == user):
        found = True
        userscore = int(data[2])+1
        scores[idx] = data[0] + "&^%" + data[1] + "&^%" + str(userscore) + "\n"
    scorefile.writelines(scores)
    if(not found):
      scorefile.write(user + "&^%0&^%1")
  ircsock.send("PRIVMSG "+ channel +" :" + user + " has changed the topic " + p.number_to_words(userscore) + " times!\n")

def set_topic(channel, user, time, msg):
  ircsock.send("TOPIC "+ channel +" :" + msg + "\n")
  count_topic(channel, user, time, msg)

def random_topic(channel, user, time, setTopic=false):
    with open("randomtopics.txt") as rtopics:
      msg = random.choice(rtopics.readlines()).strip("\n")
      if(setTopic):
          set_topic(channel, user, time, msg)
      else:
          ircsock.send("TOPIC "+ channel +" :Suggested Topic: " + msg + "\n")

def rollcall(channel):
  ircsock.send("PRIVMSG "+ channel +" :topicbot reporting! I respond to !topic !settopic !randomtopic !thistory\n")

def topic_score(channel):
    ircsock.send("PRIVMSG "+ channel +" :Not implemented yet")

def topic_scores(channel):
    ircsock.send("PRIVMSG "+ channel +" :Not implemented yet")

def topic_history(channel, user, count):
  try:
    iCount = int(count.split()[1])
  except (ValueError, IndexError) as e:
    iCount = 3
  if(iCount > 10):
    iCount = 10
  if(iCount < 1):
    iCount = 3
  with open("topics_" + channel + ".txt", "r") as topicsfile:
    #topics = topicsfile.readlines()[-iCount:].reverse()
    ircsock.send("PRIVMSG "+ channel +" :Ok, here were the last " + p.number_to_words(iCount) + " topics\n")
    for idx,topic in enumerate(reversed(topicsfile.readlines()[-iCount:])):
      topic = topic.strip("\n").split("&^%", 3)
      ircsock.send("PRIVMSG "+ channel +" :" + str(idx+1) + ": \"" + topic[2] + "\" (Set by " + topic[1] + " " + pretty_date.pretty_date(int(topic[0])) + ")\n")


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

def listen():
  while 1:

    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip('\n\r')

    if ircmsg.find("PING :") != -1:
      ping()

    formatted = formatter.format_message(ircmsg)

    if "" == formatted:
      continue

    # print formatted

    split = formatted.split("\t")
    time = split[0]
    user = split[1]
    command = split[2]
    channel = split[3]
    messageText = split[4]

    if(command == "TOPIC" and user != options.nick):
      count_topic(channel,user, time, messageText)

    if ircmsg.find(":!topic") != -1:
      get_topic(channel, user, time)

    if ircmsg.find(":!settopic") != -1:
      set_topic(channel, user, time, messageText[10:])

    if ircmsg.find(":!tscores") != -1:
      topic_scores(channel)
    elif ircmsg.find(":!tscores") != -1:
      topic_score(channel)

    if ircmsg.find(":!randomtopic") != -1:
      random_topic(channel, user, time, True)
    if ircmsg.find(":!suggesttopic") != -1:
      random_topic(channel,user,time, False)

    if ircmsg.find(":!thistory") != -1:
      topic_history(channel, user, messageText)

    if ircmsg.find(":!rollcall") != -1:
      rollcall(channel)

    if ircmsg.find("PING :") != -1:
      ping()

    sys.stdout.flush()

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
