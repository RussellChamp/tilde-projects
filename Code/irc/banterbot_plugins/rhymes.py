#!/usr/bin/python3

import pinhook.plugin
from util import rhymesWith

poetic_file = "/home/nossidge/poems/words_poetic.txt"

@pinhook.plugin.register('!rhymes')
def rhymes_plugin(msg):
    word = ""
    if msg.arg == "":
        with open(poetic_file, "r") as words:
            word = random.choice(words.readlines()).strip("\n")
    else:
        word = msg.arg.split()[0]

    rhymes = rhymesWith.rhymeZone(word)
    if len(rhymes) == 0:
        return pinhook.plugin.message("{}: Couldn't find anything that rhymes with '{}' :(".format(msg.nick, word))
    else:
        return pinhook.plugin.message("{}: Here, these words rhyme with '{}': {}".format(msg.nick, word, ", ".join(rhymes)))
