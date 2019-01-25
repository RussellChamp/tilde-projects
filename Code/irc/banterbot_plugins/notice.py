#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!notice')
def notice_plugin(msg):
    msg.notice(msg.nick, "Notice me senpai!")
