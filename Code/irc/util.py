import time
import re


def ping(pong):
    ircsock.send("PONG {}\n".format(pong.split(" ")[1]))


def sendmsg(ircsock, chan, msg):
    ircsock.send("PRIVMSG {} :{}\r\n".format(chan, msg))


def joinchan(ircsock, chan):
    ircsock.send("JOIN {}\n".format(chan))


# integer number to english word conversion
# can be used for numbers as large as 999 vigintillion
# (vigintillion --> 10 to the power 60)
# tested with Python24      vegaseat      07dec2006
def int2word(n):
    """
    convert an integer number n into a string of english words
    """
    # break the number into groups of 3 digits using slicing
    # each group representing hundred, thousand, million, billion, ...
    n3 = []
    r1 = ""
    # create numeric string
    ns = str(n)
    for k in range(3, 33, 3):
        r = ns[-k:]
        q = len(ns) - k
        # break if end of ns has been reached
        if q < -2:
            break
        else:
            if q >= 0:
                n3.append(int(r[:3]))
            elif q >= -1:
                n3.append(int(r[:2]))
            elif q >= -2:
                n3.append(int(r[:1]))
        r1 = r

    # print n3  # test

    # break each group of 3 digits into
    # ones, tens/twenties, hundreds
    # and form a string
    nw = ""
    for i, x in enumerate(n3):
        b1 = x % 10
        b2 = (x % 100) // 10
        b3 = (x % 1000) // 100
        # print b1, b2, b3  # test
        if x == 0:
            continue  # skip
        else:
            t = thousands[i]
        if b2 == 0:
            nw = ones[b1] + t + nw
        elif b2 == 1:
            nw = tens[b1] + t + nw
        elif b2 > 1:
            nw = twenties[b2] + ones[b1] + t + nw
        if b3 > 0:
            nw = ones[b3] + "hundred " + nw
    return nw


############# globals ################
ones = [
    "",
    "one ",
    "two ",
    "three ",
    "four ",
    "five ",
    "six ",
    "seven ",
    "eight ",
    "nine ",
]
tens = [
    "ten ",
    "eleven ",
    "twelve ",
    "thirteen ",
    "fourteen ",
    "fifteen ",
    "sixteen ",
    "seventeen ",
    "eighteen ",
    "nineteen ",
]
twenties = [
    "",
    "",
    "twenty ",
    "thirty ",
    "forty ",
    "fifty ",
    "sixty ",
    "seventy ",
    "eighty ",
    "ninety ",
]
thousands = [
    "",
    "thousand ",
    "million ",
    "billion ",
    "trillion ",
    "quadrillion ",
    "quintillion ",
    "sextillion ",
    "septillion ",
    "octillion ",
    "nonillion ",
    "decillion ",
    "undecillion ",
    "duodecillion ",
    "tredecillion ",
    "quattuordecillion ",
    "sexdecillion ",
    "septendecillion ",
    "octodecillion ",
    "novemdecillion ",
    "vigintillion ",
]


def format_message(message):
    pattern = r"^:.*\!~(.*)@.* (.*) (.*) :(.*)"
    now = int(time.time())
    matches = re.match(pattern, message)
    if not matches:
        return ""

    nick = matches.group(1).strip()
    command = matches.group(2).strip()
    channel = matches.group(3).strip()
    message = matches.group(4).strip()

    return "%s\t%s\t%s\t%s\t%s" % (now, nick, command, channel, message)


def get_users():
    # thanks, ~dan!
    users = []
    with open("/etc/passwd", "r") as f:
        for line in f:
            if "/bin/bash" in line:
                u = line.split(":")[0]  # Grab all text before first ':'
                users.append(u)

    return users


def pretty_date(time=False):
    """
  Get a datetime object or a int() Epoch timestamp and return a
  pretty string like 'an hour ago', 'Yesterday', '3 months ago',
  'just now', etc
  """
    from datetime import datetime

    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ""

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"
