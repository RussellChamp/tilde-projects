#!/usr/bin/python3

import pinhook.plugin
import subprocess

UNITS_CMD = "/home/krowbar/Code/units/units-2.11/units"
UNITS_CFG = "/home/krowbar/Code/units/units-2.11/definitions.units"

@pinhook.plugin.register('!units')
def units_plugin(msg):
    if not msg.arg:
        return pinhook.plugin.message("No text given. :(")
    else:
        result = subprocess.Popen(
            [UNITS_CMD, "-v1f", UNITS_CFG] + msg.arg.split(" "), shell=False, stdout=subprocess.PIPE
        ).stdout.read().decode("utf-8").strip()
    return pinhook.plugin.message(result)
