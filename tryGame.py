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
        return "La famille :%s - avec les points :%s" % (self.couleur, self.valeur)



class Paquet:

    def __init__(self):
        self.cartes = []

        for c in noms_couleurs:            # nombre de familles
            for valeur in noms_valeurs:     # points de chaque familles
                carte = Card(c, valeur,noms_couleurs, noms_valeurs)
                self.cartes.append(carte)     







if __name__ == '__main__':
    
    paquet = Paquet()
    print(paquet)           # TEST PAQUET

    # TEST CARD
    carte = Card('Autobus', 1, noms_couleurs, noms_valeurs)
    print(carte)

    