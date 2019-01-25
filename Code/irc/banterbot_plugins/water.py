#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!water')
def water_plugin(msg):
    if msg.botnick in msg.arg:
        return pinhook.plugin.message("Fight me, {}!".format(msg.nick))
