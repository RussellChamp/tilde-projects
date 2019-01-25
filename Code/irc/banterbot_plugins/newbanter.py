#!/usr/bin/python3

import pinhook.plugin
from util import newBanter

@pinhook.plugin.register('!newbanter')
def newbanter_plugin(msg):
    try:
        args = msg.arg.split()
        banter = newBanter.getBanter(*args)
        if banter == "":
            text = "{}: Could not find any new banter".format(msg.nick)
            if len(args) >= 1:
                text += " using munge word '{}'. Try something else?".format(args[0])
            return pinhook.plugin.message(text)
        else:
            return pinhook.plugin.message("{}: Here, why don't you try '{}'?".format(msg.nick, banter))

    except FileNotFoundError as e: # this happens if you attempt to search a word dict that doesn't exist
        text = "{}: Could not find word dictionary".format(msg.nick)
        if len(args) >= 2:
            text += " '{}'. Maybe try another one?".format(args[1])
        return pinhook.plugin.message(text)
