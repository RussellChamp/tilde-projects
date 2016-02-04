#!/usr/bin/python
import random
import inflect

p = inflect.engine()
primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

def make_puzzle():
  answer = 0
  puzzle = random.choice(["Prove you're not a robot: ", "Are you a robot?: ", "Anti-bot check: ", "Counter-cndorphant measures: "])
  puzzle += random.choice(["What is", "How many is", "What do you get from", "What do you get with", "What is the value of", "Can you answer", "Can you tell me"])
  puzzle += " "
  roll = random.randrange(0,6)
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
      answer = var1 ** var2
      puzzle += p.number_to_words(var1) + " to the " + p.ordinal(p.number_to_words(var2)) + " power"
  elif roll == 5:
      p1 = primes[random.randrange(0,len(primes))]
      p2 = primes[random.randrange(0,len(primes))]
      answer = str(min(p1,p2)) + ',' + str(max(p1,p2))
      puzzle += p.number_to_words(p1 * p2) + " when factored into its two primes (answer in the form of the two primes with a comma between)"


  puzzle += "? (Answer with numbers)"
  return [answer, puzzle]
