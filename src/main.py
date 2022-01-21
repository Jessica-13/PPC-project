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











if __name__ == '__main__':









    signal.signal(signal.SIGUSR1, handlerGame) #on modifie le signal SIGUSR1 selon la méthode handler        
    #reciiver process1
    key1=100
    mq1=sysv_ipc.MessageQueue(key1,sysv_ipc.IPC_CREAT)
    #reciever process2
    key2=200
    mq2=sysv_ipc.MessageQueue(key2,sysv_ipc.IPC_CREAT)
    #reviever processs 3
    key3=300
    mq3=sysv_ipc.MessageQueue(key3,sysv_ipc.IPC_CREAT)

    #round= multiprocessing.Value(0)

    #création et distribution des cartes
    Transports=["vélo", "voiture", "trottinette", "train"]
    n=3 #le nombre de joueurs
    cartes= [] #cartes qu'on va distribuer par la suite aux joueurs
    for i in range (0,n):
        a=Transports[i]
        cartes.append(a)
    cartes= cartes*5        #m'assurer que ce truc là marche ??
    random.shuffle(cartes)  #pas nécessaire mais stylé
    C1, C2, C3 = list(itertools.repeat(0, 5)), list(itertools.repeat(0, 5)), list(itertools.repeat(0, 5))
    C=[C1,C2,C3]
    for i in range (0,3):
        while 0 in C[i]:  
            o=random.choice(cartes)
            C[i].append(o)
            C[i].remove(0)
            cartes.remove(o)

    with Manager() as manager:
        request = manager.list() #création de la mémoire partagée
        lock = Lock()
        lockV= Lock() #lock pour la Value
        whoWin= Array('i', 1)
        color1="red"
        color2="blue"
        color3="green"

        print("******************** START GAME ********************")
        print('Le joueur 1 a comme liste de carte', C1)
        print('Le joueur 1 a comme liste de carte', C2)
        print('Le joueur 1 a comme liste de carte', C3)
       
        print()


        #on lance les 3 processes
        p1=Process(target=player, args=(C1,request,lock,color1,mq1,mq2,mq3,lockV,whoWin))
        p2=Process(target=player, args=(C2,request,lock,color2,mq1,mq2,mq3,lockV,whoWin))
        p3=Process(target=player, args=(C3,request,lock,color3,mq1,mq2,mq3,lockV,whoWin))
        p1.start()
        p2.start()
        p3.start()

        '''key1=p1.pid
        key2=p2.pid
        key3=p3.pid
        print(key1)
        mq1=sysv_ipc.MessageQueue(key1,sysv_ipc.IPC_CREAT)
        mq2=sysv_ipc.MessageQueue(key2,sysv_ipc.IPC_CREAT)
        mq3=sysv_ipc.MessageQueue(key3,sysv_ipc.IPC_CREAT)'''

        p1.join()
        p2.join()
        p3.join()

        if whoWin[0]==p1.pid:
            print("Le joueur 1 a gagné")
        elif whoWin[0]==p2.pid:
            print("Le joueur 2 a gagné")
        elif whoWin[0]==p3.pid:
            print("Le joueur 3 a gagné")
        else:
            print("La partie s'est terminée mais personne n'a gagné")

        mq1.remove()
        mq2.remove()
        mq3.remove()