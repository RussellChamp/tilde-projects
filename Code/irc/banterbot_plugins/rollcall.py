#!/usr/bin/python3

import pinhook.plugin

@pinhook.plugin.register('!rollcall')
def rollcall_plugin(msg):
    text = "U wot m8? I score all the top drawer #banter and #bantz on this channel! / Find new top-shelf banter with !newbanter [mungeWord [dictionary]], !rhymes, and !define."
    text += "\nLook up things with !acronym and !whosaid / Make your chatter #legend with !rainbow, !toilet, and !figlet."
    text += "\nFind interesting things with !xkcd and !wiki-philosophy / Get jokes with !welch !evil !kjp and !help"
    return pinhook.plugin.message(text)
