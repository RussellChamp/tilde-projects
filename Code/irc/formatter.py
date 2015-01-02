import time
import re

def format_message(message):
	pattern = r'^:.*\!~(.*)@.* (.*) (.*) :(.*)'
	now = int(time.time())
	matches = re.match(pattern, message)
	if not matches:
		return ''

	nick    = matches.group(1).strip()
        command = matches.group(2).strip()
        channel = matches.group(3).strip()
	message = matches.group(4).strip()

	return "%s\t%s\t%s\t%s\t%s" % (now, nick, command, channel, message)
