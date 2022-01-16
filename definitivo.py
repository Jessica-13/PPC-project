#!/usr/bin/env python3

import threading

import multiprocessing
from multiprocessing import Process, Manager
from random import *
import random

# import threading
import queue
from queue import Queue

# import sysv_ipc
import time



'''def worker(queue, data_ready):
    print("Starting thread:", threading.current_thread().name)    
    data_ready.wait()
    value = queue.get()
    print("got value:", value)
    print("Ending thread:", threading.current_thread().name)'''
 


# Game block
# def gameBlock(j, points, offre):

# queueQ = queue.Queue()


# Circular Queue implementation in Python
class CircularQueue():
    def __init__(self, k):
        self.k = k
        self.queue = [None] * k
        self.head = self.tail = -1

    # Insert an element into the circular queue
    def enqueue(self, data):

        if ((self.tail + 1) % self.k == self.head):
            print("The circular queue is full\n")

        elif (self.head == -1):
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 1) % self.k
            self.queue[self.tail] = data

    # Delete an element from the circular queue
    def dequeue(self):
        if (self.head == -1):
            print("The circular queue is empty\n")

        elif (self.head == self.tail):
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.k
            return temp

    def printCQueue(self):
        if(self.head == -1):
            print("No element in the circular queue")

        elif (self.tail >= self.head):
            for i in range(self.head, self.tail + 1):
                print(self.queue[i], end=" ")
            print()
        else:
            for i in range(self.head, self.k):
                print(self.queue[i], end=" ")
            for i in range(0, self.tail + 1):
                print(self.queue[i], end=" ")
            print()

queueQ = CircularQueue(8)



class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return


# FOR INPUT 
def my_callback(inp):
    #evaluate the keyboard input
    print('You Entered:', inp)
    queueQ.enqueue(inp)
    print("The queue ICI : ")
    queueQ.printCQueue()    #



# FOR LOCK 
processLook = multiprocessing.Lock()

#start the Keyboard thread
kthread = KeyboardThread(my_callback)



# Definition of player 
class Joueur(multiprocessing.Process):
    def __init__(self, identifiant, l):
        multiprocessing.Process.__init__(self)
        self.identifiant=identifiant
        self.main= l
    
    def run(self):
        print ("Process : " + self.name + " START")
        # *** ACTION ***
        # jeu(self.identifiant)

    def __str__(self):
        return "Player %s cards : %s" % (self.identifiant, self.main)

    def ajouterCarte (self,carte):
        self.main.append(carte)
    
    # Définition méthode pour déterminer le plus grand nombre de cartes identiques
    def maxCardsEg(self):
        # To get the number of occurrences of each item in a list
        cardsEg = []
        
        cv = self.main.count("Velo")
        ca = self.main.count("Autobus")
        vv = self.main.count("Voiture")
        ct = self.main.count("Tracteur")

        cardsEg.append(cv)
        cardsEg.append(ca)
        cardsEg.append(vv)
        cardsEg.append(ct)

        maxCardsEg = max(cardsEg)
        '''max = 0
        indice = -1
        for j in range(len(cardsEgSplit)):
            if cardsEgSplit[j] > max:
                max = cardsEgSplit[j]

        
        for j in range (i.main):
            counted = i.main.count(i.main[i][j]) 
            if (max < counted) and (Carte.couleur[indice].nom != Carte.valeur[j].nom):
                max = counted
                indice = j
            elif (compte == max):
                if (i.cartes[j].points > i.cartes[indice].points):
                    indice = j

        t = return_values_nbCartesEg(max, indice)   # How many times/which card
        return t'''
        return maxCardsEg

    def choseToTake(self, off):
        print("The queue ICI: ")
        queueQ.printCQueue()
        print(" +++ ")
        if queueQ.dequeue() == 1 and off == 1:
            print("The offer : ", off, " is token.")
        else: 
            queueQ.enqueue(1)
            if queueQ.dequeue() == 2 and off == 2:
                print("The offer : ", off, " is token.")
            else:
                queueQ.enqueue(2)
                if queueQ.dequeue() == 3 and off == 3:
                    print("The offer : ", off, " is token.")
                else:
                    queueQ.enqueue(3)
                    if queueQ.dequeue() == 4 and off == 4:
                        print("The offer : ", off, " is not permitted.")
                    else :
                        queueQ.enqueue(4)
                        if queueQ.dequeue() == 5 and off == 5:
                            print("The player : ", self.identifiant, " win.")
                            #points.append()       # ***
                            #players.terminate()   # ***



