#!/usr/bin/python3

import pinhook.plugin
import time
from util import numberwang

@pinhook.plugin.register('!rollcall')
def rollcall_plugin(msg):
    return pinhook.plugin.message("Is it time for Numberwang? It might be! Start a new game with !numberwang or stop a current game with !wangernumb Get your score with !myscore and the list of top wangers with !topwangers")

# the numberwang lib returns message lists that may contain numbers.
# if we get one of those, sleep for that long
def print_messages(msg, messages):
    for line in messages:
        if isinstance(line, int) or isinstance(line, float):
            time.sleep(line)
        else:
            msg.privmsg(msg.channel, line)

@pinhook.plugin.register('!numberwang')
def numberwang_plugin(msg):
    if numberwang.roundsLeft == 0:
        print_messages(msg, numberwang.start_numberwang(msg.channel, msg.nick))

@pinhook.plugin.register('!wangernumb')
def wangernumb_plugin(msg):
    if numberwang.roundsLeft > 0:
        print_messages(msg, numberwang.stop_numberwang(msg.nick))

@pinhook.plugin.register('!topwangers')
def top_plugin(msg):
    print_messages(msg, numberwang.show_highscores())

@pinhook.plugin.register('!myscore')
def my_score_plugin(msg):
    print_messages(msg, numberwang.show_user_score(msg.nick))

@pinhook.plugin.listener('numberwang')
def numberwang_listener(msg):
    if msg.text.split()[0] in ['!numberwang', '!wangernumb', '!topwangers', '!myscore'] or numberwang.roundsLeft is 0 or msg.channel != numberwang.GOOD_CHAN:
        return

    print_messages(msg, numberwang.guess_numberwang(msg.channel, msg.user, msg.arg))
