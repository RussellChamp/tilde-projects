#!/usr/bin/python
# http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

# Import some necessary libraries.
import socket
import os
import sys
from optparse import OptionParser

import get_users
import mentions
import formatter

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default='127.0.0.1',
                  help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default='#bot_test',
                  help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default='tilde_bot',
                  help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

def ping(pong):
  ircsock.send("PONG {}\n".format(pong))

def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def hello():
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

def tilde(channel, user, time):
  #h = os.popen("haiku").read().replace("\n", " // ")
  msg = time + ":" + user
  print msg
  ircsock.send("PRIVMSG "+ channel +" :" + msg + "\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n") # user authentication
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

    if ircmsg[:4] == "PING":
      ping(ircmsg.split(" ")[1])

    formatted = formatter.format_message(ircmsg)

    if "" == formatted:
      continue

    print formatted

    split = formatted.split("\t")
    time = split[0]
    user = split[1]
    messageText = split[2]

    if ircmsg.find(":!tilde") != -1:
      tilde(options.channel, user, time)

    if ircmsg[:4] == "PING":
      ping(ircmsg.split(" ")[1])

    sys.stdout.flush()

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
