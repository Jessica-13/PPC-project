#!/usr/bin/env python3

# Python 3
# sudo apt-get install python3-tk
# sudo apt-get install python3-pil python3-pil.imagetk



from random import *
import multiprocessing
import queue

from posixpath import split

import multiprocessing
from multiprocessing import Process, Manager
from random import *
import random

import queue

import time



# GUI *********************************************************************************************
from tkinter import *
from turtle import color         # import de tkinter
from PIL import ImageTk, Image
import os


root = Tk() # creation of the window
# app = Frame(root)   # 

# Window resolution
root.resizable(width = True, height = True)
root.geometry("1380x868")
# Set title
root.title("Cambiecolo")


root.configure(bg = 'white')

# Disposition cartes dans la fenêtre de jeu
# Cloche





# Canva
X = 1380	# width
Y = 868     # height
canva = Canvas(root, width = X, height = Y, background="white")


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
# set first image on canvas
# img0 = canva.create_image(0, 0, image = img[0])



# Show the player's cards
# img0 = ImageTk.PhotoImage(Image.open("0.png"))
# img = str(deckShuffledSplitValues[i]) + ".png"
for i in range(5):	
    # Show player j1's cards
    imageCart.append(canva.create_image(430+100*i, 770, image = img[0]))
    # canva.create_image(430+100*i, 770, image = img0)
for i in range(5,10):	
    # Show player j2's cards
    imageCart.append(canva.create_image(1110, 160+130*(i-5), image = img[0]))
    # canva.create_image(1110, 160+130*(i-5), image = img0)
for i in range(10,15):	
    # Show player j3's cards
    imageCart.append(canva.create_image(430+100*(i-10), 90, image = img[0]))
    # canva.create_image(430+100*(i-10), 90, image = img0)
for i in range(15,20):
    # Show player j4's cards
    imageCart.append(canva.create_image(170, 160+130*(i-15), image = img[0]))
    # canva.create_image(170, 160+130*(i-15), image = img0)
canva.place(x = 0, y = 0)


# GUI *********************************************************************************************

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
            if (id == 0):
                for i in range(5):
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        #showCards(id)
            if (id == 1):
                for i in range(5,10):	
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        #showCards(id)
            if (id == 2):
                for i in range(10,15):	
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        #showCards(id)
            if (id == 3):
                for i in range(15,20):	
                    if deckShuffledSplitValues[i] == typeExchange: 
                        deckShuffledSplitValues[i] = bb
                        deckShuffledSplitSuites[i] = cc
                        #showCards(id)
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



def reDraw(canva):
    time.sleep(5)
    for i in range(20):
        if deckShuffledSplitValues[i] == "3":
            canva.itemconfig(imageCart[i], image = img[1])
        else:
            if deckShuffledSplitValues[i] == "5":
                canva.itemconfig(imageCart[i], image = img[2])
            else:
                if deckShuffledSplitValues[i] == "7":
                    canva.itemconfig(imageCart[i], image = img[3])
                else:
                    if deckShuffledSplitValues[i] == "9":
                        canva.itemconfig(imageCart[i], image = img[4])
                    else:
                        canva.itemconfig(imageCart[i], image = img[0])
    root.update()


