#!/usr/bin/python3

import pinhook.plugin
from util import tumblr

@pinhook.plugin.register('!kjp')
def kjp_plugin(msg):
    return pinhook.plugin.message(tumblr.tumble("http://kingjamesprogramming.tumblr.com"))

@pinhook.plugin.register('!help')
def help_plugin(msg):
    return pinhook.plugin.message(tumblr.tumble("http://thedoomthatcametopuppet.tumblr.com"))
