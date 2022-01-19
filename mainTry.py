#!/usr/bin/env python3

#!/usr/bin/env python3

from posixpath import split
import string
import threading

import multiprocessing
from multiprocessing import Process, Manager
from random import *
import random

# import threading
from threading import Thread,Timer
import queue
from queue import Queue

import sysv_ipc
import time


import pygame
from pygame.locals import *
from pygame import mixer
import sys 

# GUI *********************************************************************************************************************************
white = (255, 255, 255) 
black= (0, 0,0) 

# fenetre resolution
X = 1380	# width
Y = 868	# height



pygame.init() 	# Initialisation fenêtre de jeu
### mixer.init()	# Initialisation musique

font = pygame.font.Font('freesansbold.ttf', 50)	# Pour le message alla fin

smallfont = pygame.font.SysFont('Corbel',35)	## defining a font


fenetre = pygame.display.set_mode((X, Y), RESIZABLE)

# fills the screen with a color
## fenetre.fill((60,25,60))
fenetre.fill(white)

''' changer le fond 
fond = pygame.image.load("fondnoir.jpg").convert()
fenetre.blit(fond,(0,0))'''



# son = pygame.mixer.Sound("son.wav")
######## mixer.music.load("musique.mp3")
######## mixer.music.play(loops=-1)
# *************************************************************************************************************************************

# # # Definition of the deck **********************************************************************************************************

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
	
	def popCard(self): # à enlever 
		if len(self.mycardset) == 0: 
			return "NO CARDS CAN BE POPPED FURTHER"
		else: # à enlever
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
  
    def popCard(self): # à enlever
        if len(self.mycardset) == 0: 
            return "NO CARDS CAN BE POPPED FURTHER"
        else: # à enlever
            cardpopped = self.mycardset.pop() 
            return (cardpopped) 


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



# vectSplitOffre = []
# Initializing a queue
queue = []
for gg in range(11): # To solve the empty list problem
    queue.append(0)

# # ************************************************************************************************************************************


class return_values_nbCartesEg: # For double retourn
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c



# Definition of player 
class Joueur(multiprocessing.Process):
    def __init__(self, identifiant, l):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event() ### pour terminer - à enlever 
        self.identifiant = identifiant
        self.main = l

    def __str__(self):
        return "Player %s cards : %s" % (self.identifiant, self.main)

    def ajouterCarte (self,carte):
        self.main.append(carte)
    
    # Definition method to determine the greatest number of identical cards
    def maxCardsEg(self, id):
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

        maxCardsEg = max(cardsEg) # je sais pas si ça sert :P 
        minCardsEg = min(cardsEg)

        if minCardsEg == cv:
            typeExchange = "Velo"
        else: 
            if minCardsEg == ca:
                typeExchange = "Autobus"
            else:
                if minCardsEg == vv:
                    typeExchange = "Voiture"
                else: 
                    if minCardsEg == ct:
                        typeExchange = "Tracteur"
                    

        if maxCardsEg == minCardsEg:     # je sais pas si ça sert :P 
            if random.randint(0,1) == 0:
                minCardsEg = maxCardsEg

        # ajouter l'affichage avec (1, 0, 2, 2) -> donc (1 velo, etc .... )
        # ajouter le control (si min = 0, alors on prend l'autre au dessus)
        return id, minCardsEg, typeExchange



    def choseToTake(self, id): ### AJOUTER L'ECHANGE 
        print("The queue ICI: ")
        print(queue)
        print(" +++ ")
        idRet, minCardsEg, typeExchange = j.maxCardsEg(id)       # find the offers
        aa = queue.pop(0)   # id
        bb = queue.pop(1)   # value
        cc = queue.pop(2)   # type
        if idRet != aa and minCardsEg == bb: # we take it if ok 
            print("The offer : is token.")
            # appelle à echange !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # idRet, minCardsEg, typeExchange / aa, bb, cc
            if (id == 0):
                for i in range(5):
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        showCards(id)
            if (id == 1):
                for i in range(5,10):	
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        showCards(id)
            if (id == 2):
                for i in range(10,15):	
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        showCards(id)
            if (id == 3):
                for i in range(15,20):	
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        showCards(id)
        else: 
            queue.append(aa)
            queue.append(bb)
            queue.append(cc)



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
    for i in range(5):	
        # Show player j1's cards
        image= str(deckShuffledSplitValues[i]) + ".png"
        uno = pygame.image.load(image).convert()
        fenetre.blit(uno,(440+100*i,733))
    for i in range(5,10):	
        # Show player j2's cards
        image= str(deckShuffledSplitValues[i]) + ".png"
        uno = pygame.image.load(image).convert()
        fenetre.blit(uno,(1110,109+130*(i-5)))
    for i in range(10,15):	
        # Show player j3's cards
        image= str(deckShuffledSplitValues[i]) + ".png"
        uno = pygame.image.load(image).convert()
        fenetre.blit(uno,(440+100*(i-10),5))
    for i in range(15,20):
        # Show player j4's cards
        image= str(deckShuffledSplitValues[i]) + ".png"
        uno = pygame.image.load(image).convert()
        fenetre.blit(uno,(170,109+130*(i-15)))
        # updates the frames of the game
    pygame.display.update()
    # pygame.display.flip()	



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




