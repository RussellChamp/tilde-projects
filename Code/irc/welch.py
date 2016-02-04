import random

def get_thing():
    file = "/home/krowbar/logs/welchdata.txt"
    thing = ""
    return "Thing Mr. Welch can no longer do in a RPG #" + random.choice(list(open(file))).rstrip()
