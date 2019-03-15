#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!botlist')
def rollcall_plugin(msg):
    text = "I am owned and run by {}".format(",".join(msg.ops))
    return pinhook.plugin.message(text)