def takeInput(valueInput):
    if(valueInput == 0): # player 1
        showCards(valueInput)

    if(valueInput == 1): # player 2
        showCards(valueInput)

    if(valueInput == 2): # player 3
        showCards(valueInput)

    if(valueInput == 3): # player 4
        showCards(valueInput)


nOffreMade = 5
offreMadeM = [multiprocessing.Lock() for i in range(nOffreMade)]



def exchange(off):
    i = 0 # à faire <------------------------------------------------------------------------------------------------------------------------------------------------------



def wait(joueurI):
    print ("Player ",joueurI, " is waiting")
    #the normal program executes without blocking. here just counting up
    time.sleep(5)
    print ("Player ",joueurI, " is not waiting anymore")

def madeOffer(joueurI):
    print ("Player ",joueurI, " is making an offer")
    time.sleep(10)
    idRet, minCardsEg, typeExchange = j.maxCardsEg(joueurI)    # make the offer
    queue.append(idRet)
    queue.append(minCardsEg)
    queue.append(typeExchange)
    print ("Player ",joueurI, " is not making an offer anymore")

def takeOffer(joueurI):
    print ("Player ",joueurI, " is taking an offer")
    time.sleep(7)
    j.choseToTake(joueurI)  # take the offer
    print("Player ",joueurI, " is not taking an offer anymore")




def play(i):
    done = True
    while done:
        wait(i)
        offreInputMade = i  #
        offreInputTake = (i + 1) % nOffreMade   #
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
            # Show players' cards
            takeInput(i) 
            offreMadeM[offreInputTake].release()







if __name__ == '__main__':
    manager = Manager()

    
    nb_players = 4
    for i in range(nb_players):
        # Player creation
        j = Joueur(i,[])



    # on définit le processus principale
    players = [multiprocessing.Process(target=play, args = (i, ))for i in range (nb_players)]
    
    
    

    # Creation of a list managed by the manager, to add points
    points = manager.list()


    # Creation of a list managed by the manager to add the current offer
    offre = manager.list()
    

    # Main process
    print("Starting main process:", multiprocessing.current_process().name)
 
    
    data_ready = multiprocessing.Event() # <- à verifier



    # GUI *********************************************************************************************
    # Disposition cartes dans la fenêtre de jeu
    # Cloche
    uno = pygame.image.load("cloche.jpg").convert()
    fenetre.blit(uno,(645,389))
    # pygame.display.update()
    # pygame.display.flip()



    # TEXTE WITH PLAYER NAME
    label = smallfont.render("PLAYER 1", 1, black)
    fenetre.blit(label, (300, 790))

    label = smallfont.render("PLAYER 2", 1, black)
    fenetre.blit(label, (1100, 780))

    label = smallfont.render("PLAYER 3", 1, black)
    fenetre.blit(label, (950, 50))

    label = smallfont.render("PLAYER 4", 1, black)
    fenetre.blit(label, (165, 60))



    dodo = 0    # TEST <- il faut y mettre l'offre
    # TEXTE WITH OFFERS
    label = smallfont.render("Offre : " + str(dodo), 1, black)
    fenetre.blit(label, (300, 830))

    label = smallfont.render("Offre : " + str(dodo), 1, black)
    fenetre.blit(label, (1100, 820))

    label = smallfont.render("Offre : " + str(dodo), 1, black)
    fenetre.blit(label, (950, 10))

    label = smallfont.render("Offre : " + str(dodo), 1, black)
    fenetre.blit(label, (165, 20))



    for i in range(25):
        if i<5:											# Joueur 1
            # randomInt = random.randint(1, 4)
            # image= str(randomInt) + ".png"
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(440+100*i,733))
        elif i<10:										# Joueur 2
            # randomInt = random.randint(1, 4)
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(1110,109+130*(i-5)))
        elif i<15:										# Joueur 3
            # randomInt = random.randint(1, 4)
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(440+100*(i-10),5))
        elif i<20:										# Joueur 4
            # randomInt = random.randint(1, 4)
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(170,109+130*(i-15)))

    
    # updates the frames of the game
    pygame.display.update()
    # pygame.display.flip()
    
    # ************************************************************************************************

    '''t3=Thread(target=entreeClavier,args=()) # VERIFIER 
    t3.start()
    t3.join()'''


    # Start + order of process
    for p in players:
        # Card assignment
        giveCards(j)
        p.start()
    for p in players:
        p.join()



    time.sleep(30)  # time after end processus
    


    # TEST
    print("The points : ", points)
    
    # Main process
    print("Ending process:", multiprocessing.current_process().name)