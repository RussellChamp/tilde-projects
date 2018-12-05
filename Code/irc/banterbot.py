#!/usr/bin/python3
# using python3 because of unicode and crap
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import argparse
import socket
import os
import sys
import fileinput
import random
import re
import subprocess
import textwrap
import time
import datetime

import inflect
from rhymesWith import getRhymes
from rhymesWith import rhymeZone
from defineWord import defWord
import welch
import evil
import tumblr
import xkcdApropos
import wikiphilosophy
import acronymFinder
import util
from whosaid import whoSaid

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s",
    "--server",
    dest="server",
    default="127.0.0.1:6667",
    help="the server to connect to",
    metavar="SERVER",
)
parser.add_argument(
    "-c",
    "--channels",
    dest="channels",
    nargs="+",
    default=["#bot_test"],
    help="the channels to join",
    metavar="CHANNELS",
)
parser.add_argument(
    "-n",
    "--nick",
    dest="nick",
    default="banterbot",
    help="the nick to use",
    metavar="NICK",
)
parser.add_argument(
    "-o",
    "--owner",
    dest="owner",
    default="krowbar",
    help="the owner of this bot",
    metavar="OWNER",
)

args = parser.parse_args()

p = inflect.engine()

def hello():
    util.sendmsg(ircsoc, channel, "Hello!")


def score_banter(channel, user, messageText):
    score = 5
    with open("banterscores.txt", "r") as banterfile:
        bantz = banterfile.readlines()
        words = messageText.strip("\n").split(" ")
        for word in words:
            for bant in bantz:
                bword = bant.strip("\n").split("|")
                if re.sub("[^a-z0-9]+", "", word.lower()) == bword[0]:
                    score += int(bword[1])

    score += messageText.count("!") * 2  # hype is banter
    score -= messageText.count("!!!") * 6  # too much hype is not banter
    score += messageText.count("#") * 3  # hashs are mad bantz
    score -= messageText.count("##") * 6  # but too many is garbage

    names = ["mate", "lad", "my best boy"]
    compliment = [
        "top-drawer",
        "top-shelf",
        "bangin'",
        "legendary",
        "smashing",
        "incredible",
        "impeccable",
        "stunning",
    ]

    msg = ""
    if score > 100:
        msg = "Truely {}, {}! That was some #banter! You earned a {} for that!".format(
            random.choice(compliment).capitalize(), random.choice(names), score
        )
    elif score > 50:
        msg = "{} #banter! You get a {} from me!".format(
            random.choice(compliment).capitalize(), score
        )
    elif score > 10:
        msg = "{} #banter. You get a {}".format(
            random.choice(["acceptible", "reasonable", "passable"]).capitalize(), score
        )
    else:
        msg = "That {} #banter, {}. I'll give you a {}. Maybe try again?".format(
            random.choice(
                ["was hardly", "was barely", "wasn't", "won't pass for", "was awful"]
            ),
            random.choice(["lad", "lah", "boy", ""]),
            score,
        )

    util.sendmsg(ircsock, channel, msg)


def get_new_banter(channel, user):
    with open("/usr/share/dict/words", "r") as dict:
        words = list(filter(lambda word: re.search(r"^[^']*$", word), dict.readlines()))
        if random.randint(0, 1):  # look for *ant words
            words = list(filter(lambda word: re.search(r"ant", word), words))
            random.shuffle(words)
            word = words[0].strip("\n")
            start = word.find("ant")
            if start == 0:
                word = "b" + word
            else:
                if "aeiou".find(word[start]) > -1:  # just append a 'b'
                    word = word[:start] + "b" + word[start:]
                else:  # replace the letter with 'b'
                    word = word[: start - 1] + "b" + word[start:]
        else:  # look for ban* words
            words = list(filter(lambda word: re.search(r"ban", word), words))
            random.shuffle(words)
            word = words[0].strip("\n")
            end = word.find("ban") + 3
            if end == len(word):
                word = word + "t"
            else:
                if "aeiou".find(word[end]) > -1:  # just append 't'
                    word = word[:end] + "t" + word[end:]
                else:  # replace the letter with 'b'
                    word = word[:end] + "t" + word[end + 1 :]
        util.sendmsg(
            ircsock, channel, "{} : Here, why don't you try '{}'?".format(user, word)
        )


