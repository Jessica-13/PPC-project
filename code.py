#!/usr/bin/env python3

# CODE MAIN

import sysv_ipc
from multiprocessing import Process, Manager, Value
import multiprocessing
from threading import Thread,Timer
import pygame
from pygame.locals import *
from random import *
import sys 
from pygame import mixer




mutexPioche = multiprocessing.Lock()		# si on prend une carte elle n'est plus accessible
mutexQueue = multiprocessing.Lock()
mutexAffichage = multiprocessing.Lock()		# Affichage main


white = (255, 255, 255) 
black= (0, 0,0) 

# fenetre resolution
X=1380	# width
Y=868	# height

 
lRandom = [] 		# Pour random
okTest = True

pygame.init() 	# Initialisation fenêtre de jeu
mixer.init()	# Initialisation musique

font = pygame.font.Font('freesansbold.ttf', 50)	# Pour le message alla fin

smallfont = pygame.font.SysFont('Corbel',35)	## defining a font


fenetre = pygame.display.set_mode((X, Y), RESIZABLE)

# fills the screen with a color
fenetre.fill((60,25,60))



# son = pygame.mixer.Sound("son.wav")
mixer.music.load("musique.mp3")
mixer.music.play(loops=-1)



# Clés
key =int(random()*1000)
cle = key +1 
# Message queue
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
aff = sysv_ipc.MessageQueue(cle, sysv_ipc.IPC_CREAT)


# Définition du joueur 
class Joueur:
	def __init__(self, identifiant, l):
		self.identifiant=identifiant
		self.main= l
	def ajouterCarte (self,carte):
		self.main.append(carte)

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


# Définition des cartes que les joueurs ont au début du jeu : assigner les cartes aux joueurs






# Offre



def entreeClavier() : 
	#Cette fonction vérifie les différentes entrées du clavier et envoie un signal aux process joueur concernés, indiquant quelle carte il devra jouer
	#Par exemple une touche correspondra a une carte d'un joueur, cette finction sera multithreadé
    a=1
    while a == 1:
        for event in pygame.event.get():   
            if event.type == KEYDOWN and event.key == K_3:
                message="3"					# quelle carte
                message=message.encode()
                mq.send(message, type=5)	# joueur 1 / type 5
            if event.type == KEYDOWN and event.key == K_5:
                message="5"					
                message=message.encode()
                mq.send(message, type=5)	
            if event.type == KEYDOWN and event.key == K_7:
                message="7"					
                message=message.encode()
                mq.send(message, type=5)	
            if event.type == KEYDOWN and event.key == K_9:
                message="9"					
                message=message.encode()
                mq.send(message, type=5)	
            if event.type == KEYDOWN and event.key == K_0:
                message="0"					# aucune
                message=message.encode()
                mq.send(message, type=5)	
            # **************************************************
            if event.type == KEYDOWN and event.key == K_3:
                message="3"					
                message=message.encode()
                mq.send(message, type=6)	# joueur 2 / type 6
            if event.type == KEYDOWN and event.key == K_5:
                message="5"					
                message=message.encode()
                mq.send(message, type=6)	
            if event.type == KEYDOWN and event.key == K_7:
                message="7"					
                message=message.encode()
                mq.send(message, type=6)	
            if event.type == KEYDOWN and event.key == K_9:
                message="9"					
                message=message.encode()
                mq.send(message, type=6)	
            if event.type == KEYDOWN and event.key == K_0:
                message="0"					
                message=message.encode()
                mq.send(message, type=6)	
            # **************************************************
            if event.type == KEYDOWN and event.key == K_3:
                message="3"					
                message=message.encode()
                mq.send(message, type=7)	# joueur 3 / type 7
            if event.type == KEYDOWN and event.key == K_5:
                message="5"					
                message=message.encode()
                mq.send(message, type=7)	
            if event.type == KEYDOWN and event.key == K_7:
                message="7"					
                message=message.encode()
                mq.send(message, type=7)	
            if event.type == KEYDOWN and event.key == K_9:
                message="9"					
                message=message.encode()
                mq.send(message, type=7)	
            if event.type == KEYDOWN and event.key == K_0:
                message="0"					
                message=message.encode()
                mq.send(message, type=7)	
            # **************************************************
            if event.type == KEYDOWN and event.key == K_3:
                message="3"					
                message=message.encode()
                mq.send(message, type=8)	# joueur 3 / type 8
            if event.type == KEYDOWN and event.key == K_5:
                message="5"					
                message=message.encode()
                mq.send(message, type=8)	
            if event.type == KEYDOWN and event.key == K_7:
                message="7"					
                message=message.encode()
                mq.send(message, type=8)	
            if event.type == KEYDOWN and event.key == K_9:
                message="9"					
                message=message.encode()
                mq.send(message, type=8)	
            if event.type == KEYDOWN and event.key == K_0:
                message="0"					
                message=message.encode()
                mq.send(message, type=8)	
            # **************************************************
            if event.type == KEYDOWN and event.key == K_3:
                message="3"					
                message=message.encode()
                mq.send(message, type=9)	# joueur 4 / type 9
            if event.type == KEYDOWN and event.key == K_5:
                message="5"					
                message=message.encode()
                mq.send(message, type=9)	
            if event.type == KEYDOWN and event.key == K_7:
                message="7"					
                message=message.encode()
                mq.send(message, type=9)	
            if event.type == KEYDOWN and event.key == K_9:
                message="9"					
                message=message.encode()
                mq.send(message, type=9)	
            if event.type == KEYDOWN and event.key == K_0:
                message="0"					
                message=message.encode()
                mq.send(message, type=9)	
            # **************************************************
            if event.type == QUIT :
                a = 0							# Pour arreter le while 
                pygame.quit()
                sys.exit()



