#!/usr/bin/python3

import pinhook.plugin
import util.fightCrime

@pinhook.plugin.register('!crime')
def crime_plugin(msg):
    message = util.fightCrime.getDuo()
    return pinhook.plugin.message(message)