def get_rhymes(channel, user, text):
    word = ""
    if len(text.split(" ")) > 1:
        word = text.split(" ")[1]
    else:
        with open("/home/nossidge/poems/words_poetic.txt", "r") as words:
            word = random.choice(words.readlines()).strip("\n")
    rhymes = rhymeZone(word)
    if len(rhymes) == 0:
        util.sendmsg(
            ircsock,
            channel,
            "{}: Couldn't find anything that rhymes with '{}' :(".format(user, word),
        )
    else:
        util.sendmsg(
            ircsock,
            channel,
            "{}: Here, these words rhyme with '{}': {}".format(
                user, word, ", ".join(rhymes)
            ),
        )


def define_word(channel, user, text):
    word = ""
    defs = []
    if len(text.split(" ")) > 1:
        word = text.split(" ")[1]
        defs = defWord(word)
    if len(defs) == 0:
        util.sendmsg(
            ircsock,
            channel,
            "{}: Couldn't find the definition of '{}' :(".format(user, word),
        )
    elif isinstance(defs, list):
        for entry in defs:
            util.sendmsg(
                ircsock, channel, "{} : Define '{}' {}".format(user, word, entry[0:400])
            )
    else:
        util.sendmsg(
            ircsock, channel, "{} : Define '{}' {}".format(user, word, defs[0:400])
        )


def make_rainbow(channel, user, text):
    rbword = util.makeRainbow(text[9:])
    util.sendmsg(ircsock, channel, rbword)


def get_welch(channel):
    util.sendmsg(ircsock, channel, welch.get_thing()[0:400])


def get_evil(channel):
    evilThing = evil.get_thing()
    for line in [evilThing[i : i + 400] for i in range(0, len(evilThing), 400)]:
        util.sendmsg(ircsock, channel, line)


def get_tumble(url, channel):
    tumble = tumblr.tumble(url)
    for line in [tumble[i : i + 400] for i in range(0, len(tumble), 400)]:
        util.sendmsg(ircsock, channel, line)


def get_xkcd(channel, text):
    links = xkcdApropos.xkcd(text[6:])
    joined_links = ", ".join(links)
    for line in [joined_links[i : i + 400] for i in range(0, len(joined_links), 400)]:
        util.sendmsg(ircsock, channel, line)


def get_wphilosophy(channel, text):
    util.sendmsg(ircsock, channel, "Ok, give me a minute while I look up '{}'".format(text))
    steps = wikiphilosophy.get_philosophy_lower(text)
    if not steps:
        util.sendmsg(
            ircsock, channel, "Couldn't find a wikipedia entry for {}".format(text)
        )
    else:
        joined_steps = " > ".join(steps)
        if steps[-1] == "Philosophy":
            joined_steps += "!!!"
        for line in [
            joined_steps[i : i + 400] for i in range(0, len(joined_steps), 400)
        ]:
            util.sendmsg(ircsock, channel, line)


def figlet(channel, text):
    if not text:
        util.sendmsg(ircsock, channel, "No text given. :(")
    else:
        lines = subprocess.Popen(
            ["figlet", "-w140"] + text.split(" "), shell=False, stdout=subprocess.PIPE
        ).stdout.read().decode("utf-8")
        for line in lines.split("\n"):
            util.sendmsg(ircsock, channel, line)
            time.sleep(0.4)  # to avoid channel throttle due to spamming


def toilet(channel, text):
    if not text:
        util.sendmsg(ircsock, channel, "No text given. :(")
    else:
        lines = subprocess.Popen(
            ["toilet", "-w140", "--irc"] + text.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
        ).stdout.read().decode("utf-8")
        for line in lines.split("\n"):
            util.sendmsg(ircsock, channel, line)
            time.sleep(0.4)  # to avoid channel throttle due to spamming


def get_acronym(channel, text):
    if not text:
        util.sendmsg(ircsock, channel, "No text given :(")
    else:
        defs = acronymFinder.get_acros(text, True, True)
        for d in defs[0:5]:  # only the first five. they are already sorted by 'score'
            util.sendmsg(ircsock, channel, d)
        if len(defs) > 5:
            util.sendmsg(ircsock, channel, defs[-1])