# Definition of the "Carte" object
class Carte:
    def __init__(self, val, couleur):
        self.couleur = couleur
        self.valeur = val
        
    def __str__(self):
        return "%s : %s" % (self.couleur, self.valeur)

# # Definition of the "Carte" object for the Deck
class Cards:
	global suites, values 
	suites = ['Velo', 'Autobus', 'Voiture', 'Tracteur']
	values = ['3', '5', '7', '9'] 
	
	def __init__(self): 
		pass

# Definition of the Deck
class Deck(Cards): 
	def __init__(self): 
		Cards.__init__(self) 
		self.mycardset = []
		
		for i in range(5): 		# 4 players
			for j in range(4): 	    # 5 cards for every family
				self.mycardset.append(values[j] + " " + suites[j])
	
	def popCard(self): 
		if len(self.mycardset) == 0: 
			return "NO CARDS CAN BE POPPED FURTHER"
		else: 
			cardpopped = self.mycardset.pop() 
			print("Card removed is", cardpopped) 


# Shuffle the deck of cards
class ShuffleCards(Deck): 
    def __init__(self): 
        Deck.__init__(self) 
  
    def shuffle(self): 
        if len(self.mycardset) < 20: 
            print("cannot shuffle the cards") 
        else: 
            shuffle(self.mycardset) 
            return self.mycardset 
  
    def popCard(self): 
        if len(self.mycardset) == 0: 
            return "NO CARDS CAN BE POPPED FURTHER"
        else: 
            cardpopped = self.mycardset.pop() 
            return (cardpopped) 


# Heap definition for each player
def giveCards(identity):
    if (identity == 0):
        for i in range(5):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[i], deckShuffledSplitSuites[i]))
    if (identity == 1):
        for i in range(5,10):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[i], deckShuffledSplitSuites[i]))
    if (identity == 2):
        for i in range(10,15):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[i], deckShuffledSplitSuites[i]))
    if (identity == 3):
        for i in range(15,20):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[i], deckShuffledSplitSuites[i]))



# Show the player's cards
def showCards(identity):
    if (identity == 0):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(5):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 1):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(5,10):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 2):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(10,15):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 3):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(15,20):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")


'''
def jeu(identifiant):
    showCards(identifiant)
    # Acquisition of the lock
    processLook.acquire()
    reponse = int(input("Make or accept?(1/2)")) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! verifier
    if(reponse == 1):   # make an offer
        # Start with offers
        makeOffreInput = input("Submit your offer :")
        offre.append(makeOffreInput)
        print(makeOffreInput)   # TEST
        print ("Process : " + identifiant + " STOP")
        # Lock release
        processLook.release()
    else:
        # SHOW OFFERS

        # Look at offers and take one
        takeOffreInput = input("Which offer do you want to accept?")
        offre.remove(takeOffreInput)

        # UPDATE CARDS

        # CHECK IF VICTORY
        # points.append(values)
        print(points)
        # print("Identifiant : ", identifiant)
        print("Try out: ", identifiant.main) # *** FOR CARDS ***

        print ("Process : " + identifiant + " STOP")
        # Lock release
        processLook.release()
'''


def takeInput(valueInput):
    if(valueInput == 0): # player 1
        # Show player j1's cards
        showCards(valueInput)
        # Hide the other cards ***

    if(valueInput == 1): # player 2
        # Show player j2's cards
        showCards(valueInput)
        # Hide the other cards ***

    if(valueInput == 2): # player 3
        # Show player j3's cards
        showCards(valueInput)
        # Hide the other cards ***

    if(valueInput == 3): # player 4
        # Show player j4's cards
        showCards(valueInput)
        # Hide the other cards ***



