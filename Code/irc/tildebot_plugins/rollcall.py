#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!rollcall')
def rollcall_plugin(msg):
    return pinhook.plugin.message("tildebot reporting! I respond to !tilde !tildescore")