'''
    for i in range(5):	
        # print("ICIIIIIIII ", deckShuffledSplitValues[i])
        # Show player j1's cards
        # img1 = ImageTk.PhotoImage(Image.open(str(deckShuffledSplitValues[i]) + ".png"))
        # change image
        if deckShuffledSplitValues[i] == 3:
            canva.itemconfig(imageCart[i], image = img[1])
        else:
            if deckShuffledSplitValues[i] == 5:
                canva.itemconfig(imageCart[i], image = img[2])
            else:
                if deckShuffledSplitValues[i] == 7:
                    canva.itemconfig(imageCart[i], image = img[3])
                else:
                    if deckShuffledSplitValues[i] == 9:
                        canva.itemconfig(imageCart[i], image = img[4])
                    else:
                        canva.itemconfig(imageCart[i], image = img[0])
        
        # canva.create_image(440+100*i, 733, image = img[int(int(deckShuffledSplitValues[i])/2)-1])
        #print(img1.__str__())
    for i in range(5,10):	
        # Show player j2's cards
        if deckShuffledSplitValues[i] == 3:
            canva.itemconfig(imageCart[i], image = img[1])
        else:
            if deckShuffledSplitValues[i] == 5:
                canva.itemconfig(imageCart[i], image = img[2])
            else:
                if deckShuffledSplitValues[i] == 7:
                    canva.itemconfig(imageCart[i], image = img[3])
                else:
                    if deckShuffledSplitValues[i] == 9:
                        canva.itemconfig(imageCart[i], image = img[4])
                    else:
                        canva.itemconfig(imageCart[i], image = img[0])
        # img2 = ImageTk.PhotoImage(Image.open(str(deckShuffledSplitValues[i]) + ".png"))
        # canva.create_image(1110, 109+130*(i-5), image = img[int(int(deckShuffledSplitValues[i])/2)-1])
    for i in range(10,15):	
        # Show player j3's cards
        if deckShuffledSplitValues[i] == 3:
            canva.itemconfig(imageCart[i], image = img[1])
        else:
            if deckShuffledSplitValues[i] == 5:
                canva.itemconfig(imageCart[i], image = img[2])
            else:
                if deckShuffledSplitValues[i] == 7:
                    canva.itemconfig(imageCart[i], image = img[3])
                else:
                    if deckShuffledSplitValues[i] == 9:
                        canva.itemconfig(imageCart[i], image = img[4])
                    else:
                        canva.itemconfig(imageCart[i], image = img[0])
        # img3 = ImageTk.PhotoImage(Image.open(str(deckShuffledSplitValues[i]) + ".png"))
        # canva.create_image(440+100*(i-10), 5, image = img[int(int(deckShuffledSplitValues[i])/2)-1])
    for i in range(15,20):
        # Show player j4's cards
        if deckShuffledSplitValues[i] == 3:
            canva.itemconfig(imageCart[i], image = img[1])
        else:
            if deckShuffledSplitValues[i] == 5:
                canva.itemconfig(imageCart[i], image = img[2])
            else:
                if deckShuffledSplitValues[i] == 7:
                    canva.itemconfig(imageCart[i], image = img[3])
                else:
                    if deckShuffledSplitValues[i] == 9:
                        canva.itemconfig(imageCart[i], image = img[4])
                    else:
                        canva.itemconfig(imageCart[i], image = img[0])
        # img4 = ImageTk.PhotoImage(Image.open(str(deckShuffledSplitValues[i]) + ".png"))
        # canva.create_image(170, 109+130*(i-15), image = img[int(int(deckShuffledSplitValues[i])/2)-1])
'''


def showTerminal(identity):    
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
def takeInput(valueInput):
    if(valueInput == 0): # player 1
        root.update()
        reDraw(valueInput)

    if(valueInput == 1): # player 2
        root.update()
        reDraw(valueInput)

    if(valueInput == 2): # player 3
        root.update()
        reDraw(valueInput)

    if(valueInput == 3): # player 4
        root.update()
        reDraw(valueInput)
'''


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
            showTerminal(i)   
            # *** print("Offre board : ", offre)
            madeOffer(i)    #
            offreMadeM[offreInputMade].release()
        else :
            offreMadeM[offreInputTake].acquire()
            takeOffer(i)    #
            # Show players' cards
            showTerminal(i) 
            offreMadeM[offreInputTake].release()

# on affiche enfin la fenêtre principal et on attend les événements (souris, clic, clavier)
# root.mainloop ()  
# root.update()








if __name__ == '__main__':
    manager = Manager()     #####

    
    nb_players = 4
    for i in range(nb_players):
        # Player creation
        j = Joueur(i,[])

    # on définit le processus principale
    players = [multiprocessing.Process(target=play, args = (i, ))for i in range (nb_players)]
    
    # Creation of a list managed by the manager, to add points
    points = manager.list() ###

    # Creation of a list managed by the manager to add the current offer
    offre = manager.list()  ###
    
    # Main process
    print("Starting main process:", multiprocessing.current_process().name)

    # Start + order of process
    for p in players:
        # Card assignment
        giveCards(j)
        p.start()
    '''for p in players:
        p.join()'''
    # voir pour la fin 


    # showCards(canva)

    # time.sleep(30)  # time after end processus
    
    while True: 
        root.update()
        reDraw(canva)

    # TEST
    print("The points : ", points)
    
    # Main process
    print("Ending process:", multiprocessing.current_process().name)