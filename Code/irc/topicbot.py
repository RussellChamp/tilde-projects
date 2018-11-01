#!/usr/bin/python3
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
import fileinput
import random
import time
import argparse

import inflect
import util

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
    default="topicbot",
    help="the nick to use",
    metavar="NICK",
)

args = parser.parse_args()

p = inflect.engine()


def get_topic(channel, user, time):
    # topic scores are saved as <USER>&^%<GETS SCORE>&^%<SETS SCORE>
    with open("topicscores.txt", "r") as scorefile:
        scores = scorefile.readlines()
    userscore = 1
    found = False
    with open("topicscores.txt", "w") as scorefile:
        for idx, score in enumerate(scores):
            data = score.strip("\n").split("&^%")
            if data[0] == user:
                found = True
                userscore = int(data[1]) + 1
                scores[idx] = data[0] + "&^%" + str(userscore) + "&^%" + data[2] + "\n"
        scorefile.writelines(scores)
        if not found:
            scorefile.write(user + "&^%1&^%0\n")

    with open("topics_" + channel + ".txt", "r") as topics:
        topic = topics.readlines()[-1].strip("\n").split("&^%", 3)
        byuser = util.get_name(topic[1])
        util.sendmsg(
            ircsock,
            channel,
            "I've told you {} times! It's \"{}\" (set by {} {})".format(
                p.number_to_words(userscore),
                topic[2],
                byuser,
                util.pretty_date(int(topic[0])),
            ),
        )


def count_topic(channel, user, time, msg):
    with open("topics_" + channel + ".txt", "a") as topics:
        topics.write(time + "&^%" + user + "&^%" + msg + "\n")
    with open("topicscores.txt", "r") as scorefile:
        scores = scorefile.readlines()
    userscore = 1
    found = False
    with open("topicscores.txt", "w") as scorefile:
        for idx, score in enumerate(scores):
            data = score.strip("\n").split("&^%")
            if data[0] == user:
                found = True
                userscore = int(data[2]) + 1
                scores[idx] = data[0] + "&^%" + data[1] + "&^%" + str(userscore) + "\n"
        scorefile.writelines(scores)
        if not found:
            scorefile.write(user + "&^%0&^%1")
    util.sendmsg(
        ircsock,
        channel,
        "{} has changed the topic {} times!".format(user, p.number_to_words(userscore)),
    )


def set_topic(channel, user, time, msg):
    ircsock.send("TOPIC " + channel + " :" + msg + "\n")
    count_topic(channel, user, time, msg)


def random_topic(channel, user, time, setTopic=False):
    with open("randomtopics.txt") as rtopics:
        msg = random.choice(rtopics.readlines()).strip("\n")
        if setTopic:
            set_topic(channel, user, time, msg)
        else:
            util.sendmsg(ircsock, channel, "Suggested Topic: {}".format(msg))


def rollcall(channel):
    util.sendmsg(
        ircsock,
        channel,
        "topicbot reporting! I respond to !topic !settopic !suggesttopic !thistory",
    )


def topic_score(channel):
    util.sendmsg(ircsock, channel, "Not implemented yet")


def topic_scores(channel):
    util.sendmsg(ircsock, channel, "Not implemented yet")


def topic_history(channel, user, count):
    try:
        iCount = int(count.split()[1])
    except (ValueError, IndexError):
        iCount = 3
    if iCount > 10:
        iCount = 10
    if iCount < 1:
        iCount = 3
    with open("topics_" + channel + ".txt", "r") as topicsfile:
        # topics = topicsfile.readlines()[-iCount:].reverse()
        util.sendmsg(
            ircsock,
            channel,
            "Ok, here are the last {} topics".format(p.number_to_words(iCount)),
        )
        for idx, topic in enumerate(reversed(topicsfile.readlines()[-iCount:])):
            topic = topic.strip("\n").split("&^%", 3)
            byuser = util.get_name(topic[1])
            util.sendmsg(
                ircsock,
                channel,
                "{}: {} (set by {} {})".format(
                    str(idx + 1), topic[2], byuser, util.pretty_date(int(topic[0]))
                ),
            )


def listen():
    while 1:

        ircmsg = ircsock.recv(2048).decode("utf-8")
        ircmsg = ircmsg.strip("\n\r")

        if ircmsg[:4] == "PING":
            util.ping(ircsock, ircmsg)

        formatted = util.format_message(ircmsg)

        if "" == formatted:
            continue

        # print formatted

        msgtime, user, command, channel, messageText = formatted.split("\t")

        if command == "TOPIC" and user != args.nick:
            count_topic(channel, user, msgtime, messageText)

        if ircmsg.find(":!topic") != -1:
            get_topic(channel, user, msgtime)

        if ircmsg.find(":!settopic") != -1:
            set_topic(channel, user, msgtime, messageText[10:])

        if ircmsg.find(":!tscores") != -1:
            topic_scores(channel)
        elif ircmsg.find(":!tscores") != -1:
            topic_score(channel)

        if ircmsg.find(":!randomtopic") != -1:
            random_topic(channel, user, msgtime, True)
        if ircmsg.find(":!suggesttopic") != -1:
            random_topic(channel, user, msgtime, False)

        if ircmsg.find(":!thistory") != -1:
            topic_history(channel, user, messageText)

        if ircmsg.find(":!rollcall") != -1:
            rollcall(channel)

        sys.stdout.flush()
        time.sleep(1)


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
util.connect(ircsock, args)
listen()
