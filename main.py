#!/usr/bin/env python3

# main Cambiecolo 

# --- Structure du programme --- #

'''
# Définition méthode pour déterminer le plus grand nombre de cartes identiques

class return_values_nbCartesEg:
    def __init__(self, a, b):
    self.a=a
    self.b=b

def nbCartesEg(a):
    max = 0
    indice = -1     # pour pouvoir retrouver aussi le cas 0
    for j in range (i.cartes[]):
        counted = i.cartes[].count(i.cartes[j])
        if (max < counted) && (i.cartes[indice].nom != i.cartes[j].nom) :
            max = counted
            indice = j
        elif (compte == max)
            if (i.cartes[j].points > i.cartes[indice].points):
            indice = j

    t=return_values (max, indice)
    return t


# Définition méthode pour trouver les priorités choix offre : 

def priorités(i) :

## compter le nombre de cartes identiques
    x =nbCartesEg(i)    # appel à nbCartesEg()

### Il faudrait considérer les cas où il y a plusieurs joueurs qui gagnent au même moment (c’est-à-dire plusieurs joueurs qui ont déjà 5 cartes égales au début du jeu / deux joueurs qui échangent leurs cartes et ils complètent leur famille)

    # cas où il y a les 5 cartes identiques
    if x.a == 5 :
        i.points = i.cartes[x.b].points
        famille = i.cartes[x.b].nom
        cloche = True 
        -> option: envoyer un signal qui kill le programme
        -> ajouter un Print avec le numéro du joueur qui a gagné, la famille qu’il a complétée et les points qu’il a fait.

## partie pour déterminer les cartes restantes identiques
    maxOffre = 0
    indiceOffre = -1
    for m in range (cartes[]) :
        if (i.cartes[m].nom != i.cartes[x.b].nom) :
            compte = i.cartes[].count(i.cartes[m])
        if ( compte > maxOffre):
            maxOffre = compte
            indiceOffre = m
        if (compte == maxOffre)&&(i.cartes[m].points < i.cartes[indiceOffre].points):
            indiceOffre = m

## création et remplissage liste avec les cartes à donner
    offre [] -> liste
    for a in range(maxOffre):
        offre[a] <- i.cartes[indiceOffre] // [b|<-] [b|<-] [b|null]
        return offre[]


# Définition méthode exchange : 
    def echange(offrei, offrem) :
        -> offre[i] ***échangé avec*** offre[m]
        -> enlever les cartes à offrir dans la liste des cartes du joueur
        -> ajouter les cartes acceptées dans la liste des cartes du joueur


# Initialisations des 3 états :
    ## En attente d’offres : 
    def enAttente(i) :     // i étant l’indice du joueur
        etatEnAttente = True
        Print ( Le joueur player(i) est en attente)

    ## En phase de proposition d’offre : 
    def propositionOffre(i):
        etatEnAttente = False
        Print ( Le joueur player(i) est en train de faire une proposition)

    ## En train de regarder quel offre accepter : 
    def examinationOffre(i):
        etatEnAttente = False
        Print ( Le joueur player(i) est en train d’examiner les offres disponibles)


# Définition structure d’une carte : 
    structure cartes(nom + points)  









# --- *** Joueur *** --- #

def joueur(i) : 
    while(cloche==False)
        if (compteurNbPropMTemps < nbPropMTemps && etatEnAttente)
        # on détermine qui doit faire un offre et qui l’accepter :
            if( random(0,1) == 1)(entre le nbJoueurs pour voir qui tire le dé)
                -> si le joueur a eu 1 -> commence à jouer 
                -> il est mis dans l’état propositionOffre() 
                -> appelle à la méthode priorites() 
                -> on obtient offre[i] 
                -> compteurNbPropMTemps += 1
            else
                -> si player a eu 0 -> il peut faire un offre 
                -> il est mis dans l’état examinationOffre() 
                -> appelle à la méthode priorites() 
                -> on obtient offre[i] 
                -> offre[i].acquire()
        
            for(m in nbJoueurs) :
                if(m==i) 
                    pass

                offre[m].acquire()  # pour dire que le joueur bloque l’offre car il est en train de choisir s’il l’accepte ou pas
                if(length(offre[i]) == length(offre[m]))
                    -> appelle à la méthode echange(offre[i],offre[m]) 
                    -> compteurNbPropMTemps -= 1
                    -> Print (“Le joueur player(i) a accepté l’offre du joueur player(m). Ils ont echangés length(offre[i]) cartes.”)
                    enAttente(i)
                    enAttente(m)
                    set offre[i] == null
                    set offre[m] == null
                    break
                else 
                    offre[m].release() # si le joueur(m) n’accepte pas l’offre

            enAttente(i)            # si le joueur(m) a accepté l’offre, alors le joueur(i) peut retourner à joueur aussi  
            offre[i].release()      # pour libérer la place
            offre[m].release()      # pour libérer la place









# --- *** global *** --- #

offre = [multiprocessing.Lock() for i in range (nbPropMTemps)]

-> Initialisation global cloche : type booléen

# Initialisation d’un compteur pour avoir trace du nombre de offre qui on été faites jusqu’à ce moment:

compteurNbPropMTemps = 0
boolean etatEnAttente = False




"""
++ partie interaction user (propositions)

Afficher cartes du joueur actuel
Afficher les offres disponibles (nb de cartes) (elles doivent évoluer en direct en fonction des autres joueurs qui jouent)
Choisir propositionOffre() ou examinationOffre()?
Choisir manuellement les cartes qu’on peut donner
Choisir éventuellement l’offre qu’on veut prendre
"""


'''


