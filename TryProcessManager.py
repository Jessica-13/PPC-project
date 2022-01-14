#!/usr/bin/env python3.10

from multiprocessing import Process, Manager
from random import *


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
    match identity:
        case 1:
            print("Player ", identity, " cards")
            for i in range(5):	
                j1.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
                print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
            print(" ")
        case 2:
            print("Player ", identity, " cards")
            for i in range(5,10):	
                j2.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
                print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
            print(" ")
        case 3:
            print("Player ", identity, " cards")
            for i in range(10,15):	
                j3.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
                print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
            print(" ")
        case 4:
            print("Player ", identity, " cards")
            for i in range(15,20):	
                j4.ajouterCarte(Carte(deckShuffledSplitValues[2], deckShuffledSplitSuites[2]))
                print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
            print(" ")
        case _:
            print("ERROR : problem with player index")


def jeu(identifiant, points, offre):
    offre.append(1)
    offre.append(2)
    offre.append(3)
    points.reverse()
    print("Identifiant : ", identifiant)
    print("Try out: ", j1.main)

'''class MathsClass:
    def add(self, x, y):
        return x + y
    def mul(self, x, y):
        return x * y'''


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
    
    
    # pioche = manager.list()    # Creation of a shared list representing the Deck -> common to all players

    for i in range(19):
        deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
        deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]
    
    
    


    j1= Joueur(1,[])
    j2= Joueur(2,[])
    j3= Joueur(3,[])
    j4= Joueur(4,[])
    giveCards(j1.identifiant)
    giveCards(j2.identifiant)
    giveCards(j3.identifiant)
    giveCards(j4.identifiant)

    points = manager.list(range(10))


    for i in range(19):     # To see the shuffled Deck
        print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])

    



    offre = manager.list()  # Offer made
    

    p1 = Process(target=jeu, args=(j1, points, offre))
    p2 = Process(target=jeu, args=(j2, points, offre))
    p3 = Process(target=jeu, args=(j3, points, offre))
    p4 = Process(target=jeu, args=(j4, points, offre))
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