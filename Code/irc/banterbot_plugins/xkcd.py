#!/usr/bin/python3

import pinhook.plugin
import util.xkcdApropos

@pinhook.plugin.register('!xkcd')
def xkcd_plugin(msg):
    return pinhook.plugin.message(util.xkcdApropos.xkcd(msg.arg))
