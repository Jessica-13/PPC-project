#!/usr/bin/env python3

# Def.

import sysv_ipc
from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer
import pygame
from pygame.locals import *
import random
import multitimer
import sys 
import os
from pygame import mixer




mutexPioche = multiprocessing.Lock()		# si on prend une carte elle n'est plus accessible
# mutexQueue = multiprocessing.Lock()
mutexAffichage = multiprocessing.Lock()		# Affichage main


white = (255, 255, 255) 
black= (0, 0,0) 
#X=1920
#Y=1080
X=1380
Y=868
 


pygame.init() 	# Initialisation fenêtre de jeu
mixer.init()	# Initialisation musique

font = pygame.font.Font('freesansbold.ttf', 50)	# Pour le message alla fin



fenetre = pygame.display.set_mode((X, Y), RESIZABLE)
fond = pygame.image.load("fond.png").convert()
fenetre.blit(fond,(0,0))



# son = pygame.mixer.Sound("son.wav")
mixer.music.load("musique.mp3")
mixer.music.play(loops=-1)




# Clé
key =int(random.random()*1000)
cle = key +1 
# Message queue
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
aff = sysv_ipc.MessageQueue(cle, sysv_ipc.IPC_CREAT)



class Joueur:
	def __init__(self, identifiant, l):
		self.identifiant=identifiant
		self.main= l
	def ajouterCarte (self,carte):
		self.main.append(carte)

class Carte:
	def __init__(self, val, couleur):
		self.couleur=couleur
		self.valeur = val



# Définition des cartes que les joueurs ont au début du jeu
# Assigner les cartes aux joueurs
def piocher(j): # Permet à un joueur de piocher une carte
	mutexPioche.acquire()						# on block le paquet pour prendre les cartes 
	#son.play() # quand on prend les cartes/pas necessarie
	a = int(random.random() * (len(pioche)))		# on prend une carte random
	j.ajouterCarte(pioche[a])					# main 
	del pioche[a]								# on enleve cette carte
	mutexPioche.release()						# on release le paquet
	# afficherMain(j)
	faireOffre(j)
	


# Offre
'''
def faireOffre(j):
	mutexPioche.acquire() 

	a=int(random.random() * (len(pioche)))
	j.ajouterCarte(pioche[a])
	del pioche[a]
	mutexPioche.release()
	# afficherMain(j)
'''

''' TRY
def faireOffre(j):
	print("Main :%s" % (j.main))
	print("Valeur : ", carte=j.main[1])
'''


def entreeClavier() : 
	a=1
	#Cette fonction vérifie les différentes entrées du clavier et envoie un signal aux process joueur concernés, indiquant quelle carte il devra jouer
	#Par exemple une touche correspondra a une carte d'un joueur, cette finction sera multithreadé
	while a ==1:
		for event in pygame.event.get():   
			if event.type == KEYDOWN and event.key == K_1:
				message="1"					# verifier signification message
				message=message.encode()
				mq.send(message, type=5)	# verifier type?
			if event.type == KEYDOWN and event.key == K_2:
				message="2"					#
				message=message.encode()
				mq.send(message, type=5)	#
			if event.type == KEYDOWN and event.key == K_3:
				message="3"					#
				message=message.encode()
				mq.send(message, type=5)	#
			if event.type == KEYDOWN and event.key == K_4:
				message="4"					#
				message=message.encode()
				mq.send(message, type=5)	#
			if event.type == KEYDOWN and event.key == K_5:
				message="5"					#
				message=message.encode()
				mq.send(message, type=5)	#
			if event.type == QUIT :
				a=0							#
				pygame.quit()
				sys.exit()





def jouer(j) : 	
	z= multitimer.MultiTimer(interval =10, function=piocher, kwargs = {"j":j}, runonstart=False)
	z.start()
	m, t=mq.receive(type=4 +j.identifiant)		# verifier type ?
	
	'''
	numero = int(m.decode())
	if numero<len(j.main):
		z.stop()
		carte=j.main[numero]
		message = str(j.identifiant) + ":" + str(carte.valeur) + ":" + carte.couleur
		msg= str(message).encode()
		mutexQueue.acquire()
		mq.send(msg, type=1)
		m, t =mq.receive(type= 1+j.identifiant)
		mutexQueue.release()
		b = int(m.decode())
		if b==1:
			j.main.remove(carte)
		else : 
			piocher(j)
	if (len(j.main)==0):
			msg = str(j.identifiant)
			msg=msg.encode()
			mq.send(msg, type=4)
	'''
	# afficherMain(j)

# DEFINIR L'ECHANGE 
# def is_valid(): 

# ===> DEFNIR SI QUELQU'UN À GAGNÉ 
# envoyer le signal pour arreter le jeu


# MODIFIER !!!!!!!!!!!!!!!!!!!!!!!!!!!
def afficherMain(j):
	message = " "
	message = message.encode()
	aff.send(message, type = 3 + j.identifiant)
	for i in range(len(j.main)):
		message = str(j.main[i].valeur) + ":" + str(j.main[i].couleur) + ":"+ str(i)
		message = message.encode()
		mutexAffichage.acquire()
		aff.send(message, type = j.identifiant)
		mutexAffichage.release()
# Par rapport à la touche 1/2/3/4/5

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
		'''
		if t==5 : 	# CAS PARTICULIER : 4
			image = "fondnoirbas.jpg"
			uno = pygame.image.load(image).convert()
			fenetre.blit(uno,(0,0))
			pygame.display.update()
		if t==6:  	# CAS PARTICULIER : 5
			image = "fondnoirbas.jpg"
			uno = pygame.image.load(image).convert()
			fenetre.blit(uno,(0,880))
			pygame.display.update()
		if t==7: 	# CAS PARTICULIER : 6
			a=0
		if t==8: 	# CAS PARTICULIER : 7
			a=0
			msg=""
			msg=msg.encode()
			mq.send(msg, type=10)
			mq.send(msg, type=11)
		'''




# 
def fgamer(j):
	a = 1
	for i in range(5):		# Prend 5 cartes
		piocher(j)			# fonction pour piocher les cartes
	# afficherMain(j)
	
	# MODIFIER !!!!!!!!!!!!!!!!!!!!!!!!!!!
	while a==1 :
		''' EXEPTION
		try:
			m, t = mq.receive(block=False, type = 9+j.identifiant)
			if t == 9+j.identifiant:
				a = 0
			break 
		except sysv_ipc.BusyError:
			print("")
		'''
		jouer(j)



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
	# if n == 3:
	#	message = "Partie terminée! Ex-aequo !"
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
		pioche = manager.list()    # Création d'une liste partagée représentant la pioche, pour que ça soit commune à tous les joueurs

		for i in range(5):
			pioche.append(Carte(3, "Velo"))			# Points : 3
			pioche.append(Carte(7, "Voiture"))		# Points : 7
			pioche.append(Carte(9, "Tracteur"))		# Points : 9
			pioche.append(Carte(13, "Autobus"))		# Points : 13

		


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
		# t2 = Thread(target=finPartie, args=())

		t3=Thread(target=entreeClavier,args=())
		# t4= Thread(target=is_valid, args=())
		
		
		p1.start()

		t.start()
		# t2.start()

		p2.start()

		t3.start()
		# t4.start()

		p3.start()
		p4.start()



		t3.join()
		t.join()
		# t2.join()
		p1.join()	# joueur 1
		p2.join()	# joueur 2
		p3.join()	# joueur 3
		p4.join()	# joueur 4
		# t4.join()