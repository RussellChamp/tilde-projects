#!/usr/bin/python3

import pinhook.plugin
from util import banter

@pinhook.plugin.listener('banter')
def banter_plugin(msg):
    if "#banter" in msg.text.lower() or "#bantz" in msg.text.lower():
        message = banter.score_banter(msg.nick, msg.text)
        return pinhook.plugin.message(message)
