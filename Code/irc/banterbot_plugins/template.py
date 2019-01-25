#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!')
def _plugin(msg):
    return pinhook.plugin.message()
