#!/usr/bin/python3

import pinhook.plugin
from util import defineWord

@pinhook.plugin.register('!define')
def define_plugin(msg):
    if not msg.arg:
        return pinhook.plugin.message("{}: No word given".format(msg.nick))

    word = msg.arg.split()[0]
    defs = defineWord.defWord(word)

    if not defs:
        return pinhook.plugin.message("{}: Couldn't find the definition of '{}' :(".format(msg.nick, word))
    elif isinstance(defs, list):
        return pinhook.plugin.message("\n".join(["{} : Define '{}' {}".format(msg.nick, word, entry) for entry in defs]))
    else:
        return pinhook.plugin.message("{} : Define '{}' {}".format(msg.nick, word, defs))