def get_whosaid(channel, text):
    if not text:
        util.sendmsg(ircsock, channel, " :No text given :(")
    else:
        result = whoSaid(text)
        date = datetime.date.fromtimestamp(result["timecutoff"])
        dateStr = date.strftime("%B %d")
        if not result["data"]:
            msg = "Nobody said '%s' since %s" % (text, dateStr)
        else:
            msg = "Since %s, %s said '%s' %d times" % (
                dateStr,
                result["data"][0][0],
                text,
                result["data"][0][1],
            )
            if len(result["data"]) > 1:
                msg += " and %s said it %d times" % (
                    result["data"][1][0],
                    result["data"][1][1],
                )
        util.sendmsg(ircsock, channel, msg)


def get_notice(user, channel):
    util.notice(ircsock, user, channel, "Notice me senpai!")


def get_water(user, channel, msg, botnick):
    if msg.find(botnick) == 0:
        util.sendmsg(ircsock, channel, "Fight me, {}!".format(user))


def mug_off(channel):
    util.sendmsg(ircsock, channel, "u want some of this, m8?")


def rollcall(channel):
    text = """
        U wot m8? I score all the top drawer #banter and #bantz on this channel! / Find new top-shelf banter with !newbanter, !rhymes, and !define.
        Look up things with !acronym and !whosaid / Make your chatter #legend with !rainbow, !toilet, and !figlet.
        Find interesting things with !xkcd and !wiki-philosophy / Get jokes with !welch !evil !kjp and !help
    """
    for line in textwrap.dedent(text).split("\n"):
        if line == "":
            continue
        util.sendmsg(ircsock, channel, line)


def listen(botnick):
    while 1: # loop forever

        ircmsg = ircsock.recv(2048).decode('utf-8')
        for msg in ircmsg.split("\n"):
            msg = msg.strip("\n\r")

            if msg[:4] == "PING":
                util.ping(ircsock, msg)
                continue

            formatted = util.format_message(msg)

            if "" == formatted:
                continue

            print(formatted)

            _time, user, _command, channel, messageText = formatted.split("\t")

            if messageText.find("#banter") != -1 or messageText.find("#bantz") != -1:
                score_banter(channel, user, messageText)

            if messageText.startswith("!newbanter"):
                get_new_banter(channel, user)

            if messageText.startswith("!rhymes"):
                get_rhymes(channel, user, messageText)

            if messageText.startswith("!define"):
                define_word(channel, user, messageText)

            if messageText.startswith("!rainbow"):
                make_rainbow(channel, user, messageText)

            if messageText.startswith("!welch"):
                get_welch(channel)

            if messageText.startswith("!evil"):
                get_evil(channel)

            if messageText.startswith("!kjp"):
                get_tumble("http://kingjamesprogramming.tumblr.com", channel)

            if messageText.startswith("!help"):
                get_tumble("http://thedoomthatcametopuppet.tumblr.com", channel)

            if messageText.startswith("!xkcd"):
                get_xkcd(channel, messageText)

            if messageText.startswith("!wiki-philosophy"):
                get_wphilosophy(channel, messageText[17:])

            if messageText.startswith("!figlet"):
                figlet(channel, messageText[8:])

            if messageText.startswith("!toilet"):
                toilet(channel, messageText[8:])

            if messageText.startswith("!acronym"):
                get_acronym(channel, messageText[9:])

            if messageText.startswith("!whosaid"):
                get_whosaid(channel, messageText[9:])

            if messageText.startswith("!notice"):
                get_notice(user, channel)

            if messageText.startswith("!water"):
                get_water(user, channel, messageText[7:], botnick)

            if messageText.startswith("!rollcall"):
                rollcall(channel)

            if messageText.startswith(botnick + ":"):
                mug_off(channel)

            if messageText.startswith("!join") and user == args.owner:
                util.joinchan(ircsock, messageText[6:])

            if messageText.startswith("!part") and user == args.owner:
                util.part(ircsock, messageText[6:])

            if messageText.startswith("!quit") and user == args.owner:
                util.quit(ircsock, "Later chumps!")
                return

        sys.stdout.flush()
        time.sleep(1)


# ROOT: i commented this out until it stops pegging the CPU.
# ~krowbar: this has the same logic loop as tildebot but for whatever reason
# it is banterbot that gets booted from IRC then rage-thrashes the machine
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
util.connect(ircsock, args)
listen(args.nick)
