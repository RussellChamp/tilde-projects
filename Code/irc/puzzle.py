#!/usr/bin/python
import random
import inflect

p = inflect.engine()

def make_puzzle():
  answer = 0
  puzzle = random.choice(["Prove you're not a robot: ", "Are you a robot?: ", "Anti-bot check: ", "Counter-cndorphant measures: "])
  puzzle += random.choice(["What is", "How many is", "What do you get from", "What do you get with", "What is the value of", "Can you answer", "Can you tell me"])
  puzzle += " "
  roll = random.randrange(0,4)
  var1 = random.randrange(1,10)
  var2 = random.randrange(1,10)

  if roll == 0:
      answer = var1 + var2
      puzzle += p.number_to_words(var1) + " " + random.choice(["and", "plus", "sum", "add"]) + " " + p.number_to_words(var2)

  elif roll == 1:
      answer = var1 * var2
      puzzle += p.number_to_words(var1) + " " + random.choice(["times", "multiply", "multiplied by", "product"]) + " " + p.number_to_words(var2)
  elif roll == 2:
      if var2 > var1:
          var1,var2 = var2,var1
      answer = var1 - var2
      puzzle += p.number_to_words(var1) + " " + random.choice(["minus", "subtract", "take away", "less"]) + " " + p.number_to_words(var2)
  elif roll == 3:
      if var2 > var1:
          var1,var2 = var2,var1
      answer = var1 * 2 / var2
      puzzle += p.number_to_words(var1*2) + " " + random.choice(["divided by", "over"]) + " " + p.number_to_words(var2) + " (no remainder)"
  elif roll == 4:
      answer == var1 ** var2
      puzzle += p.number_to_words(var1) + " to the " + p.ordinal(p.number_to_words(var2)) + " power"

  puzzle += "? (Answer with numbers)"
  return [answer, puzzle]
