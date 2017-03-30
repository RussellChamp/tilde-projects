#!/usr/bin/python
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
from optparse import OptionParser
import fileinput
import random
import time
import re
import operator

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
parser.add_option("-n", "--nick", dest="nick", default='numberwang_bot',
                  help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

p = inflect.engine()
LIMIT_GUESSING = True
MIN_ROUNDS = 5
MAX_ROUNDS = 12
SCORE_FILE = "numberwangscores.txt"
SHOW_TOP_NUM = 5
GOOD_CHAN = "#bots"

roundsLeft = 0
bonusRound = 0
guesses = 0
lastGuesser = ""
currentScores = {}

def resetGlobals():
  global roundsLeft
  global bonusRound
  global guesses
  global lastGuesser
  global currentScores
  roundsLeft = 0
  bonusRound = 0
  guesses = 0
  lastGuesser = ""
  currentScores.clear()


def ping():
  ircsock.send("PONG :pingis\n")

def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def hello():
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

def start_numberwang(channel, user):
    if(channel != "#bots"):
        ircsock.send("PRIVMSG " + channel + " :Numberwang has been disabled for " + channel + " due to spamminess. Please join " + GOOD_CHAN + " to start a game.\n")
        return

    print user + " started a game"
    resetGlobals()
    ircsock.send("PRIVMSG " + channel + " :It's time for Numberwang!\n")
    time.sleep(1)
    ircsock.send("PRIVMSG " + channel + " :Here's how to play:\n")

    ircsock.send("PRIVMSG " + channel + " :1. There are 10 rounds\n")
    ircsock.send("PRIVMSG " + channel + " :2. Each round lasts 10 seconds. You're up against the clock!\n")
    ircsock.send("PRIVMSG " + channel + " :3. Play your numbers, as long as they're between 0 and 99.\n")
    ircsock.send("PRIVMSG " + channel + " :4. That's Numberwang!\n")
    time.sleep(2)
    ircsock.send("PRIVMSG " + channel + " :Let's get started!\n")
    global roundsLeft
    global bonusRound
    roundsLeft = random.randint(MIN_ROUNDS,MAX_ROUNDS)
    bonusRound = random.randint(2,roundsLeft-1)
    print "There will be " + str(roundsLeft) + " rounds with the bonus on round " + str(roundsLeft - bonusRound + 1)

def print_scores(channel):
    scoreStrs = []
    first = True
    for name in currentScores:
        scoreStrs.append(name + " is " + ("also " if not first and random.randint(1,3) == 3 else "") + "on " + str(currentScores[name]))
        first = False
    ircsock.send("PRIVMSG " + channel + " :" + p.join(scoreStrs) + "!\n")

def guess_numberwang(channel, user, messageText):
    global guesses
    global lastGuesser
    global currentScores
    global roundsLeft
    print user + " guessed '" + messageText + "'"
    guess = re.sub('[^0-9]','',messageText.split()[0]) #must have a number in the first 'word'
    if(guess):
        if(LIMIT_GUESSING and user == lastGuesser):
            ircsock.send("PRIVMSG " + channel + " :" + user + ", you just guessed! Give another player a try!\n")
        else:
            guesses += 1
            lastGuesser = user
            ###CORRECT GUESS###
            if(random.randint(0,10) > 10 - guesses): #the more guesses, the higher the probability
                guesses = 0
                lastGuesser = ""
                ircsock.send("PRIVMSG " + channel + " :" + user + ": THAT'S NUMBERWANG!\n")
                points = random.randint(2,10) * (random.randint(2,4) if roundsLeft == bonusRound else 1)
                if user in currentScores.keys():
                    currentScores[user] += points
                else:
                    currentScores[user] = points
                roundsLeft -= 1
                time.sleep(2)
                if(roundsLeft == 0):
                    ircsock.send("PRIVMSG " + channel + " :Numberwang is now over. Thank you for playing!\n")
                    ircsock.send("PRIVMSG " + channel + " :Final scores:\n")
                    print_scores(channel)
                    save_scores()
                else:
                    print_scores(channel)
                    newRoundStr = ""
                    if(roundsLeft == 1):
                        newRoundStr += "The last round is Wangernumb!"
                    elif(roundsLeft == bonusRound):
                        newRoundStr += "**Bonus Round!**"
                    else:
                        newRoundStr += "New Round!"
                    if(random.randint(1,10) > 8):
                        newRoundStr += " Let's rotate the board!"
                    ircsock.send("PRIVMSG " + channel + " :" + newRoundStr + " Start guessing!\n")


            ###INCORRECT GUESS###
            else:
                ircsock.send("PRIVMSG " + channel + " :" + random.choice(["Sorry", "I'm sorry", "No", "Nope"]) + ", " + user + ", " \
                        + random.choice(["that's not", "that is not", "that isn't", "that is not", "that won't make", "that will not make"])\
                        + " Numberwang!\n")

def stop_numberwang(channel, user):
    print user + " stopped a game"
    resetGlobals()
    ircsock.send("PRIVMSG " + channel + " :Numberwang has been stopped. No points have been awarded. " + user + " is such a party pooper!\n")

def save_scores():
    with open(SCORE_FILE, "r+") as scorefile:
        scores = scorefile.readlines()
        scorefile.seek(0)
        scorefile.truncate()
        for line in scores:
            for name in currentScores:
                score = line.strip("\n").split("&^%")
                if(score[0] == name):
                    line = score[0] + "&^%" + str(int(score[1]) + currentScores[name]) + "\n"
                    del currentScores[name]
                    break
            scorefile.write(line)

        for name in currentScores: #new wangers
            line = name + "&^%" + str(currentScores[name]) + "\n"
            scorefile.write(line)

def show_highscores(channel):
    with open(SCORE_FILE, "r") as scorefile:
        scores = []
        for line in scorefile.readlines():
            sline = line.strip("\n").split("&^%")
            scores.append((int(sline[1]), sline[0]))
        scores = sorted(scores, reverse=True)[:SHOW_TOP_NUM]

        ircsock.send("PRIVMSG " + channel + " :   ====TOP WANGERS====\n")
        for score in scores:
            ircsock.send("PRIVMSG " + channel + " :== ~" + score[1] + " (" + str(score[0]) + " points!) ==\n")


def show_user_score(channel, user):
    with open(SCORE_FILE, "r") as scorefile:
        for line in scorefile.readlines():
            score = line.strip("\n").split("&^%")
            if(user == score[0]):
                ircsock.send("PRIVMSG " + channel + " :" + user + ": Your global numberwang score is " + str(score[1]) + "!\n")
                return
        #if we don't find a score line
        ircsock.send("PRIVMSG " + channel + " :" + user + ": You haven't scored any points yet!\n")

def rollcall(channel):
  ircsock.send("PRIVMSG "+ channel +" :Is it time for Numberwang? It might be! Start a new game with !numberwang or stop a current game with !wangernumb Get your score with !myscore and the list of top wangers with !topwangers\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :krowbar\n") # user authentication
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)
  joinchan(GOOD_CHAN)

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

    if ircmsg.find(":!numberwang") != -1 and roundsLeft == 0:
        start_numberwang(channel, user)

    if channel == GOOD_CHAN:
        if ircmsg.find(":!wangernumb") != -1 and roundsLeft > 0:
            stop_numberwang(channel, user)
        if roundsLeft > 0:
            guess_numberwang(channel, user, messageText)

    if ircmsg.find(":!topwangers") != -1:
        show_highscores(channel)
    if ircmsg.find(":!myscore") != -1:
        show_user_score(channel, user)

    if ircmsg.find(":!rollcall") != -1:
      rollcall(channel)

    if ircmsg.find("PING :") != -1:
      ping()

    sys.stdout.flush()
    time.sleep(1)

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
