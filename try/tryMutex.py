#!/usr/bin/env python3

# MultiProcessing using Mutex example       


import time        
from multiprocessing import Process, Lock, Array, Value


          
def task(index, result): 
    result[index.value] = index.value ** 2
             
def run(n):   
          
    mutex = Lock()
    start = time.time()  
    result = Array('i', range(n), lock=mutex)
           
    for k in range(n):  
        value = Value('i', k)
        process = Process(
            target=task,
            args=(value, result)
          
        )
        
        process.start()
        process.join()       
          
    print(list(result))           
    print("Finished in: ", time.time() - start)


if __name__ == '__main__':
    
    run(10)


'''
import threading
numOfGames = 10
resultList = [[] for x in xrange(numOfGames)]

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