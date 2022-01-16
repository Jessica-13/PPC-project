#!/usr/bin/env python3
'''
import sysv_ipc
from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer
# import pygame
# from pygame.locals import *
import random
# import multitimer
import sys 
'''

import numpy as np
import random

nbJoueurs = 10

# définition famille des cartes
noms_couleurs = []
noms_valeurs = []

class Card:
    # Représente une carte à jouer standard
    def __init__(self, couleur, valeur, noms_couleurs, noms_valeurs):
        self.couleur = couleur
        self.valeur = valeur
        self.noms_couleurs = noms_couleurs
        self.noms_valeurs = noms_valeurs
        
    # Initialisation du jeu : création du fichier avec les autant de moyens de transport que de joueurs
    with open("transports.txt", "r") as fichier1, open("transportsJEU.txt", "w") as fichier2:
        ligne = fichier1.readline()
        i = 0
        while ligne != "" and i<nbJoueurs:
            for index in range(5):
                fichier2.write(f"{ligne}")
            ligne = fichier1.readline()
            i+=1

    with open("transportsJEU.txt", "r") as filin:
        for ligne in filin:
            # Créer la liste avec toutes les cartes : on prend le fichier txt (liste de tous les moyens de transport) :
            noms_couleurs.append(ligne)

    # définition points des cartes
    numPoint = 1
    for indexI in range(nbJoueurs):
        for indexJ in range(5):
            noms_valeurs.append(numPoint)
        numPoint+= 2


    # Comparer des cartes :
    def __lt__(self, other):     # operateur < , https://www.pythonpool.com/python-__lt__/
        # vérifier les couleurs
        if self.couleur < other.couleur: return True
        if self.couleur > other.couleur: return False

        # les couleurs sont identiques... vérifier les valeurs
        return self.valeur < other.valeur

    ''' # meme mais avec comparaison de tuple
    def __lt__(self, other):
        t1 = self.couleur, self.valeur
        t2 = other.couleur, other.valeur
        return t1 < t2
    '''

    
    # affichage carte
    def __str__(self):
        return "La famille :%s- avec les points :%d" % (self.couleur, self.valeur)



class Paquet:

    def __init__(self):
        self.cartes = []

        for c in noms_couleurs:            # nombre de familles
            for valeur in noms_valeurs:     # points de chaque familles
                carte = Card(c, valeur,noms_couleurs, noms_valeurs)
                self.cartes.append(carte)     
        
    
    # Mélanger le paquet de cartes
    def battre(self):
        np.random.shuffle(self.cartes)
    
    # Distribuer des cartes
    '''
    Comme pop retire la dernière carte dans la liste, 
    nous distribuons les cartes à partir de la fin du paquet.
    '''
    def pop_carte(self):
        return self.cartes.pop()

    # Ajouter une carte au paquet

    def ajouter_carte(self, carte):
        self.cartes.append(carte)

# *****************************************************************************

class Main(Paquet):
    """Représente une main au jeu de cartes."""
    def __init__(self, etiquette = ''):
            self.cartes = []
            self.etiquette = etiquette




if __name__ == '__main__':
    
    paquet = Paquet()
    print(paquet)           # TEST PAQUET

    # TEST CARD
    carte = Card('Autobus', 1, noms_couleurs, noms_valeurs)
    print(carte)

    # TEST priorité cards
    carte1 = Card('Avion', 2, noms_couleurs, noms_valeurs)
    carte2 = Card('Barque', 3, noms_couleurs, noms_valeurs)
    print(carte1<carte2)



    # TEST MAIN
    main = Main('Tas 1')    # Changer l'etiquette du main
    print("Joueur :%s" % (main.etiquette))             # numero du joueur 
    paquet.battre()
    for indexTryPaquet in range(5*nbJoueurs):
        print("Carte :%s" % (paquet.cartes[indexTryPaquet]))


    ## tas = Paquet()
    for indexTas in range(5): 
        carteMain = paquet.pop_carte()
        main.ajouter_carte(carteMain)
        # print("try :%s" % (carteMain)) 
    for indexTas in range(5): 
        print("Carte :%s" % (main.cartes[indexTas]))              # Cartes de ce main


    for indexTry in range(len(noms_valeurs)):
        print(noms_valeurs[indexTry])

    
