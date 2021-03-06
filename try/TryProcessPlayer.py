#!/usr/bin/env python3

from multiprocessing import Process, Manager
from random import *


import sysv_ipc

key = 128
mq = sysv_ipc.MessageQueue(key)



# Game block
def playerBlock(j, points, offre):
    while True:
        message, t = mq.receive()
        value = message.decode()
        value = int(value)
        
        if value:
            print("Player : ", j, ", received:", value)
            # jeu(value)
        else:
            print("exiting.")   # value = 0 -> exit
            print("Player : ", j, ", made:", points, " points.")
            break
        
        
        try:
            value2 = int(input())
            offre.append(value2)
            # jeu(value)
        except:
            print("Input error, try again!")
        message2 = str(value2).encode()
        mq.send(message2)




# Definition of player 
class Joueur:
    def __init__(self, identifiant, l):
        self.identifiant=identifiant
        self.main= l

    def __str__(self):
        return "Player %s cards : %s" % (self.identifiant, self.main)

    def ajouterCarte (self,carte):
        self.main.append(carte)


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
        print("Player ", identity, " cards")
        for i in range(5):	
            j1.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 2):
        print("Player ", identity, " cards")
        for i in range(5,10):	
            j2.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 3):
        print("Player ", identity, " cards")
        for i in range(10,15):	
            j3.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")
    if (identity == 4):
        print("Player ", identity, " cards")
        for i in range(15,20):	
            j4.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
            print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        print(" ")



def jeu(identifiant, points, offre):
    offre.append(1)
    offre.append(2)
    offre.append(3)
    # points.append(values)
    print(points)
    print("Identifiant : ", identifiant)
    print("Try out: ", j1.main)



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
    

    
    # Player creation
    j1= Joueur(1,[])
    j2= Joueur(2,[])
    j3= Joueur(3,[])
    j4= Joueur(4,[])

    # Card assignment
    giveCards(j1.identifiant)
    giveCards(j2.identifiant)
    giveCards(j3.identifiant)
    giveCards(j4.identifiant)

    # Creation of a list managed by the manager, to add points
    points = manager.list()

    # TEST
    for i in range(19):     # Just to see the shuffled Deck
        print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])

    


    # Creation of a list managed by the manager to add the current offer
    offre = manager.list()
    
    # Process initialization
    '''p1 = Process(target=jeu, args=(j1, points, offre))
    p2 = Process(target=jeu, args=(j2, points, offre))
    p3 = Process(target=jeu, args=(j3, points, offre))
    p4 = Process(target=jeu, args=(j4, points, offre))'''

    p1 = Process(target=playerBlock, args=(j1, points, offre))
    p2 = Process(target=playerBlock, args=(j2, points, offre))
    p3 = Process(target=playerBlock, args=(j3, points, offre))
    p4 = Process(target=playerBlock, args=(j4, points, offre))


    # Start + order of threads
    p1.start()
    p1.join()

    p2.start()
    p2.join()

    p3.start()
    p3.join()

    p4.start()
    p4.join()


    # TEST
    print(points)
    print(offre)



    # Keyboard input
    # playerBlock()