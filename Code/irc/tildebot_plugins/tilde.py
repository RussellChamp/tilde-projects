#!/usr/bin/python3

import pinhook.plugin
import util.tilde

@pinhook.plugin.register('!tildescore')
def tildescore_plugin(msg):
    return pinhook.plugin.message(util.tilde.show_tildescore(msg.nick))

@pinhook.plugin.register('!jackpot')
def jackpot_plugin(msg):
    return pinhook.plugin.message(util.tilde.show_jackpot())

# ADMIN PLUGIN
@pinhook.plugin.register('!debug')
def debug_plugin(msg):
    if msg.nick not in msg.ops:
        return
    if msg.arg:
        util.tilde.DEBUG = (msg.arg.lower == 'true' or msg.arg.lower == 't')
    return pinhook.plugin.message("DEBUG set to '{}'".format(util.tilde.DEBUG))

# ADMIN PLUGIN
@pinhook.plugin.register('!tilde_requests')
def tilde_requests_plugin(msg):
    if msg.nick not in msg.ops and not util.tilde.DEBUG:
        return
    return pinhook.plugin.message("Outstanding requests: {}".format(",".join(util.tilde.challenges) if util.tilde.challenges else "(none)"))

@pinhook.plugin.register('!tilde')
def tilde_plugin(msg):
    if msg.channel != util.tilde.GOOD_CHAN and not util.tilde.DEBUG:
        return pinhook.plugin.message("{} is a meanie and gets no tildes. **Tildebot now only gives out tildes in the {} channel.**".format(msg.nick, util.tilde.GOOD_CHAN))
    if msg.nick not in util.tilde.challenges:
        return pinhook.plugin.message(util.tilde.challenge(msg.channel, msg.nick, msg.timestamp))

@pinhook.plugin.listener('tilde_guess')
def tilde_guess_plugin(msg):
    if msg.nick in util.tilde.challenges and (msg.channel == util.tilde.GOOD_CHAN or util.tilde.DEBUG):
        return pinhook.plugin.message(util.tilde.challenge_response(msg.nick, msg.timestamp, msg.text))