def jouer(j) : 	
    # objShuffleCards.popCard()    # Removing a card from the deck
	m, t = mq.receive(type = 4 + j.identifiant)
	numero = int(m.decode())    # quelle carte il faut prendre <- touche appuyée
	if numero<len(j.main):      # si on a bien encore des cartes
		carte = j.main[numero]  # on prend donc la carte
		message = str(j.identifiant) + ":" + str(carte.valeur) + ":" + carte.couleur    # message avec les info
		msg = str(message).encode()
		mutexQueue.acquire()
		mq.send(msg, type = 1)      # message envoyé
		m, t = mq.receive(type= 1 + j.identifiant)  # ?
		mutexQueue.release()
		b = int(m.decode())
		if b==1:
			j.main.remove(carte)    # ! on enleve la carte car c'est bon (cela quand on accepte l'offre)
		# else : 
			# pass
            # il faut passer le tour
	if (len(j.main)==0):        # si on n'a plus de cartes
			msg = str(j.identifiant)
			msg = msg.encode()
			mq.send(msg, type = 4)      # on a gagné
	afficherMain(j)


# DEFINIR L'ECHANGE 
def is_valid(): 
    a = 1
    mutexPioche.acquire()
    b = int(random.random() * (len(pioche)))
    carteActu=pioche[b]
    del pioche[b]
    mutexPioche.release()
	
    while a == 1:
        mutexAffichage.acquire()
        x = str(carteActu.valeur)
        image = x + ":" + carteActu.couleur + ":" + "8"
        image = image.encode()
        aff.send(image, type=3)
        mutexAffichage.release()
        resultat  =0
        m, t = mq.receive(type = 1)
        message = m.decode()
        message = message.split(":")
        identifiant = int(message[0])
        carte = Carte(int(message[1]), message[2])
        if (carte.couleur == carteActu.couleur and carte.valeur%10==(carteActu.valeur+1)%10) or (carte.couleur == carteActu.couleur and carte.valeur%10==(carteActu.valeur-1)%10) or (carte.valeur==carteActu.valeur):
            resultat = 1
            carteActu=Carte(carte.valeur, carte.couleur)
            
        msg = str(resultat).encode()
        mq.send(msg, type = identifiant+1)


# ===> SI QUELQU'UN À GAGNÉ 
# envoyer le signal pour arreter le jeu
# faire donc sonner la cloche (musique + changer l'image avec clocheSonne.jpg)


# def afficherMain(j):


