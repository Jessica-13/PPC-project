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

import signal
import os



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
# # ************************************************************************************************************************************


'''def worker(queue, data_ready):
    print("Starting thread:", threading.current_thread().name)    
    data_ready.wait()
    value = queue.get()
    print("got value:", value)
    print("Ending thread:", threading.current_thread().name)'''
 


class return_values_nbCartesEg: # For double retourn
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c



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



'''class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            #self.input_cbk(input()) #waits to get input + Return
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()'''

                
'''
# FOR INPUT 
def my_callback(inp):
    #evaluate the keyboard input
    print('You Entered:', inp)
    queueQ.enqueue(inp)
    print("The queue ICI : ")
    queueQ.printCQueue()    #'''



# FOR LOCK 
processLook = multiprocessing.Lock()    # à enlever 

'''#start the Keyboard thread
kthread = KeyboardThread(my_callback)'''



# Definition of player 
class Joueur(multiprocessing.Process):
    def __init__(self, identifiant, l):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event() ### pour terminer - à enlever 
        self.identifiant = identifiant
        self.main = l
    
    ''' def run(self):
        print ("Process : " + self.name + " START")
        while not self.exit.is_set():
            pass
        # *** ACTION ***
        # jeu(self.identifiant)

    def shutdown(self):
        self.exit.set()'''

    def __str__(self):
        return "Player %s cards : %s" % (self.identifiant, self.main)

    def ajouterCarte (self,carte):
        self.main.append(carte)
    
    # Definition method to determine the greatest number of identical cards
    def maxCardsEg(self, id):
        # To get the number of occurrences of each item in a list
        cardsEg = []
        
        # Attribue à cv, ca, vv, ct, le nombre de cartes dans la liste avec le nom correspondant
        cv = self.main.count("Velo")
        ca = self.main.count("Autobus")
        vv = self.main.count("Voiture")
        ct = self.main.count("Tracteur")

        # cardsEg est la liste contenant le nombre de cartes de chaque nom (catégorie)
        cardsEg.append(cv)
        cardsEg.append(ca)
        cardsEg.append(vv)
        cardsEg.append(ct)

        maxCardsEg = max(cardsEg) # je sais pas si ça sert :P 
        minCardsEg = min(cardsEg)

        if (maxCardsEg == 5 or minCardsEg = 5):
            os.kill(os.getppid(), signal.SIGINT)

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



        # ajouter l'affichage avec (1, 0, 2, 2) -> donc (1 velo, etc .... )
        # ajouter le control (si min = 0, alors on prend l'autre au dessus)
        return id, minCardsEg, typeExchange   # How many times/which card
    



    def choseToTake(self, off): ### AJOUTER L'ECHANGE 
        print("The queue ICI: ")
        queueQ.printCQueue()
        print(" +++ ")
        offreTokenFromQueue = queueQ.dequeue()
        # vectSplitOffreId, vectSplitOffreMinCardsEg, vectSplitOffreTypeExchange = maxCardsEg(offreTokenFromQueue)
        # vectSplitSelfOffreId, vectSplitSelfOffreMinCArdsEg, vectSplitSelfOffreTypeExchange = maxCardsEg(off)
        # vectSplitOffre[0] / vectSplitSelfOffre[0] : identifier
        # vectSplitOffre[1] / vectSplitSelfOffre[1] : value
        # vectSplitOffre[2] / vectSplitSelfOffre[2] : type

        # si le joueur à l'origine de l'offre est différent du joueur qui regarde l'offre
        # ET si le nombre de cartes offertes correspond au nombre de cartes cherché
        # ET si ce nombre de cartes = 1
        if vectSplitOffre[0] != vectSplitSelfOffre[0] and vectSplitOffre[1] == vectSplitSelfOffre[1] and vectSplitOffre[1] == 1: 
            print("The offer with 1 card : ", off, " is token.")
            # appelle à echange 
        else: 
            queueQ.enqueue(1)
            if vectSplitOffre[0] != vectSplitSelfOffre[0] and vectSplitOffre[1] == vectSplitSelfOffre[1] and vectSplitOffre[1] == 2: 
                print("The offer with 2 cards : ", off, " is token.")
                # appelle à echange 
            else:
                queueQ.enqueue(2)
                if vectSplitOffre[0] != vectSplitSelfOffre[0] and vectSplitOffre[1] == vectSplitSelfOffre[1] and vectSplitOffre[1] == 3:
                    print("The offer with 3 cards : ", off, " is token.")
                    # appelle à echange 
                    
        offreTokenFromQueueId = [i.split(' ')[0] for i in offreTokenFromQueue]
        offId = [i.split(' ')[0] for i in off]

        offreTokenFromQueueValue = [i.split(' ')[1] for i in offreTokenFromQueue]
        offalue = [i.split(' ')[1] for i in off]
        
        if offreTokenFromQueueId != offId and offreTokenFromQueueValue == offalue: # we take it if ok 
            print("The offer : ", off, " is token.")
            # appelle à echange 

    def exchange(typeExchange, off, listeCartes):
    # i = 0
    # enlever les cartes en nombre min du joueur qui accepte
    for a in range(off):
        self.l.remove(typeExchange)
    # rajouter les cartes de l'offre du joueur qui accepte
    for a in range(off):
        self.l.append()
    # enlever les cartes en nombre min du joueur qui offre
    for a in range(off):
        
    # rajouter les cartes de l'offre du joueur qui offre
    for a in range(off):




    



