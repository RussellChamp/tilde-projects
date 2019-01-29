#!/usr/bin/python3

import inflect
import random

scores_file = "/home/krowbar/Code/irc/data/topicscores.txt"
channel_topics = "/home/krowbar/Code/irc/data/topics_{}.txt"
random_topics = "/home/krowbar/Code/irc/data/randomtopics.txt"

p = inflect.engine()

def get_topic(channel, user, time):
    # topic scores are saved as <USER>&^%<GETS SCORE>&^%<SETS SCORE>
    with open(scores_file, "r") as scorefile:
        scores = scorefile.readlines()
    userscore = 1
    found = False
    with open(scores_file, "w") as scorefile:
        for idx, score in enumerate(scores):
            data = score.strip("\n").split("&^%")
            if data[0] == user:
                found = True
                userscore = int(data[1]) + 1
                scores[idx] = data[0] + "&^%" + str(userscore) + "&^%" + data[2] + "\n"
        scorefile.writelines(scores)
        if not found:
            scorefile.write(user + "&^%1&^%0\n")

    with open(channel_topics.format(channel), "r") as topics:
        topic = topics.readlines()[-1].strip("\n").split("&^%", 3)
        byuser = util.get_name(topic[1])
        return "I've told you {} times! It's \"{}\" (set by {} {})".format(
            p.number_to_words(userscore),
            topic[2],
            byuser,
            util.pretty_date(int(topic[0])),
        )


def count_topic(channel, user, time, msg):
    with open(channel_topic.format(channel), "a") as topics:
        topics.write(time + "&^%" + user + "&^%" + msg + "\n")
    with open(scores_file, "r") as scorefile:
        scores = scorefile.readlines()
    userscore = 1
    found = False
    with open(scores_file, "w") as scorefile:
        for idx, score in enumerate(scores):
            data = score.strip("\n").split("&^%")
            if data[0] == user:
                found = True
                userscore = int(data[2]) + 1
                scores[idx] = data[0] + "&^%" + data[1] + "&^%" + str(userscore) + "\n"
        scorefile.writelines(scores)
        if not found:
            scorefile.write(user + "&^%0&^%1")
    return "{} has changed the topic {} times!".format(user, p.number_to_words(userscore))


def set_topic(channel, user, time, msg):
    ircsock.send("TOPIC " + channel + " :" + msg + "\n")
    return count_topic(channel, user, time, msg)


def random_topic(channel, user, time, setTopic=False):
    with open(random_topics) as rtopics:
        msg = random.choice(rtopics.readlines()).strip("\n")
        if setTopic:
            set_topic(channel, user, time, msg)
        else:
            return "Suggested Topic: {}".format(msg)


def rollcall(channel):
    return "topicbot reporting! I respond to !topic !settopic !suggesttopic !thistory"


def topic_history(channel, user, count):
    try:
        iCount = int(count.split()[1])
    except (ValueError, IndexError):
        iCount = 3
    if iCount > 10:
        iCount = 10
    if iCount < 1:
        iCount = 3

    with open(channel_topics.format(channel), "r") as topicsfile:
        message = "Ok, here are the last {} topics".format(p.number_to_words(iCount))
        for idx, topic in enumerate(reversed(topicsfile.readlines()[-iCount:])):
            topic = topic.strip("\n").split("&^%", 3)
            byuser = util.get_name(topic[1])
            message += "\n{}: {} (set by {} {})".format( str(idx + 1), topic[2], byuser, util.pretty_date(int(topic[0])) )

        return message