# MODIFIER !!!!!!!!!!!!!!!!!!!!!!!!!!!
def afficher():
	a=1
	while a==1:
		m,t = aff.receive()		# le message + identifiant joueur
		message = m.decode()
		message = message.split(":")
		if t==1:				# Joueur 1
			image= message[0] + " " + message[1] + ".png"	# valeur + couleur
			uno = pygame.image.load(image).convert()
			i = int(message[2])
			fenetre.blit(uno,(440+100*i,733))
			pygame.display.update()

		if t==2:				# Joueur 2
			image= message[0] + " " + message[1] + ".png"	# valeur + couleur
			uno = pygame.image.load(image).convert()
			i = int(message[2])
			fenetre.blit(uno,(1095,109+130*(i-5)))
			pygame.display.update()

		if t==3:				# Joueur 3
			# son.play()	# quand on prend les cartes/pas necessarie
			image= message[0] + " " + message[1] + ".png"	# valeur + couleur
			uno = pygame.image.load(image).convert()
			i = int(message[2])
			fenetre.blit(uno,(440+100*(i-10),5))
			pygame.display.update()

		if t==4:				# Joueur 4
			image= message[0] + " " + message[1] + ".png"	# valeur + couleur
			uno = pygame.image.load(image).convert()
			i = int(message[2])
			fenetre.blit(uno,(155,109+130*(i-15)))
			pygame.display.update()


		# A CHOISIR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		# Ajouter la partie avec l'offre
	     


# 
def fgamer(j):
	'''
	for i in range(5):		# Prend 5 cartes
		piocher(j)			# fonction pour piocher les cartes
	'''
	# afficherMain(j)
	
	# MODIFIER !!!!!!!!!!!!!!!!!!!!!!!!!!!
	while True :
		''' EXEPTION
		try:
			m, t = mq.receive(block=False, type = 9+j.identifiant)
			if t == 9+j.identifiant:
				a = 0
			break 
		except sysv_ipc.BusyError:
			print("")
		'''
		# jouer(j)



def finPartie():
	a = True
	m,t = mq.receive(type = 4)		# ASSIGNER !!!
	m = m.decode()
	n = int(m)
	if(t == 4):						# ASSIGNER !!!
		print("Fin de Partie!")
		msg = ""
		msg = msg.encode()
		aff.send(msg, type = 6)		# ASSIGNER !!!
		mq.send(msg, type = 10)		# ASSIGNER !!!
		mq.send(msg, type = 11)		# ASSIGNER !!!
	else:
		message = "Le joueur " + m + " a gagné ! "
	text = font.render(message, True, white, black)		# Format du texte
	textRect = text.get_rect() 
	textRect.center = (X // 2, Y // 2) 					# Position du texte
	while a : 
		fenetre.fill(black) 
		fenetre.blit(text, textRect)  
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 				# Pour terminer le jeu
				a = False
				pygame.quit() 
				sys.exit() 
			pygame.display.update() 



if __name__ == '__main__':
	with Manager() as manager:
		# ***********************************
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
			# print("Val : ", deckShuffledSplitValues[i], " Famille : ", deckShuffledSplitSuites[i])
			

		offre = manager.list()


		# Disposition cartes dans la fenêtre de jeu
		# Cloche
		uno = pygame.image.load("cloche.jpg").convert()
		fenetre.blit(uno,(645,389))
		pygame.display.update()

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
			else:											# OFFRE
				image= str(0) + ".png"
				uno = pygame.image.load(image).convert()
				fenetre.blit(uno,(440+100*(i-20),553))
		
		# updates the frames of the game
		pygame.display.update()


		# Dèfinition joueurs
		j1= Joueur(1,[])
		p1= Process(target=fgamer, args=(j1,))

		j2= Joueur(2,[])
		p2= Process(target=fgamer, args=(j2,))

		j3= Joueur(3,[])
		p3= Process(target=fgamer, args=(j3,))

		j4= Joueur(4,[])
		p4= Process(target=fgamer, args=(j4,))
		
		# ***
		t = Thread(target=afficher, args=())

		t3=Thread(target=entreeClavier,args=())
		
		
		p1.start()

		t.start()

		p2.start()

		t3.start()


		p3.start()
		p4.start()

		t3.join()
		t.join()

		p1.join()	# joueur 1
		p2.join()	# joueur 2
		p3.join()	# joueur 3
		p4.join()	# joueur 4