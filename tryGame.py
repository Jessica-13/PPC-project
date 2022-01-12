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

class Card:
    # Représente une carte à jouer standard
    def __init__(self, couleur, valeur):
        self.couleur = couleur
        self.valeur = valeur
        
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
    noms_valeurs = [None, 'as', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'valet', 'dame', 'roi']



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
        return '%s de %s' % (Card.noms_valeurs[self.valeur], noms_couleurs[self.couleur])
    


class Paquet:

    def __init__(self):
        self.cartes = []

        for c in noms_couleurs:            # nombre de familles
            for valeur in range(1, 14):     # points de chaque familles
                carte = Card(c, valeur)
                self.cartes.append(carte)        
        
    
    # Afficher le paquet : 
    def __str__(self):
        res = []
        for carte in self.cartes:
            res.append(str(carte))
        return '\n'.join(res)
    








if __name__ == '__main__':
    
    paquet = Paquet()
    print(paquet)