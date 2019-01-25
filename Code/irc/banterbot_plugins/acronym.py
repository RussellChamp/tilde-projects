#!/usr/bin/python3

import pinhook.plugin
from util import acronymFinder

@pinhook.plugin.register('!acronym')
def acronym_plugin(msg):
    return pinhook.plugin.message(acronymFinder.get_acros(msg.arg, True, True))
