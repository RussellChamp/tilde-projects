#!/usr/bin/python3

import argparse
from pinhook.bot import Bot

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s",
    "--server",
    dest="server",
    default="127.0.0.1",
    help="the server to connect to",
    metavar="SERVER",
)
parser.add_argument(
    "-p",
    "--port",
    dest="port",
    type=int,
    default=6667,
    help="the port to connect to",
    metavar="PORT",
)
parser.add_argument(
    "-c",
    "--channels",
    dest="channels",
    nargs="+",
    default=["#bot_test"],
    help="the channels to join",
    metavar="CHANNELS",
)
parser.add_argument(
    "-n",
    "--nick",
    dest="nick",
    default="banterbot",
    help="the nick to use",
    metavar="NICK",
)
parser.add_argument(
    "-o",
    "--owner",
    dest="owner",
    default="krowbar",
    help="the owner of this bot",
    metavar="OWNER",
)

args = parser.parse_args()
print(args)

bot = Bot(
        channels = args.channels,
        nickname = args.nick,
        ops = [ args.owner ],
        plugin_dir = "{}_plugins".format(args.nick),
        server = args.server,
        port = args.port
        )

if __name__ == "__main__":
    bot.start()
