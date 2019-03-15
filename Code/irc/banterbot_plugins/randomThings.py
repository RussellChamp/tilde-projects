#!/usr/bin/python3

import pinhook.plugin
from util import randomThings

@pinhook.plugin.register('!random')
def acronym_plugin(msg):
    return pinhook.plugin.message(randomThings.getRandom(msg.arg))
