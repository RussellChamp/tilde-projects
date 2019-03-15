#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!help2')
def help_plugin(msg):
    # just a placeholder to overload the built-in !help function
    if msg.nick in msg.ops:
        return pinhook.plugin.message("!help has been disabled")
