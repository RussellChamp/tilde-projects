#!/usr/bin/python3

import pinhook.plugin
from util import wikiphilosophy

@pinhook.plugin.register('!wphilosophy')
def wiki_philosophy_plugin(msg):
    msg.privmsg(msg.channel, "Ok, give me a minute while I look up '{}'".format(msg.arg))

    steps = wikiphilosophy.get_philosophy_lower(msg.arg)
    if not steps:
        return pinhook.plugin.message("Couldn't find a wikipedia entry for {}".format(msg.arg))
    else:
        joined_steps = " > ".join(steps)
        if steps[-1] == "Philosophy":
            joined_steps += "!!!"
        for line in [ joined_steps[i : i + 400] for i in range(0, len(joined_steps), 400) ]:
            msg.privmsg(msg.channel, line)
