#!/usr/bin/env python3

# Python 3
# sudo apt-get install python3-tk
# sudo apt-get install python3-pil python3-pil.imagetk

from distutils import ccompiler
from random import *

from posixpath import split

from multiprocessing import Process, Manager, Lock, Array
from random import *
import time

import signal
import os
import sysv_ipc

from player import player

# GUI *********************************************************************************************
from tkinter import *
from turtle import color         # import de tkinter
from PIL import ImageTk, Image
import os

from pygame import mixer

mixer.init()


mixer.music.load("musique.mp3")
mixer.music.play(loops=-1)



# GUI *********************************************************************************************
root = Tk() # creation of the window

# Window resolution
root.resizable(width = True, height = True)
root.geometry("1380x868")
# Set title
root.title("Cambiecolo")

root.configure(bg = 'white')

# Canva
X = 1380	# width
Y = 868     # height
canva = Canvas(root, width = X, height = Y, background="white")


# Put the bell
imgCloche = ImageTk.PhotoImage(Image.open("cloche.jpg"))
canva.create_image(645, 389, image = imgCloche)


# TEXTE WITH PLAYER NAME
canva.create_text(300, 790, text = "PLAYER 1", font = ("freesansbold.ttf", 20))
canva.create_text(1100, 780, text = "PLAYER 2", font = ("freesansbold.ttf", 20))
canva.create_text(950, 50, text = "PLAYER 3", font = ("freesansbold.ttf", 20))
canva.create_text(180, 60, text = "PLAYER 4", font = ("freesansbold.ttf", 20))


img = []
img.append(PhotoImage(file = "0.png"))
img.append(PhotoImage(file = "3.png"))
img.append(PhotoImage(file = "5.png"))
img.append(PhotoImage(file = "7.png"))
img.append(PhotoImage(file = "9.png"))

imageCart = []
for i in range(5):	
    imageCart.append(canva.create_image(430+100*i, 770, image = img[0]))
for i in range(5,10):	
    imageCart.append(canva.create_image(1110, 160+130*(i-5), image = img[0]))
for i in range(10,15):	
    imageCart.append(canva.create_image(430+100*(i-10), 90, image = img[0]))
for i in range(15,20):
    imageCart.append(canva.create_image(170, 160+130*(i-15), image = img[0]))
canva.place(x = 0, y = 0)

# GUI *********************************************************************************************

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


objCards = Cards() # ?
objDeck = Deck() # ?

deckOrigin = objDeck.mycardset 

objShuffleCards = ShuffleCards() 

deckShuffled = objShuffleCards.shuffle() 

deckShuffledSplitValues = [i.split(' ')[0] for i in deckShuffled]
deckShuffledSplitSuites = [i.split(' ')[1] for i in deckShuffled]


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

# # # ********************************************************************************************

nbPlayer = 4

def reDraw(canva):
    root.update()
    while True:
        for i in range(5):
            if playerCardsForExchange1[i] == "Velo":
                canva.itemconfig(imageCart[i], image = img[1])
            else:
                if playerCardsForExchange1[i] == "Autobus":
                    canva.itemconfig(imageCart[i], image = img[2])
                else:
                    if playerCardsForExchange1[i] == "Voiture":
                        canva.itemconfig(imageCart[i], image = img[3])
                    else:
                        if playerCardsForExchange1[i] == "Tracteur":
                            canva.itemconfig(imageCart[i], image = img[4])
                        else:
                            canva.itemconfig(imageCart[i], image = img[0])
        for i in range(5,10):
            if playerCardsForExchange2[i-5] == "Velo":
                canva.itemconfig(imageCart[i], image = img[1])
            else:
                if playerCardsForExchange2[i-5] == "Autobus":
                    canva.itemconfig(imageCart[i], image = img[2])
                else:
                    if playerCardsForExchange2[i-5] == "Voiture":
                        canva.itemconfig(imageCart[i], image = img[3])
                    else:
                        if playerCardsForExchange2[i-5] == "Tracteur":
                            canva.itemconfig(imageCart[i], image = img[4])
                        else:
                            canva.itemconfig(imageCart[i], image = img[0])
        for i in range(10,15):
            if playerCardsForExchange3[i-10] == "Velo":
                canva.itemconfig(imageCart[i], image = img[1])
            else:
                if playerCardsForExchange3[i-10] == "Autobus":
                    canva.itemconfig(imageCart[i], image = img[2])
                else:
                    if playerCardsForExchange3[i-10] == "Voiture":
                        canva.itemconfig(imageCart[i], image = img[3])
                    else:
                        if playerCardsForExchange3[i-10] == "Tracteur":
                            canva.itemconfig(imageCart[i], image = img[4])
                        else:
                            canva.itemconfig(imageCart[i], image = img[0])
        for i in range(15,20):
            if playerCardsForExchange4[i-15] == "Velo":
                canva.itemconfig(imageCart[i], image = img[1])
            else:
                if playerCardsForExchange4[i-15] == "Autobus":
                    canva.itemconfig(imageCart[i], image = img[2])
                else:
                    if playerCardsForExchange4[i-15] == "Voiture":
                        canva.itemconfig(imageCart[i], image = img[3])
                    else:
                        if playerCardsForExchange4[i-15] == "Tracteur":
                            canva.itemconfig(imageCart[i], image = img[4])
                        else:
                            canva.itemconfig(imageCart[i], image = img[0])
        root.update()






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

    with Manager() as manager:
        request = manager.list() # SHARED MEMORY
        lock = Lock()
        lockValue = Lock() # LOCK FOR VALUE
        winner = Array('i', 1) # ?
   

        print("******************** START GAME ********************")

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

        p5 = Process(target = reDraw, args=(canva, ))   # GUI

        p5.start()

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()


        # The bell ring
        # Put the bell
        imgCloche = ImageTk.PhotoImage(Image.open("clocheSonne.jpg"))
        canva.create_image(645, 389, image = imgCloche)
        root.update()

        time.sleep(5)

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

        p5.join()
        