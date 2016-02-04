import random

def get_thing():
    file = "/home/krowbar/logs/evildata.txt"
    thing = ""
    return "If I Ever Become an Evil Overlord: " + random.choice(list(open(file))).rstrip()
