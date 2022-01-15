#!/usr/bin/env python3

import multiprocessing
from multiprocessing import Process, Manager
from random import *
import random

# import threading
from queue import Queue

# import sysv_ipc
import time



'''def worker(queue, data_ready):
    print("Starting thread:", threading.current_thread().name)    
    data_ready.wait()
    value = queue.get()
    print("got value:", value)
    print("Ending thread:", threading.current_thread().name)'''
 

processLook = multiprocessing.Lock()






# Game block
# def gameBlock(j, points, offre):







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
    
    def read():
        print("Put input : ")
        inFromUser = input()
        print("Offre taked : ", inFromUser)
        offre.append(inFromUser)


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
    if (identity == 1):
        for i in range(5):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
    if (identity == 2):
        for i in range(5,10):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
    if (identity == 3):
        for i in range(10,15):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
    if (identity == 4):
        for i in range(15,20):	
            j.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))



# Show the player's cards
def showCards(identity):
    if (identity == 1):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(5):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 2):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(5,10):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 3):
        print("Player ", identity, " cards")
        print("___________________________________________________________________")
        for i in range(10,15):	
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 4):
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
    if(valueInput == 1): # player 1
        # Show player j1's cards
        showCards(valueInput)
        # Hide the other cards ***

    if(valueInput == 2): # player 2
        # Show player j2's cards
        showCards(valueInput)
        # Hide the other cards ***

    if(valueInput == 3): # player 3
        # Show player j3's cards
        showCards(valueInput)
        # Hide the other cards ***

    if(valueInput == 4): # player 4
        # Show player j4's cards
        showCards(valueInput)
        # Hide the other cards ***



nOffreMade = 5
offreMadeM = [multiprocessing.Lock() for i in range(nOffreMade)]



def wait(joueurI):
    print ("Player ",joueurI, " is waiting")
    time.sleep(5)
    print ("Player ",joueurI, " is not waiting anymore")

def madeOffer(joueurI, offreInputMade):
    print ("Player ",joueurI, " is making an offer")
    time.sleep(3)
    print(offreInputMade)
    print ("Player ",joueurI, " is not making an offer anymore")

def takeOffer(joueurI, offreInputTake):
    print ("Player ",joueurI, " is taking an offer")
    time.sleep(3)
    print(offreInputTake)
    print ("Player ",joueurI, " is not taking an offer anymore")




def play(i):
    while True:
        wait(i)
        offreInputMade = i
        offreInputTake = (i + 1) % nOffreMade
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
            Joueur.read()
            print("Offre board : ", offre)
            madeOffer(i, offreInputMade)
            offreMadeM[offreInputMade].release()
        else :
            offreMadeM[offreInputTake].acquire()
            takeOffer(i, offreInputTake)
            offreMadeM[offreInputTake].release()



if __name__ == '__main__':
    manager = Manager()


    objCards = Cards() 
    objDeck = Deck() 
    
    deckOrigin = objDeck.mycardset 
    # print('\n Player 1 Cards: \n', deckOrigin) 
    
    objShuffleCards = ShuffleCards() 
    
    deckShuffled = objShuffleCards.shuffle() 
    # print('\n Player 2 Cards: \n', deckShuffled) 
    
    # ***********************************
    


    for i in range(19):     # To have access to the two parts separately
        deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
        deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]
    

    nb_players = 4
    for i in range(nb_players):
        # Player creation
        j = Joueur(i,[])



    # on définit le processus principale
    players = [multiprocessing.Process(target=play, args = (i, ))for i in range (nb_players)]
    
    for p in players:
        # Card assignment
        giveCards(j)
        p.start()
    for p in players:
        p.join()
    
    
    

    # Creation of a list managed by the manager, to add points
    points = manager.list()

    # TEST
    for i in range(19):     # Just to see the shuffled Deck
        print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])


    # Creation of a list managed by the manager to add the current offer
    offre = manager.list()
    

    # Main process
    print("Starting main process:", multiprocessing.current_process().name)
 
    queue = Queue()
    data_ready = multiprocessing.Event()
 
    '''# Who want to start
    valueInput = input("Who want to start?")
    queue.put(valueInput)

    # Show players' cards
    takeInput(int(valueInput))'''


    '''# Process initialization
    p1 = Process(target=jeu, args=(j1, points, offre))
    p2 = Process(target=jeu, args=(j2, points, offre))
    p3 = Process(target=jeu, args=(j3, points, offre))
    p4 = Process(target=jeu, args=(j4, points, offre))

    # Start + order of process
    p1.start()
    p1.join()

    p2.start()
    p2.join()

    p3.start()
    p3.join()

    p4.start()
    p4.join()'''

    '''j1.start()
    j2.start()
    j3.start()
    j4.start()


    j3.join()
    j2.join()
    j1.join()
    j4.join()'''


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