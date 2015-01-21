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
parser.add_option("-n", "--nick", dest="nick", default='tildebot',
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

def too_recent(time1, time2):
    if(int(time1) - int(time2) < 60*60):
        return True
    else:
        return False

def get_prize(user):
    if(random.randint(1,10) > 2):
        prizes = [1] * 8 + [2] * 4 + [3] * 2 + [5] * 1
        prize = random.choice(prizes)
        return [prize, user + " is " + ("super " if prize > 4 else "really " if prize > 2 else "") + "cool and gets " + p.number_to_words(prize) + " tildes!"]
    else:
        return [0, user + " is a meanie and gets no tildes!"]

def give_tilde(channel, user, time):
    found = False
    with open("tildescores.txt", "r+") as scorefile:
        scores = scorefile.readlines()
        scorefile.seek(0)
        scorefile.truncate()
        for score in scores:
            person = score.strip("\n").split("&^%")
            if(person[0] == user):
                found = True
                if(too_recent(time, person[2])):
                    ircsock.send("PRIVMSG " + channel + " :You have asked for a tilde too recently. Try again later.\n")
                else:
                    prize = get_prize(user)
                    score = person[0] + "&^%" + str(int(person[1]) + prize[0]) + "&^%" + time + "\n"
                    ircsock.send("PRIVMSG " + channel + " :" + prize[1] + "\n")
            scorefile.write(score)
        if(not found):
            prize = get_prize(user)
            ircsock.send("PRIVMSG " + channel + " :Welcome to the tilde game! Here's " + p.number_to_words(prize[0]+1) + " free tilde(s) to start you off.\n")
            scorefile.write(user + "&^%" + str(prize[0]+1) + "&^%" + time + "\n")

def show_tildescore(channel, user):
    with open("tildescores.txt", "r") as scorefile:
        for idx,score in enumerate(scorefile):
            person = score.strip("\n").split("&^%")
            if(person[0] == user):
                ircsock.send("PRIVMSG " + channel + " :" + user + " has " + p.number_to_words(person[1]) + " tildes!\n")
                return
        #person has not played yet
        ircsock.send("PRIVMSG " + channel + " :" + user + " has no tildes yet!\n")

def rollcall(channel):
  ircsock.send("PRIVMSG "+ channel +" :tildebot reporting! I respond to !tilde !tildescore\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :krowbar\n") # user authentication
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)

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

    if ircmsg.find(":!tildescore") != -1:
        show_tildescore(channel, user)
    elif ircmsg.find(":!tilde") != -1:
        give_tilde(channel, user, time)

    if ircmsg.find(":!rollcall") != -1:
      rollcall(channel)

    if ircmsg.find("PING :") != -1:
      ping()

    sys.stdout.flush()

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
