#!/usr/bin/python
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
from optparse import OptionParser

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
    default="#tildetown",
    help="the channel to join",
    metavar="CHANNEL",
)
parser.add_option(
    "-n",
    "--nick",
    dest="nick",
    default="quotebot",
    help="the nick to use",
    metavar="NICK",
)

(options, args) = parser.parse_args()


def random_quote(channel):
    quote = os.popen("/home/frs/quotes/randquote.py").read()
    if len(quote) >= 256:
        quote = quote[:253] + "..."
    util.sendmsg(ircsock, channel, quote)


def haiku(channel):
    h = os.popen("haiku").read().replace("\n", " // ")
    util.sendmsg(ircsock, channel, h)


def say_mentions(user, message):
    nick = util.get_user_from_message(message)
    menschns = (
        os.popen("/home/karlen/bin/mensch -u {} -t 24 -z +0".format(user))
        .read()
        .replace("\t", ": ")
        .split("\n")
    )
    for mention in menschns:
        if not "" == mention:
            toSend = "PRIVMSG " + nick + " :" + mention + "\n"
            if len(toSend) >= 256:
                toSend = toSend[:253] + "..."
            ircsock.send(toSend)


def say_chatty(channel):
    chattyOut = os.popen("/home/karlen/bin/chatty").read().split("\n")
    for line in chattyOut:
        if line:
            util.sendmsg(ircsock, channel, line)


def listen():
    while 1:

        ircmsg = ircsock.recv(2048).decode()
        ircmsg = ircmsg.strip("\r\n")

        formatted = util.format_message(ircmsg)

        if "" == formatted:
            continue

        print(formatted)

        user = formatted.split("\t")[1]

        if ircmsg.find(":!quote") != -1:
            random_quote(options.channel)

        if ircmsg.find(":!mentions") != -1:
            say_mentions(user, ircmsg)

        if ircmsg.find(":!chatty") != -1:
            say_chatty(options.channel)

        if ircmsg.find(":!haiku") != -1:
            haiku(options.channel)

        if ircmsg[:4] == "PING":
            util.ping(ircsock, ircmsg)

        sys.stdout.flush()
        # time.sleep(1)


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
util.connect(ircsock, options)
listen()
