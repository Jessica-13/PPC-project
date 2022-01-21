#!/usr/bin/env python3

# Python 3
# sudo apt-get install python3-tk
# sudo apt-get install python3-pil python3-pil.imagetk



from distutils import ccompiler
from random import *
import multiprocessing
import queue

from posixpath import split

import multiprocessing
from multiprocessing import Process, Manager, Lock, Array
from random import *
import random

import queue

import time

import signal
import os
import sysv_ipc

from player import player

import itertools


def handlerGame(sig, frame): # if SIGUSR1
    if sig == signal.SIGUSR1: 
        os.kill(p1.pid, signal.SIGUSR2) # SIGUSR1 signal send to p1
        print("KILL p1")
        os.kill(p2.pid, signal.SIGUSR2)
        print("KILL p2")
        os.kill(p3.pid, signal.SIGUSR2)
        print("KILL p3")
        os.kill(p4.pid, signal.SIGUSR2)
        print("KILL p4")






# # # Definition of the deck **********************************************************************************************************
# Definition of the "Carte" object
class Carte:
    def __init__(self, val, couleur):
        self.couleur = couleur
        self.valeur = val
        
    def __repr__(self):
        return "<Type : %s - Points :%s>" % (self.couleur, self.valeur)


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


objCards = Cards() # ?
objDeck = Deck() # ?

deckOrigin = objDeck.mycardset 

objShuffleCards = ShuffleCards() 

deckShuffled = objShuffleCards.shuffle() 

deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]
# # # ********************************************************************************************

nbPlayer = 4

'''# Definition of player 
class Joueur(multiprocessing.Process):
    def __init__(self, identifiant, l):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event() ### pour terminer - à enlever 
        self.identifiant = identifiant
        self.liste = l
    
    def __repr__(self):
        return "<Player : %s - Cards :%s>" % (self.identifiant, self.liste)'''

    
    # def maxCardsEg(self, id):
    # def choseToTake(self, id):



class return_values_nbCartesEg: # For double retourn
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c





if __name__ == '__main__':

    signal.signal(signal.SIGUSR1, handlerGame)      # signal follow handlerGame roules

    
    # messages from p1
    key1 = 100
    mq1 = sysv_ipc.MessageQueue(key1,sysv_ipc.IPC_CREAT)

    # messages from p2
    key2 = 200
    mq2 = sysv_ipc.MessageQueue(key2,sysv_ipc.IPC_CREAT)

    # messages from p3
    key3 = 300
    mq3 = sysv_ipc.MessageQueue(key3,sysv_ipc.IPC_CREAT)

    # messages from p4
    key4 = 400
    mq4 = sysv_ipc.MessageQueue(key4,sysv_ipc.IPC_CREAT)

    
    '''# Player creation ?
    j1 = Joueur(1, [])
    j2 = Joueur(2, [])
    j3 = Joueur(3, [])
    j4 = Joueur(4, [])'''

    # cards for exchange
    playerCardsForExchange1, playerCardsForExchange2, playerCardsForExchange3, playerCardsForExchange4 = list(), list(), list(), list()
    for a in range(5):
        playerCardsForExchange1.append(deckShuffledSplitSuites[a])
    for a in range(5,10):
        playerCardsForExchange2.append(deckShuffledSplitSuites[a])
    for a in range(10,15):
        playerCardsForExchange3.append(deckShuffledSplitSuites[a])
    for a in range(15,20):
        playerCardsForExchange4.append(deckShuffledSplitSuites[a])


    '''# Heap definition for each player
    for a in range(5):
        j1.liste.append(Carte(str(deckShuffledSplitValues[a]), str(deckShuffledSplitSuites[a])))
    for a in range(5,10):	
        j2.liste.append(Carte(deckShuffledSplitValues[a], deckShuffledSplitSuites[a]))
    for a in range(10,15):	
        j3.liste.append(Carte(deckShuffledSplitValues[a], deckShuffledSplitSuites[a]))
    for a in range(15,20):	
        j4.liste.append(Carte(deckShuffledSplitValues[a], deckShuffledSplitSuites[a]))'''




    with Manager() as manager:
        request = manager.list() # SHARED MEMORY
        lock = Lock()
        lockValue = Lock() # LOCK FOR VALUE
        winner = Array('i', 1) # ?
   

        print("******************** START GAME ********************")
        '''print(j1.identifiant, print(j1.liste))
        print(j2.identifiant, print(j2.liste))
        print(j3.identifiant, print(j3.liste))
        print(j4.identifiant, print(j4.liste))'''
    
        print("PLAYER 1 CARDS : ", playerCardsForExchange1)
        print("PLAYER 2 CARDS : ", playerCardsForExchange2)
        print("PLAYER 3 CARDS : ", playerCardsForExchange3)
        print("PLAYER 4 CARDS : ", playerCardsForExchange4)
       
        print()


        # PLAYERS' PROCESS
        p1 = Process(target = player, args=(playerCardsForExchange1,request,lock,mq1,mq2,mq3,mq4,lockValue,winner))
        p2 = Process(target = player, args=(playerCardsForExchange2,request,lock,mq1,mq2,mq3,mq4,lockValue,winner))
        p3 = Process(target = player, args=(playerCardsForExchange3,request,lock,mq1,mq2,mq3,mq4,lockValue,winner))
        p4 = Process(target = player, args=(playerCardsForExchange4,request,lock,mq1,mq2,mq3,mq4,lockValue,winner))

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()


        # The bell ring
        #################

        # THE WINNER IS :
        if winner[0] == p1.pid:
            print("PLAYER 1 WIN !!!")
        elif winner[0] == p2.pid:
            print("PLAYER 2 WIN !!!")
        elif winner[0] == p3.pid:
            print("PLAYER 3 WIN !!!")
        elif winner[0] == p4.pid:
            print("PLAYER 4 WIN !!!")
        else:
            print("The game ends in a draw :P ")

        mq1.remove()
        mq2.remove()
        mq3.remove()
        mq4.remove()