#!/bin/bash
# check if the bot is already running
if [[ ! `pidof -sx bot_launcher.py` || ! `ps -p $(pidof -sx bot_launcher.py) -o args | grep "\-n banterbot"` ]]; then
  echo "Starting banterbot"
  /home/krowbar/Code/irc/bot_launcher.py -n banterbot -s 127.0.0.1 -p 6667 -c \#tildetown \#bots
  # nohup /home/krowbar/Code/irc/bot_launcher.py -n banterbot -s 127.0.0.1:6667 -c \#bot_test
else
  echo "Banterbot has already been started"
fi
