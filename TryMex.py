#!/usr/bin/env python3.10


import threading
import time
from random import randint
import sys

# Definition of the lock
threadLock = threading.Lock()


class Player (threading.Thread):
   def __init__(self, identifiant, points):
      threading.Thread.__init__(self)
      self.nome = identifiant
      self.durata = points

   def run(self):
      print ("Player : " + self.name + " is playing")

      # Acquisition of the lock
      threadLock.acquire()
      time.sleep(self.durata) # action made by player
      print ("Player : " + self.name + " is not playing anymore")
      # Lock release
      threadLock.release()


if __name__ == '__main__':
    # Creation of threads
    thread1 = Player("Player#1", 0)
    thread2 = Player("Player#2", 0)
    thread3 = Player("Player#3", 0)
    thread4 = Player("Player#4", 0)


    # Starting the threads
    thread1.start()
    thread2.start()
    thread3.start()


    # Join
    thread1.join()
    thread2.join()
    thread3.join()

    
    # End of script
    print("Fine")
    print(sys.version)








'''
import threading



numOfGames = 10
resultList = [[] for x in range(numOfGames)]

class Game(threading.Thread):

    def __init__(self, player1, player2, number):
        threading.Thread.__init__(self)
        self.number = number
        self.player1 = player1
        self.player2 = player2

    def run(self):

        #Your game algorithm between self.player1 and self.player2 is here

        #Put game result into shared list
        resultList[self.number] = <result>


if __name__ == '__main__':
    #Create instances of the Game() class, pass your Player() objects
    #You can do the step in loop
    game0 = Game(<PlayerObj>,<PlayerObj>,0)
    game1 = Game(<PlayerObj>,<PlayerObj>,1)

    #Start execution of Game.run() methods of all Game() objects in separate threads
    #You can do the step in loop
    game0.start()
    game1.start()

    #Wait until all Game.run() methods are executed = all threads are finished
    #You can do the step in loop
    game0.join()
    game1.join()

    #In the shared list you have corresponding return values, 
    #whatever they are in your case [[result of Game 0],[result of Game 1],[]...]
    print resultList

'''