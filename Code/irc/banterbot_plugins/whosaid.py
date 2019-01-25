#!/usr/bin/python3

import pinhook.plugin
from util import whoSaid

@pinhook.plugin.register('!whosaid')
def whosaid_plugin(msg):
    return pinhook.plugin.message(whoSaid.whoSaid(msg.arg))
