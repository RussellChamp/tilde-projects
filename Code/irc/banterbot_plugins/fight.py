#!/usr/bin/python3

import pinhook.plugin
import time

@pinhook.plugin.listener('fight')
def fight_plugin(msg):
    if msg.botnick + ": " in msg.text:
        return pinhook.plugin.message("u want some of this, m8?")

@pinhook.plugin.listener('action')
def action_plugin(msg):
    if msg.botnick in msg.text and hasattr(msg, 'event') and msg.event is "action":
        time.sleep(1)
        msg.action(msg.channel, msg.text.replace(msg.botnick, msg.nick) + " back")
