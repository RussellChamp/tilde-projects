#!/bin/bash

nohup ./wangbot.py -s 127.0.0.1 -n numberwang_bot -c \#bots >> wanglog 2>> wanglog &
#nohup ./wangbot.py -s 127.0.0.1 -n numberwang_bot -c \#bot_test >> wanglog 2>> wanglog &
