#!/usr/bin/env python3

from multiprocessing import Process, Manager
from random import *



# Définition de l'objet "carte"
class Carte:
	def __init__(self, val, couleur):
		self.couleur = couleur
		self.valeur = val

# # Définition de l'objet "carte" pour le paquet
class Cards:
	global suites, values 
	suites = ['Velo', 'Autobus', 'Voiture', 'Tracteur']
	values = ['3', '5', '7', '9'] 
	
	def __init__(self): 
		pass

# Définir le paquet
class Deck(Cards): 
	def __init__(self): 
		Cards.__init__(self) 
		self.mycardset = []
		
		for i in range(5): 		# 4 joueurs
			for j in range(4): 	    # 5 cartes par famille
				self.mycardset.append(values[j] + " " + suites[j])
	
	def popCard(self): 
		if len(self.mycardset) == 0: 
			return "NO CARDS CAN BE POPPED FURTHER"
		else: 
			cardpopped = self.mycardset.pop() 
			print("Card removed is", cardpopped) 


# Mixer le paquet
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








def jeu(identifiant, points, offre):
    offre.append(1)
    offre.append(2)
    offre.append(3)
    points.reverse()
    print("identifiant : ", identifiant)

class MathsClass:
    def add(self, x, y):
        return x + y
    def mul(self, x, y):
        return x * y


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
    
    
    pioche = manager.list()    # Création d'une liste partagée représentant la pioche, pour que ça soit commune à tous les joueurs

    for i in range(19):
        deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
        deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]
    
    for i in range(19):
        pioche.append(Carte(deckShuffledSplitValues[i], deckShuffledSplitSuites[i]))	
        print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
        











    identifiant = 1
    points = manager.list(range(10))

    offre = manager.list()
    

    p = Process(target=jeu, args=(identifiant, points, offre))
    p.start()
    p.join()

    print(points)
    print(offre)