import numpy as np
import multiprocessing
import random




if __name__ == "__main__":
    # Initialisation du jeu : charger le fichier avec les moyens de transport

    f = open('transports.txt', 'r')  # pour ouvrir le fichier

    # Créer la liste avec toutes les cartes : on prend le fichier txt (liste de tous les moyens de transport) :

    g = np.genfromtxt(fname='transports.txt')    # pour prendre les valeurs


    # Prendre en input le nombre de joueur :

    nbJoueurs = input('Entrez le nombre de joueurs: ')

    while ( nbJoueurs  < 2)     # pas assez pour jouer
        nbJoueurs = input("Entrez le nombre de joueurs: ")
        if nbJoueurs == 0 : 
            print("Valeur pas bonne car on peut pas jouer s’il n’y a pas de joueurs.")
            # on retour donc à l’input du nbJoueurs
        if nbJoueurs == 1 : 
            print("Valeur pas bonne, car le joueur étant seul à déjà gagné avant de commencer le jeu")
            # on retour donc à l’input du nbJoueurs 

    # Définition-paquet (création d’une liste avec les cartes du jeu) :

    paquet=[]
    print("Paquet vide.",paquet)   # test création

    for i in nbJoueurs:
        take_ligne = f.readline() # lire une seule ligne
        if f == "":  # si la ligne est vide elle sort de la boucle
            break
        elif f[0].isdigit():  #    -> on prend dans la suite un moyen de transport (en random)
            name_moyen_transport = f.split(" ")[0]  # le mot est en première position
            
            #  On l'écrit dans la liste 5 fois (car 5 cartes par famille)
            for x in range(5):
                paquet.append(name_moyen_transport)
            print("Paquet avec cartes.",paquet)    # test append

    f.close()   # pour fermer le fichier

    # Mélangez les cartes dans le paquet
    random.shuffle(paquet)
    print("Paquet mixte.", paquet)    # test append


    # Définition du nombre maximal de offres qu’on peut avoir au même temps     
    # car si tous les joueurs font une offre au même temps ils doivent attendre que leurs offres soient acceptées par quelqu’un, cela étant impossible, le jeu bloquerait
    
    nbPropMTemps = 0

    if nbJoueurs % 2 == 0 :
        nbPropMTemps = nbJoueurs/2
    else :
        nbPropMTemps = (nbJoueurs-1)/2


    # Création de (nbPropMTemps) listes, initialisés null, pour définir le “tableau de jeu” (imaginé comme des espaces pour positionner les offres)

    # Initialiser les joueurs : -> appel en Multiprocessus à player 
    
    players=[multiprocessing.Process(target=player, args = (i,))for i in range (nbJoueurs)]

    # Initialisation des tas de cartes de chaque joueur : 
    tas=[]
    
    for k in range (nbJoueurs) :
        tas.append([])
        for x in range(5):
            tas.append(paquet[x])   # 5 cartes ajoutées depuis le ficher
        for x in range(5):  # On enlève la carte une fois qu’elle a été prise 
            del paquet[x]
            


    # Initialiser les joueurs à l’état enAttente()
