# Anaisha's lessons

import pyttsx3

engine = pyttsx3.init()
#engine.say("I will speak this text")
#engine.runAndWait()
engine.setProperty('rate', 125)


import random
easy = []
medium = []
hard = []
def catagorize():
  with open('common.txt') as f:
    file = f.read().split('\n')
    for i, word in enumerate(file):
      if len(word) in range(2,8) and i < 1000:
        easy.append(word)
      elif len(word) in range(5,10) and i in range(1000,5000):
        medium.append(word)
      elif len(word) > 8 and i in range(5000,10000):
        hard.append(word)  

def choose():
  if category == 'easy':
    word = random.choice(easy)
    engine.say(word)
    engine.runAndWait()
    # read word here
    x = input()
    if x == word:
      print("You are correct!")
      return 1
    else:
      print("You are wrong!")
      print(f'The correct spelling for this is {word}')
      return 0
  if category == 'medium':
    word = random.choice(medium)
    engine.say(word)
    engine.runAndWait()
    # read word here
    x = input()
    if x == word:
      print("You are correct!")
      return 1
    else:
      print("You are wrong!")  
      print(f'The correct spelling for this is {word}')
      return 0
  if category == 'hard':
    word = random.choice(hard)
    engine.say(word)
    engine.runAndWait()
    # read word here
    x = input()
    if x == word:
      print("You are correct!")
      return 1
    else:
      print("You are wrong!")
      print(f'The correct spelling for this is {word}')
      return 0

print("Let's play a spelling game!")
category = input('Please input easy, medium, hard')
print("how many questions would you like?")
n = input()
count = 0
for i in range(int(n)):
  catagorize()
  count += choose()
print("Good job!")
print(f'Your score is: {count}/{n}' )
    






