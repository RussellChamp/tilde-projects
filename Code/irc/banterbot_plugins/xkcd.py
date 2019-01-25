#!/usr/bin/python3

import pinhook.plugin
from util import xkcdApropos

@pinhook.plugin.register('!xkcd')
def xkcd_plugin(msg):
    return pinhook.plugin.message(xkcdApropos.xkcd(msg.arg))
