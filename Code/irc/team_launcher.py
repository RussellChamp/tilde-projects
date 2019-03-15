#!/usr/bin/python3

# This is a generic launcher that acts as a chasis for various bots
# I would recomend creating a separate script that can be invoked
# directly for each bot you run

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
    "--owners",
    dest="owners",
    nargs="+",
    default=["krowbar"],
    help="the owners of this bot",
    metavar="OWNERS",
)

args = parser.parse_args()
print(args)

bot = Bot(
        channels = args.channels,
        nickname = args.nick,
        ops = args.owners,
        plugin_dir = "{}_plugins".format(args.nick),
        server = args.server,
        port = args.port
        )

if __name__ == "__main__":
    bot.start()
