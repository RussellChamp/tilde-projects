#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.listener('fight')
def fight_plugin(msg):
    if msg.botnick + ": " in msg.text:
        return pinhook.plugin.message("u want some of this, m8?")
