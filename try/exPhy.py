#!/usr/bin/env python3

import multiprocessing
import random
import time


def think(philosophe):
    print ("Je suis",philosophe, "et I'm thinking")
    time.sleep(5)
    print ("Je suis",philosophe, "et I'm not thinking anymore")

def eat(philosophe):
    print ("Je suis",philosophe, "et I'm eating")
    time.sleep(3)
    print ("Je suis",philosophe, "et I'm not eating anymore")


def philosopher(i):
  while True:
      think(i)
      left_stick = i
      right_stick = (i + 1) % N

      if random.randint(0,1) == 0: # pour choisir s'il mange
          chopstick[left_stick].acquire()

          eat(i)
          chopstick[left_stick].release() # après avoir mangé il release le chopstick

      else :
          chopstick[right_stick].acquire()

          eat(i)
          chopstick[right_stick].release()

N = 5
chopstick = [multiprocessing.Lock() for i in range(N)] # on définit le lock


if __name__=="__main__":
    nb_philosophe = 5
    # on définit le processus principale
    les_philosophes = [multiprocessing.Process(target=philosopher, args = (i,))for i in range (nb_philosophe)]

    for p in les_philosophes:
        p.start()
    for p in les_philosophes:
        p.join()