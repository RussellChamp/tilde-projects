#!/usr/bin/python3

import inflect
import random

p = inflect.engine()
LIMIT_GUESSING = True
MIN_ROUNDS = 5
MAX_ROUNDS = 12
SCORE_FILE = "/home/krowbar/Code/irc/data/numberwangscores.txt"
SHOW_TOP_NUM = 5
GOOD_CHAN = "#bots"

roundsLeft = 0
bonusRound = 0
guesses = 0
lastGuesser = ""
currentScores = {}


def resetGlobals():
    global roundsLeft
    global bonusRound
    global guesses
    global lastGuesser
    global currentScores
    roundsLeft = 0
    bonusRound = 0
    guesses = 0
    lastGuesser = ""
    currentScores.clear()


# returns a number of lines to be printed out. Numbers represent time to sleep
# between prints
def start_numberwang(channel, user):
    if channel != GOOD_CHAN:
        return [ "Numberwang has been disabled in {} due to spamminess. Please join {} to start a game.".format(channel, GOOD_CHAN) ]

    message = [ "{} started a game".format(user) ]
    resetGlobals()
    message.append("It's time for Numberwang!")
    message.append(1)
    message.append("Here's how to play:")
    message.append("1. There are 10 rounds")
    message.append("2. Each round lasts 10 seconds. You're up against the clock!")
    message.append("3. Play your numbers, as long as they're between 0 and 99.")
    message.append("4. That's Numberwang!")
    message.append(2)
    message.append("Let's get started!")
    global roundsLeft
    global bonusRound
    roundsLeft = random.randint(MIN_ROUNDS, MAX_ROUNDS)
    bonusRound = random.randint(2, roundsLeft - 1)
    # debug print
    print(
        "There will be {} rounds with the bonus on round {}".format(
            str(roundsLeft), str(roundsLeft - bonusRound + 1)
        )
    )


def print_scores():
    scoreStrs = []
    first = True
    for name in currentScores:
        scoreStrs.append(
            "{} is {} on {}".format(
                name,
                ("also " if not first and random.randint(1, 3) == 3 else ""),
                currentScores[name],
            )
        )
        first = False
    return p.join(scoreStrs)


def guess_numberwang(user, messageText):
    global guesses
    global lastGuesser
    global currentScores
    global roundsLeft
    # print(user + " guessed '" + messageText + "'")
    guess = re.sub(
        "[^0-9]", "", messageText.split()[0]
    )  # must have a number in the first 'word'
    messages = []
    if guess:
        if LIMIT_GUESSING and user == lastGuesser:
            messages.appen("{}, you just guessed! Give another player a try!".format(user))
        else:
            guesses += 1
            lastGuesser = user
            ###CORRECT GUESS###
            if (
                random.randint(0, 10) > 10 - guesses
            ):  # the more guesses, the higher the probability
                guesses = 0
                lastGuesser = ""
                message = "{}: THAT'S NUMBERWANG!".format(user)
                points = random.randint(2, 10) * (
                    random.randint(2, 4) if roundsLeft == bonusRound else 1
                )
                if user in currentScores.keys():
                    currentScores[user] += points
                else:
                    currentScores[user] = points
                roundsLeft -= 1
                message.append(2)
                if roundsLeft == 0:
                    messages.append("Numberwang is now over. Thank you for playing!")
                    messages.append("Final scores:")
                    messages.extend(print_scores())
                    save_scores()
                else:
                    messages.extend(print_scores())
                    newRoundStr = ""
                    if roundsLeft == 1:
                        newRoundStr += "The last round is Wangernumb!"
                    elif roundsLeft == bonusRound:
                        newRoundStr += "**Bonus Round!**"
                    else:
                        newRoundStr += "New Round!"
                    if random.randint(1, 10) > 8:
                        newRoundStr += " Let's rotate the board!"
                    messages.append("{} Start guessing!".format(newRoundStr))

            ###INCORRECT GUESS###
            else:
                messages.append("{}, {}, {} Numberwang!".format(
                    random.choice(["Sorry", "I'm sorry", "No", "Nope"]),
                    user,
                    random.choice(
                        [
                            "that's not",
                            "that is not",
                            "that isn't",
                            "that is not",
                            "that won't make",
                            "that will not make",
                        ]
                    ),
                ))

        return messages


def stop_numberwang(user):
    # print(user + " stopped a game")
    resetGlobals()
    return ["Numberwang has been stopped. No points have been awarded. {} is such a party pooper!".format(user)]


def save_scores():
    with open(SCORE_FILE, "r+") as scorefile:
        scores = scorefile.readlines()
        scorefile.seek(0)
        scorefile.truncate()
        for line in scores:
            for name in currentScores:
                score = line.strip("\n").split("&^%")
                if score[0] == name:
                    line = "{}&^%{}\n".format(
                        score[0], int(score[1]) + currentScores[name]
                    )
                    del currentScores[name]
                    break
            scorefile.write(line)

        for name in currentScores:  # new wangers
            scorefile.write("{}&^%{}\n".format(name, currentScores[name]))


def show_highscores():
    with open(SCORE_FILE, "r") as scorefile:
        scores = []
        for line in scorefile.readlines():
            sline = line.strip("\n").split("&^%")
            scores.append((int(sline[1]), sline[0]))
        scores = sorted(scores, reverse=True)[:SHOW_TOP_NUM]

        return ["====TOP WANGERS===="] + [" :== ~{} ({} points!) ==".format(score[1], score[0]) for score in scores]

def show_user_score(user):
    with open(SCORE_FILE, "r") as scorefile:
        for line in scorefile.readlines():
            score = line.strip("\n").split("&^%")
            if user == score[0]:
                return ["{}: Your global numberwang score is {}!".format(user, score[1])]
        # if we don't find a score line
        return ["{}: You haven't scored any points yet!".format(user)]
