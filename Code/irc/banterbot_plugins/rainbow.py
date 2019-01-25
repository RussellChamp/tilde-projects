#!/usr/bin/python3

import pinhook.plugin
import random

@pinhook.plugin.register('!rainbow')
def rainbow_plugin(msg):
    word = msg.arg or "RAINBOW"
    output = ""
    rb = ["5", "7", "8", "3", "12", "13", "6"]
    bg = "01"
    idx = random.randrange(0, len(rb))

    for l in word:
        if l == " ":
            output += " "
        else:
            output += "\x03" + rb[idx % len(rb)] + "," + bg + l
            idx += 1

    return pinhook.plugin.message(output)
