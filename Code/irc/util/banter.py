#!/usr/bin/python3

import random
import re

banter_file = "/home/krowbar/Code/irc/data/banterscores.txt"

def score_banter(nick, messageText):
    print(re)
    score = 5
    with open(banter_file, "r") as banterfile:
        bantz = banterfile.readlines()
        words = messageText.strip("\n").split(" ")
        for word in words:
            for bant in bantz:
                bword = bant.strip("\n").split("|")
                if re.sub("[^a-z0-9]+", "", word.lower()) == bword[0]:
                    score += int(bword[1])

    score += messageText.count("!") * 2  # hype is banter
    score -= messageText.count("!!!") * 6  # too much hype is not banter
    score += messageText.count("#") * 3  # hashs are mad bantz
    score -= messageText.count("##") * 6  # but too many is garbage

    names = ["mate", "lad", "my best boy"]
    compliment = [
        "top-drawer",
        "top-shelf",
        "bangin'",
        "legendary",
        "smashing",
        "incredible",
        "impeccable",
        "stunning",
    ]

    msg = ""
    if score > 100:
        msg = "Truely {}, {}! That was some #banter! You earned a {} for that!".format(
            random.choice(compliment).capitalize(), random.choice(names), score
        )
    elif score > 50:
        msg = "{} #banter! You get a {} from me!".format(
            random.choice(compliment).capitalize(), score
        )
    elif score > 10:
        msg = "{} #banter. You get a {}".format(
            random.choice(["acceptible", "reasonable", "passable"]).capitalize(), score
        )
    else:
        msg = "That {} #banter, {}. I'll give you a {}. Maybe try again?".format(
            random.choice(
                ["was hardly", "was barely", "wasn't", "won't pass for", "was awful"]
            ),
            random.choice(["lad", "lah", "boy", "son"]),
            score,
        )

    return msg

