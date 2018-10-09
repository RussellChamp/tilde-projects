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

import inflect
import util

parser = OptionParser()

parser.add_option(
    "-s",
    "--server",
    dest="server",
    default="127.0.0.1:6667",
    help="the server to connect to",
    metavar="SERVER",
)
parser.add_option(
    "-c",
    "--channel",
    dest="channel",
    default="#bot_test",
    help="the channel to join",
    metavar="CHANNEL",
)
parser.add_option(
    "-n",
    "--nick",
    dest="nick",
    default="wangbot",
    help="the nick to use",
    metavar="NICK",
)

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


def start_numberwang(channel, user):
    if channel != "#bots":
        util.sendmsg(
            ircsock,
            channel,
            "Numberwang has been disabled in {} due to spamminess. Please join {} to start a game.".format(
                channel, GOOD_CHAN
            ),
        )
        return

    print(user + " started a game")
    resetGlobals()
    util.sendmsg(ircsock, channel, "It's time for Numberwang!")
    time.sleep(1)
    util.sendmsg(ircsock, channel, "Here's how to play:")

    util.sendmsg(ircsock, channel, "1. There are 10 rounds")
    util.sendmsg(
        ircsock, channel, "2. Each round lasts 10 seconds. You're up against the clock!"
    )
    util.sendmsg(
        ircsock, channel, "3. Play your numbers, as long as they're between 0 and 99."
    )
    util.sendmsg(ircsock, channel, "4. That's Numberwang!")
    time.sleep(2)
    util.sendmsg(ircsock, channel, "Let's get started!")
    global roundsLeft
    global bonusRound
    roundsLeft = random.randint(MIN_ROUNDS, MAX_ROUNDS)
    bonusRound = random.randint(2, roundsLeft - 1)
    print(
        "There will be {} rounds with the bonus on round {}".format(
            str(roundsLeft), str(roundsLeft - bonusRound + 1)
        )
    )


def print_scores(channel):
    scoreStrs = []
    first = True
    for name in currentScores:
        scoreStrs.append(
            "{} is {} on {}".format(
                name,
                ("also " if not first and random.randint(1, 3) == 3 else ""),
                currentScores[name],
            )
        )
        first = False
    util.sendmsg(ircsock, channel, p.join(scoreStrs))


def guess_numberwang(channel, user, messageText):
    global guesses
    global lastGuesser
    global currentScores
    global roundsLeft
    print(user + " guessed '" + messageText + "'")
    guess = re.sub(
        "[^0-9]", "", messageText.split()[0]
    )  # must have a number in the first 'word'
    if guess:
        if LIMIT_GUESSING and user == lastGuesser:
            util.sendmsg(
                ircsock,
                channel,
                "{}, you just guessed! Give another player a try!".format(user),
            )
        else:
            guesses += 1
            lastGuesser = user
            ###CORRECT GUESS###
            if (
                random.randint(0, 10) > 10 - guesses
            ):  # the more guesses, the higher the probability
                guesses = 0
                lastGuesser = ""
                util.sendmsg(ircsock, channel, "{}: THAT'S NUMBERWANG!".format(user))
                points = random.randint(2, 10) * (
                    random.randint(2, 4) if roundsLeft == bonusRound else 1
                )
                if user in currentScores.keys():
                    currentScores[user] += points
                else:
                    currentScores[user] = points
                roundsLeft -= 1
                time.sleep(2)
                if roundsLeft == 0:
                    util.sendmsg(
                        ircsock,
                        channel,
                        "Numberwang is now over. Thank you for playing!",
                    )
                    util.sendmsg(ircsock, channel, "Final scores:")
                    print_scores(channel)
                    save_scores()
                else:
                    print_scores(channel)
                    newRoundStr = ""
                    if roundsLeft == 1:
                        newRoundStr += "The last round is Wangernumb!"
                    elif roundsLeft == bonusRound:
                        newRoundStr += "**Bonus Round!**"
                    else:
                        newRoundStr += "New Round!"
                    if random.randint(1, 10) > 8:
                        newRoundStr += " Let's rotate the board!"
                    util.sendmsg(
                        ircsock, channel, "{} Start guessing!".format(newRoundStr)
                    )

            ###INCORRECT GUESS###
            else:
                util.sendmsg(
                    ircsock,
                    channel,
                    "{}, {}, {} Numberwang!".format(
                        random.choice(["Sorry", "I'm sorry", "No", "Nope"]),
                        user,
                        random.choice(
                            [
                                "that's not",
                                "that is not",
                                "that isn't",
                                "that is not",
                                "that won't make",
                                "that will not make",
                            ]
                        ),
                    ),
                )


def stop_numberwang(channel, user):
    print(user + " stopped a game")
    resetGlobals()
    util.sendmsg(
        ircsock,
        channel,
        "Numberwang has been stopped. No points have been awarded. {} is such a party pooper!".format(
            user
        ),
    )


def save_scores():
    with open(SCORE_FILE, "r+") as scorefile:
        scores = scorefile.readlines()
        scorefile.seek(0)
        scorefile.truncate()
        for line in scores:
            for name in currentScores:
                score = line.strip("\n").split("&^%")
                if score[0] == name:
                    line = "{}&^%{}\n".format(
                        score[0], int(score[1]) + currentScores[name]
                    )
                    del currentScores[name]
                    break
            scorefile.write(line)

        for name in currentScores:  # new wangers
            scorefile.write("{}&^%{}\n".format(name, currentScores[name]))


def show_highscores(channel):
    with open(SCORE_FILE, "r") as scorefile:
        scores = []
        for line in scorefile.readlines():
            sline = line.strip("\n").split("&^%")
            scores.append((int(sline[1]), sline[0]))
        scores = sorted(scores, reverse=True)[:SHOW_TOP_NUM]

        util.sendmsg(ircsock, channel, "====TOP WANGERS====")
        for score in scores:
            util.sendmsg(
                ircsock, channel, " :== ~{} ({} points!) ==".format(score[1], score[0])
            )


def show_user_score(channel, user):
    with open(SCORE_FILE, "r") as scorefile:
        for line in scorefile.readlines():
            score = line.strip("\n").split("&^%")
            if user == score[0]:
                util.sendmsg(
                    ircsock,
                    channel,
                    "{}: Your global numberwang score is {}!".format(user, score[1]),
                )
                return
        # if we don't find a score line
        util.sendmsg(
            ircsock, channel, "{} You haven't scored any points yet!".format(user)
        )


def rollcall(channel):
    util.sendmsg(
        ircsock,
        channel,
        "Is it time for Numberwang? It might be! Start a new game with !numberwang or stop a current game with !wangernumb Get your score with !myscore and the list of top wangers with !topwangers",
    )


def listen():
    while 1:

        ircmsg = ircsock.recv(2048).decode()
        ircmsg = ircmsg.strip("\n\r")

        if ircmsg[:4] == "PING":
            util.ping(ircsock, ircmsg)

        formatted = util.format_message(ircmsg)

        if "" == formatted:
            continue

        # print formatted

        _time, user, _command, channel, messageText = formatted.split("\t")

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

        sys.stdout.flush()
        time.sleep(1)


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
util.connect(ircsock, options)
listen()