'''def entreeClavier() : 
    a=1
    while a == 1:
        for event in pygame.event.get():   
            if event.type == QUIT :
                a = 0							# Pour arreter le while 	
                pygame.quit()
                sys.exit()'''




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
        showCards(valueInput)

    if(valueInput == 1): # player 2
        showCards(valueInput)

    if(valueInput == 2): # player 3
        showCards(valueInput)

    if(valueInput == 3): # player 4
        showCards(valueInput)


nOffreMade = 5
offreMadeM = [multiprocessing.Lock() for i in range(nOffreMade)]




def wait(joueurI):
    print ("Player ",joueurI, " is waiting")
    #the normal program executes without blocking. here just counting up
    time.sleep(5)
    print ("Player ",joueurI, " is not waiting anymore")

def madeOffer(joueurI):
    print ("Player ",joueurI, " is making an offer")
    time.sleep(10)

    off = j.maxCardsEg(joueurI)    # make the offer
    queueQ.enqueue(off)          # put the offer in the queue
    print("The queue AVEC OFF EN PLUS : ", queueQ.printCQueue())
    print ("Player ",joueurI, " is not making an offer anymore")

def takeOffer(joueurI):
    print ("Player ",joueurI, " is taking an offer")
    time.sleep(7)
    off = j.maxCardsEg(joueurI)    # make the offer
    # vectSplitSelfOffreId, vectSplitSelfOffreMinCardsEg, vectSplitSelfOffreTypeExchange = j.maxCardsEg(joueurI)
    j.choseToTake(off)  # take the offer
    # Exchange of cards ********** <--------------------------------------------------------------------------------------------------------------------------------------
    print("Player ",joueurI, " is not taking an offer anymore")




def play(i):
    done = True
    while done:
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
            # Show players' cards
            takeInput(i) 
            offreMadeM[offreInputTake].release()
            
        '''pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            time.sleep(5)
            done = True'''







# méthode handler qui va recevoir le signal envoyé par le processus du joueur qui gagne
def signal_handler(signum, frame):
    if signum == signal.SIGUSR1:
        for i in range(1, 5):
            os.kill(childPID[i], signal.SIGKILL)
            print("Die")







if __name__ == '__main__':
    manager = Manager()


    '''objCards = Cards() 
    objDeck = Deck() 
    
    deckOrigin = objDeck.mycardset 
    # print('\n Cards: \n', deckOrigin) 
    
    objShuffleCards = ShuffleCards() 
    
    deckShuffled = objShuffleCards.shuffle() 
    # print('\n Cards Shuffled : \n', deckShuffled) 
    
    # ***********************************



    # for i in range(19):     # To have access to the two parts separately
    deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
    deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]'''
    

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
 
    
    data_ready = multiprocessing.Event() # <- à verifier
 
    '''# Who want to start
    valueInput = input("Who want to start?")
    queue.put(valueInput)

    # Show players' cards
    takeInput(int(valueInput))'''




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
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(440+100*i,733))
        elif i<10:										# Joueur 2
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(1110,109+130*(i-5)))
        elif i<15:										# Joueur 3
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(440+100*(i-10),5))
        elif i<20:										# Joueur 4
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(170,109+130*(i-15)))
        '''else:											# OFFRE
            image= str(0) + ".png"
            uno = pygame.image.load(image).convert()
            fenetre.blit(uno,(440+100*(i-20),553))'''
    
    # updates the frames of the game
    pygame.display.update()
    # pygame.display.flip()
    
    # ************************************************************************************************

    '''t3=Thread(target=entreeClavier,args=()) # VERIFIER 
    t3.start()
    t3.join()'''

    # tableau des adresses des processus
    global childPID
    childPID = []
    childPID[0] = None


    # Start + order of process
    a = 1
    for p in players:
        # Card assignment
        giveCards(j)
        p.start()
        childPID[a] = p.pid
        a += 1 # pour que le numéro du joueur corresponde à sa case d'indice du tableau
    for p in players:
        p.join()



    time.sleep(30)  # time after end processus
    
    # Affichage des résultats
    


    # TEST
    print("The points : ", points)
    
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