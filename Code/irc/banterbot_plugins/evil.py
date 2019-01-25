#!/usr/bin/python3

import pinhook.plugin
from util import evil

@pinhook.plugin.register('!evil')
def evil_plugin(msg):
    return pinhook.plugin.message(evil.get_thing())
