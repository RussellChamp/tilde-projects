#!/usr/bin/python3

import pinhook.plugin
from util import welch

@pinhook.plugin.register('!welch')
def welch_plugin(msg):
    return pinhook.plugin.message(welch.get_thing())
