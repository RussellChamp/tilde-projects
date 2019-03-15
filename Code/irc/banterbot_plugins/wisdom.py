#!/usr/bin/python3

import pinhook.plugin
import util.chopra

@pinhook.plugin.register('!wisdom')
def wisdom_plugin(msg):
    message = util.chopra.getWisdom()
    return pinhook.plugin.message(message)
