#!/usr/bin/python3

import pinhook.plugin
import subprocess
import time

@pinhook.plugin.register('!toilet')
def toilet_plugin(msg):
    if not msg.arg:
        return pinhook.plugin.message("No text given. :(")
    else:
        lines = subprocess.Popen(
            ["toilet", "-w140", "-F", "crop", "--irc"] + msg.arg.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
        ).stdout.read().decode("utf-8")
        for line in lines.split("\n"):
            msg.privmsg(msg.channel, line)
            time.sleep(0.4)  # to avoid channel throttle due to spamming
