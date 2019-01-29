import random

evil_file = "/home/krowbar/logs/evildata.txt"

def get_thing():
    return "If I Ever Become an Evil Overlord: {}".format(random.choice(list(open(evil_file))).rstrip())
