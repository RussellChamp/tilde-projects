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
import names
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

def get_positive():
    return random.choice(['Yes', 'Yep', 'Yeppers', 'Correct','You got it', 'Yeah', 'Right on', 'Uh-huh', 'Positive', 'Totally right', 'Close enough', 'That\'s it'])

def get_negative():
    return random.choice(['No', 'Nope', 'Sorry', 'Wrong', 'Nuh-uh', 'Negatory', 'Incorrect', 'Not today', 'Try again', 'Maybe later', 'Probably not', 'Answer hazy', 'Not quite',\
                'Not even close'])

def get_superlative(score):
    if score > 4:
        return random.choice(["super cool", "totally rad", "extraordinary", "dynomite", "#topdrawer", "a #TopLad", "the cat's meow", "a tilde town hero", "my favorite person", "incredibly lucky",\
                "unbelievable", "a tilde town hunk", "could bring all the boys to the yard", "worth twice their weight in gold", "the hero we need", "no ordinary townie"]);
    elif score > 2:
        return random.choice(["really cool", "pretty neat", "rather nice", "a dynamic doggo", "radical", "intense", "pretty lucky", "knows the territory", "has what it takes", "has mad skillz",\
                "going the distance", "a hard worker", "my sunshine", "ready to rumble"]);
    else:
        return random.choice(["cool", "nice", "acceptible", "good enough", "a promising pupper", "better than a horse", "swell", "a little lucky", "just credible", "my friend", "probably not a robot",\
                "valuable to the team"]);

def get_bad_thing():
    return random.choice(["is a meanie", "mugs me right off", "is worse than a horse", "smells like a ghost", "probably didn't bathe today", "didn't guess hard enough", "isn't lucky",\
            "smells of elderberries", "should reconsider their life choices", "did't believe in the heart of the tilde", "came to the wrong chat channel", "should have stopped while they were ahead",\
            "requires annotations from an authoratative source", "could have been a contender", "spreads vicious rumors", "drank my milkshake", "is probably cheating", "is trying too hard"]);

def get_prize(name, isHuman, bonus=0):
    prizes = [1] * 8 + [2] * 4 + [3] * 2 + [5] * isHuman #no 5pt prize for non-humans
    prize = random.choice(prizes) + bonus
    if(random.randint(1,10) > 6 - 4 * isHuman): #80% of the time it's a normal prize (40% for not humans)
        return [prize, name + ": " + (get_positive() if isHuman else get_negative()) + "! You are " + get_superlative(prize) + " and get " + p.number_to_words(prize) + " tildes!"]
    else: #20% of the time its a jackpot situation
        with open(JACKPOT_FILE, "r+") as jackpotfile:
            jackpot = int(jackpotfile.readline().strip("\n"))
            jackpotfile.seek(0)
            jackpotfile.truncate()
            if(random.randint(1,10) > 1 or not isHuman): #90% of the time it's a non-prize. non-humans never win jackpot
                new_jackpot = jackpot+max(1,prize)
                jackpotfile.write(str(new_jackpot)) #increase the jackpot by the prize size
                return [0, name + " " + get_bad_thing() + " and gets no tildes! (Jackpot is now " + str(new_jackpot) + " tildes)"]
            else: #hit jackpot!
                jackpotfile.write(str(JACKPOT_MIN))
                return [jackpot, name + " hit the jackpot and won **" + p.number_to_words(jackpot) + " tildes!**"]

def show_jackpot(channel):
    with open(JACKPOT_FILE, "r") as jackpotfile:
        jackpot = int(jackpotfile.readline().strip("\n"))
        ircsock.send("PRiVMSG " + channel + " :The jackpot is currently " + p.number_to_words(jackpot) + " tildes!\n")

def give_tilde(channel, user, name, time, human, bonus=0):
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
                    ircsock.send("PRIVMSG " + channel + " :" + name + " asked for a tilde too recently and " + get_bad_thing() + ". Try again later.\n")
                else:
                    prize = get_prize(name, human, bonus)
                    score = person[0] + "&^%" + str(int(person[1]) + prize[0]) + "&^%" + time + "\n"
                    ircsock.send("PRIVMSG " + channel + " :" + prize[1] + "\n")
            scorefile.write(score)
        if(not found):
            prize = get_prize(name, True, bonus)
            ircsock.send("PRIVMSG " + channel + " :Welcome to the tilde game! Here's " + p.number_to_words(prize[0]+1) + " free tilde(s) to start you off.\n")
            scorefile.write(user + "&^%" + str(prize[0]+1) + "&^%" + time + "\n")

def show_tildescore(channel, user, name):
    with open(SCORE_FILE, "r") as scorefile:
        for idx,score in enumerate(scorefile):
            person = score.strip("\n").split("&^%")
            if(person[0] == user):
                ircsock.send("PRIVMSG " + channel + " :" + name + " has " + p.number_to_words(person[1]) + " tildes!\n")
                return
        #person has not played yet
        ircsock.send("PRIVMSG " + channel + " :" + name + " has no tildes yet!\n")

def challenge(channel, user, name, time):
    if(channel != "#bots" and not DEBUG):
        ircsock.send("PRIVMSG " + channel + " :" + name + " is a meanie and gets no tildes. **Tildebot now only gives out tildes in the #bots channel.**\n")
        return
    global challenges;
    challenge = puzzle.make_puzzle();
    challenges[user] = challenge[0]; #challenges[USER] = ANSWER
    ircsock.send("PRIVMSG " + channel + " :" + name + ": " + challenge[1] + "\n");

def challenge_response(channel, user, name, time, msg):
    global challenges
    print(msg);
    if(challenges.has_key(user)):
        bonus = 1 if str(challenges[user]).find(',') != -1 else 0 #give a bonus for prime factoring
        if(msg.lower() == str(challenges[user]).lower() or msg == p.number_to_words(challenges[user])):
            give_tilde(channel, user, name, time, True, bonus);
        else:
            give_tilde(channel, user, name, time, False, 0);
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
    for msg in ircmsg.split('\n'):
      msg = msg.strip('\n\r')

      if msg.find("PING :") != -1:
        ping()

      formatted = formatter.format_message(msg)

      if "" == formatted:
        continue

    # print formatted

      split = formatted.split("\t")
      iTime = split[0]
      user = split[1]
      name = names.get_name(user)
      command = split[2]
      channel = split[3]
      messageText = split[4]

      if msg.find(":!tildescore") != -1:
        show_tildescore(channel, user, name)
      elif msg.find(":!tilde") != -1 and not challenges.has_key(user):
        challenge(channel, user, name, iTime)
      elif challenges.has_key(user):
        challenge_response(channel, user, name, iTime, messageText)
        #give_tilde(channel, user, name, iTime)

      if msg.find(":!jackpot") != -1:
        show_jackpot(channel)

      if msg.find(":!rollcall") != -1:
        rollcall(channel)

      if msg.find("PING :") != -1:
        ping()

  sys.stdout.flush()
  time.sleep(1)

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