nOffreMade = 5
offreMadeM = [multiprocessing.Lock() for i in range(nOffreMade)]



class return_values_nbCartesEg: # For double retourn
    def __init__(self, a, b):
        self.a=a
        self.b=b



def wait(joueurI):
    print ("Player ",joueurI, " is waiting")
    #the normal program executes without blocking. here just counting up
    time.sleep(2)
    print ("Player ",joueurI, " is not waiting anymore")

def madeOffer(joueurI):
    print ("Player ",joueurI, " is making an offer")
    time.sleep(5)
    off = j.maxCardsEg()    # make the offer
    queueQ.enqueue(off)          # put the offer in the queue
    print("The queue : ")
    queueQ.printCQueue()
    print ("Player ",joueurI, " is not making an offer anymore")

def takeOffer(joueurI):
    print ("Player ",joueurI, " is taking an offer")
    time.sleep(3)
    off = j.maxCardsEg()    # make the offer
    j.choseToTake(off) # take the offer
    print ("Player ",joueurI, " is not taking an offer anymore")




def play(i):
    while True:
        wait(i)
        offreInputMade = i  #
        offreInputTake = (i + 1) % nOffreMade   #
        '''# Who want to start
        print("Want to make an offer?(y or n)")
        try:
            valueInput = input()
            print(valueInput)
        except EOFError as e:
            print(e)'''
        # queue.put(valueInput)
        if random.randint(0,1) == 0:
            offreMadeM[offreInputMade].acquire()
            # Show players' cards
            takeInput(i)    
            # *** print("Offre board : ", offre)
            madeOffer(i)    #
            offreMadeM[offreInputMade].release()
        else :
            offreMadeM[offreInputTake].acquire()
            takeOffer(i)    #
            offreMadeM[offreInputTake].release()



if __name__ == '__main__':
    manager = Manager()


    objCards = Cards() 
    objDeck = Deck() 
    
    deckOrigin = objDeck.mycardset 
    # print('\n Cards: \n', deckOrigin) 
    
    objShuffleCards = ShuffleCards() 
    
    deckShuffled = objShuffleCards.shuffle() 
    # print('\n Cards Shuffled : \n', deckShuffled) 
    
    # ***********************************
    


    # for i in range(19):     # To have access to the two parts separately
    deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
    deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]
    

    nb_players = 4
    for i in range(nb_players):
        # Player creation
        j = Joueur(i,[])



    # on définit le processus principale
    players = [multiprocessing.Process(target=play, args = (i, ))for i in range (nb_players)]
    
    
    

    # Creation of a list managed by the manager, to add points
    points = manager.list()

    '''# TEST
    for i in range(19):     # Just to see the shuffled Deck
        print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
    '''

    # Creation of a list managed by the manager to add the current offer
    offre = manager.list()
    

    # Main process
    print("Starting main process:", multiprocessing.current_process().name)
 
    
    data_ready = multiprocessing.Event()
 
    '''# Who want to start
    valueInput = input("Who want to start?")
    queue.put(valueInput)

    # Show players' cards
    takeInput(int(valueInput))'''

    # Start + order of process
    for p in players:
        # Card assignment
        giveCards(j)
        p.start()
    for p in players:
        p.join()

    # TEST
    print(points)
    print(offre) 
    # Main process
    print("Ending process:", multiprocessing.current_process().name)









    # data_ready.set()
    
    # set() # Set the internal flag to true. 
    # All threads waiting for it to become true are awakened. 
    # Threads that call wait() once the flag is true will not block at all.

    # clear() # Reset the internal flag to false. 
    # Subsequently, threads calling wait() will block until set() is called to set the internal flag 
    # to true again.

    # wait(timeout=None) # Block until the internal flag is true. 