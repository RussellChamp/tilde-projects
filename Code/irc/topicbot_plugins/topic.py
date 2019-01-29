#!/usr/bin/python3

import pinhook.plugin
from util import topic

import inflect

@pinhook.plugin.listener('topic')
def topic_listener(msg):
    if msg.text.startswith("TOPIC"):
        topic.count_topic(msg.channel, msg.nick, msg.time, msg.text)

@pinhook.plugin.register('!topic')
def topic_plugin(msg):
    return pinhook.plugin.message(topic.get_topic(msg.channel, msg.nick, msg.time))

@pinhook.plugin.register('!settopic')
def set_topic_plugin(msg):
    return pinhook.plugin.action("TOPIC {} {}".format(msg.channel, msg.arg))

@pinhook.plugin.register('!randomtopic')
def set_topic_plugin(msg):
    return pinhook.plugin.message(topic.random_topic(msg.channel, msg.nick, msg.time, msg.nick == msg.owner))

@pinhook.plugin.register('!suggesttopic')
def suggest_topic_plugin(msg):
    return pinhook.plugin.message(topic.random_topic(msg.channel, msg.nick, msg.time, False))

@pinhook.plugin.register('!thistory')
def topic_history_plugin(msg):
    return pinhook.plugin.message(topic.topic_history(msg.channel, msg.nick, msg.arg))

