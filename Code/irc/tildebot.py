#!/usr/bin/python
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
import time
from optparse import OptionParser
import fileinput
import random

import formatter
import get_users
import mentions
import pretty_date
import inflect
import puzzle

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default='127.0.0.1',
                  help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default='#bot_test',
                  help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default='tildebot',
                  help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

p = inflect.engine()
challenges = {}
SCORE_FILE = "tildescores.txt"
JACKPOT_FILE = "tildejackpot.txt"
JACKPOT_MIN = 3
DEBUG = False

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

def get_prize(user, isHuman):
    if(random.randint(1,10) > 6 - 4 * isHuman): #80% of the time it's a normal prize (40% for not humans)
        prizes = [1] * 8 + [2] * 4 + [3] * 2 + [5] * isHuman #no 5pt prize for non-humans
        prize = random.choice(prizes)
        return [prize, user + ": " + (random.choice(['Yes','Yep','Correct','You got it']) if isHuman else random.choice(['No', 'Nope', 'Sorry', 'Wrong']))\
                + "! You are " + ("super " if prize > 4 else "really " if prize > 2 else "") + "cool and get " + p.number_to_words(prize) + " tildes!"]
    else: #20% of the time its a jackpot situation
        with open(JACKPOT_FILE, "r+") as jackpotfile:
            jackpot = int(jackpotfile.readline().strip("\n"))
            jackpotfile.seek(0)
            jackpotfile.truncate()
            if(random.randint(1,10) > 1 or not isHuman): #90% of the time it's a non-prize. non-humans never win jackpot
                new_jackpot = jackpot+1
                jackpotfile.write(str(new_jackpot)) #increase the jackpot by 1
                return [0, user + " is a meanie and gets no tildes! (Jackpot is now " + str(new_jackpot) + " tildes)"]
            else: #hit jackpot!
                jackpotfile.write(str(JACKPOT_MIN))
                return [jackpot, user + " hit the jackpot and won **" + p.number_to_words(jackpot) + " tildes!**"]

def show_jackpot(channel):
    with open(JACKPOT_FILE, "r") as jackpotfile:
        jackpot = int(jackpotfile.readline().strip("\n"))
        ircsock.send("PRiVMSG " + channel + " :The jackpot is currently " + p.number_to_words(jackpot) + " tildes!\n")

def give_tilde(channel, user, time, human):
    found = False
    with open(SCORE_FILE, "r+") as scorefile:
        scores = scorefile.readlines()
        scorefile.seek(0)
        scorefile.truncate()
        for score in scores:
            person = score.strip("\n").split("&^%")
            if(person[0] == user):
                found = True
                if(too_recent(time, person[2]) and not DEBUG):
                    ircsock.send("PRIVMSG " + channel + " :You have asked for a tilde too recently. Try again later.\n")
                else:
                    prize = get_prize(user, human)
                    score = person[0] + "&^%" + str(int(person[1]) + prize[0]) + "&^%" + time + "\n"
                    ircsock.send("PRIVMSG " + channel + " :" + prize[1] + "\n")
            scorefile.write(score)
        if(not found):
            prize = get_prize(user, True)
            ircsock.send("PRIVMSG " + channel + " :Welcome to the tilde game! Here's " + p.number_to_words(prize[0]+1) + " free tilde(s) to start you off.\n")
            scorefile.write(user + "&^%" + str(prize[0]+1) + "&^%" + time + "\n")

def show_tildescore(channel, user):
    with open(SCORE_FILE, "r") as scorefile:
        for idx,score in enumerate(scorefile):
            person = score.strip("\n").split("&^%")
            if(person[0] == user):
                ircsock.send("PRIVMSG " + channel + " :" + user + " has " + p.number_to_words(person[1]) + " tildes!\n")
                return
        #person has not played yet
        ircsock.send("PRIVMSG " + channel + " :" + user + " has no tildes yet!\n")

def challenge(channel, user, time):
    if(channel != "#bots" and not DEBUG):
        ircsock.send("PRIVMSG " + channel + " :" + user + " is a meanie and gets no tildes. **Tildebot now only gives out tildes in the #bots channel.**\n")
        return
    global challenges;
    challenge = puzzle.make_puzzle();
    challenges[user] = challenge[0]; #challenges[USER] = ANSWER
    ircsock.send("PRIVMSG " + channel + " :" + user + ": " + challenge[1] + "\n");

def challenge_response(channel, user, time, msg):
    global challenges
    print(msg);
    if(challenges.has_key(user)):
        if(msg == str(challenges[user]) or msg == p.number_to_words(challenges[user])):
            give_tilde(channel, user, time, True);
        else:
            give_tilde(channel, user, time, False);
        del challenges[user]; #delete the user from challenges either way



def rollcall(channel):
  ircsock.send("PRIVMSG "+ channel +" :tildebot reporting! I respond to !tilde !tildescore\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :krowbar\n") # user authentication
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)
  if(not DEBUG):
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
    iTime = split[0]
    user = split[1]
    command = split[2]
    channel = split[3]
    messageText = split[4]

    if ircmsg.find(":!tildescore") != -1:
        show_tildescore(channel, user)
    elif ircmsg.find(":!tilde") != -1 and not challenges.has_key(user):
        challenge(channel, user, iTime)
    elif challenges.has_key(user):
        challenge_response(channel, user, iTime, messageText)
        #give_tilde(channel, user, iTime)

    if ircmsg.find(":!jackpot") != -1:
        show_jackpot(channel)

    if ircmsg.find(":!rollcall") != -1:
      rollcall(channel)

    if ircmsg.find("PING :") != -1:
      ping()

    sys.stdout.flush()
    time.sleep(1)

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
