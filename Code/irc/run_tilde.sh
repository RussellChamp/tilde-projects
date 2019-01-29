#!/bin/bash
# check if the bot is already running
if [[ ! `pidof -sx bot_launcher.py` || ! `ps -p $(pidof -sx bot_launcher.py) -o args | grep "\-n tildebot"` ]]; then
  echo "Starting tildebot"
  /home/krowbar/Code/irc/bot_launcher.py -n tildebot -s 127.0.0.1 -p 6667 -c \#bots
  # nohup /home/krowbar/Code/irc/bot_launcher.py -n tildebot -s 127.0.0.1:6667 -c \#bot_test
else
  echo "Tildebot has already been started"
fi
