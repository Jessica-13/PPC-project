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
from multiprocessing import Process, Manager, Lock
from random import *
import random

import queue

import time
import signal
import os
import sys
import sysv_ipc


getPID = os.getpid()


def player(cards, request, lock, mq1, mq2, mq3, mq4, lockValue, winner):



    
    lookingFor = max(cards,key = cards.count)  # Cards that player is looking for
    offCard = [c for c in cards if c != lookingFor] # Cards other than those the player needs
    offerCounter = [] #liste des offres en attente
    



    # TO GET PID
    def askForPid(pidReciever): # 
        if pidReciever == pid1:
            return mq1
        if pidReciever == pid2:
            return mq2
        if pidReciever == pid3:
            return mq3
        if pidReciever == pid4:
            return mq4
        else:
            print("ERROR : UNABLE TO FIND PID")
            sys.exit(1)



    # when get SIGUSR1
    def handlerPlayer(sig, frame):
        if sig==signal.SIGUSR2:
            print("Je meurs")
            sys.exit(1)
    
    signal.signal(signal.SIGUSR2, handlerPlayer)


    # Definition of the offer    
    def makeOffer(offCard, request, lock):
        if offCard == []:       # The player has nothing left to offer
            print("I WIN! I AM TOO STRONG!")
        else:
            if random.randint(0,1) == 1:    # Random choice on whether to play the minimum or maximum number of cards]
                offType = max(offCard, key = offCard.count)
            else:
                offType = min(offCard, key = offCard.count)

            r = offCard.count(offType)
            print([getPID, " ", r , " ", offType])
            
            # UPDATE SHARED MEMORY
            lock.acquire()
            request.append([getPID, r])
            lock.release()
            
            R = r
            # UPDATE REQUEST IN PROGRESS
            offerCounter.append(offType)
            offerCounter.append(r)


    R = 0




    makeOffer(offCard, request, lock)
    time.sleep(2)   # Juste for the game 



    # PID ACCESS
    lock.acquire()
    pid1 = request[0][0]
    pid2 = request[1][0]
    pid3 = request[2][0]
    pid4 = request[3][0]
    lock.release()



    #chacun regarde s'il est le premier sur le liste d'attente, et stocke cette valeur
    lock.acquire()
    askIfPriorityToTake = request[0][0] == getPID
    lock.release()
    time.sleep(1)

    # PRINT OFFRE COUNTER
    print()
    print("*** The exchanges have begun ***")
    print('OFFERS :', request)




    # GAME FOR SELECTED PLAYER -> WHO MADE THE OFFER
    while (cards != [lookingFor]*5): # STOP only when family is completed
        # I the selected player is the one that have the priority to start making an offer
        if askIfPriorityToTake: # Lead the exchange
            print("The player want to give some cards")
            lock.acquire()
            notExchange = True  # To check if the exchange is made
            N = 0
            # LOOK INTO THE SHARED MEMORY
            for i in range (1,len(request)):  
                if request[0][1] == request[i][1] and notExchange: # If the offer is compatible with the number of cards the player needs
                    N = i

                    # SEND MESSAGE TO LET OTHERS KNOW
                    message = str(1) + ';' + str(offerCounter[-2]) + ';' + str(getPID)
                    message = message.encode()
                    mq = askForPid(request[i][0])
                    mq.send(message)
                    print("PLAYER SENDS : ", offerCounter[-2])

                    # IF GET A MESSAGE FROM OTHERS
                    try:
                        # GET CARDS 
                        mq = askForPid(getPID)
                        m,t = mq.receive()  # get the message
                        typeGetFromOffer = m.decode()   # decode de message
                        print("PLAYER GETS : ", typeGetFromOffer)

                        # EXCHANGE CARDS
                        for i in range(0,len(cards)):
                            if cards[i] == offerCounter[-2]: 
                                cards[i] = typeGetFromOffer

                        print("NEW HEAD OF CARDS : ",cards)

                        # TEST IF WIN
                        if (cards == [lookingFor]*5):
                            
                            lockValue.acquire()
                            askForPid[0] = getPID
                            lockValue.release()
                            os.kill(getPID, signal.SIGUSR1)

                        # UPDATE CARTES FOR EXCHANGE
                        offCard = [x for x in cards if x != lookingFor] #les cartes dont on doit se débarasser

                        # UPDATE OFFRE COUNTER
                        offerCounter.clear()
                        
                        notExchange = False                  

                    except sysv_ipc.ExistentialError:
                        print("ExistentialError. Terminate process.")
                        sys.exit(1)
            
            time.sleep(1)   # JUSTE FOR THE GAME

            # TO PASS THE TURN
            if N == 0:
                print("THE PLAYER PAS THE TURN.")
                message = str(2)
                message = message.encode()

                # SEND MESSAGE TO THE NEXT PLAYER ((pid2))
                mq = askForPid(request[1][0])
                mq.send(message)

                # SEND MESSAGE TO THE NEXT PLAYER ((pid3))
                mq = askForPid(request[2][0])
                mq.send(message)

                # SEND MESSAGE TO THE NEXT PLAYER ((pid4))
                mq = askForPid(request[3][0])
                mq.send(message)

            # TELL THAT AN OFFER HAS BEEN ACCEPTED SO NEXT PLAYER NEED TO PASS THE TURN
            elif N == 1:
                print("MEX : PASS THE TURN.")
                message = str(2)
                message = message.encode()
                mq = askForPid(request[2][0]) #j'ai échangé des cartes avec le joueur ligne 1 donc je dis au joueur ligne 2 de passer au tour suivant
                mq.send(message)
            elif N == 2:
                print("MEX : PASS THE TURN.")
                message = str(2)
                message = message.encode()
                mq = askForPid(request[1][0]) #j'ai échangé des cartes avec le joueur ligne 2 donc je dis au joueur ligne 1 de passer au tour suivant
                mq.send(message)
            elif N == 3:
                print("MEX : PASS THE TURN.")
                message = str(2)
                message = message.encode()
                mq = askForPid(request[3][0]) #j'ai échangé des cartes avec le joueur ligne 2 donc je dis au joueur ligne 1 de passer au tour suivant
                mq.send(message)
            else:
                print("ERROR.") 



        # UPDATE SHARED MEMORY FOR THE PLAYER WITH WHOM THE EXCHANGE HAPPENED         
            rwDone = False  # !!!!!!!!!!!!!!!!!!!!
            if N == 1 or N == 2 or N == 3:
                request.pop(0)
                for i in range(0,len(request)):
                    if request[i][1] == request[0][1]:
                        request.pop(i)
                        break
                rwDone = True   # !!!!!!!!!!!!!!!!!!!

            lock.release()
        

        # IF ECHANGE -> MAKE A NEW OFFER
            if N == 1 or N == 2 or N == 3:
                while not rwDone:
                    time.sleep(2)   # JUST FOR THE GAME
                makeOffer(offCard,request, lock)    # call to the function
        

        # END OF TURN
        if N == 0:
            request.pop(0)
            makeOffer(offering_cards,request, lock)

        


        # GAME FOR PLAYER -> WHO TAKE THE OFFER
        else:
            print("The player need to take some cards")
            # IF GET A MESSAGE FROM OTHERS
            try:
                mq = askForPid(getPID)
                m,t = mq.receive()  # get the message
                mes = m.decode() # decode de message
                mexDecod = [str(s) for s in mes.split(";")]
                lookIntoMex = mexDecod[0]
                lookIntoMex = int(lookIntoMex)


                if lookIntoMex == 1:   
                    typeGetFromOffer = mexDecod[1]
                    pidGOT = mexDecod[2]
                    pidGOT = int(pidGOT)
                    print("PLAYER GETS : " ,typeGetFromOffer)

                if lookIntoMex == 2:
                    print("No exchange")
                
                if lookIntoMex == 3:
                    print("No exchange")

            except sysv_ipc.ExistentialError:
                print("ExistentialError. Terminate process.")
                sys.exit(1)
            
            # SEND MESSAGE
            if lookIntoMex == 1:
                message = str(offerCounter[-2]).encode()
                mq = askForPid(pidGOT)
                mq.send(message)
                print("PLAYER SENDS : ", offerCounter[-2])
                
                # EXCHANGE CARDS
                for i in range(0,len(cards)):
                    if cards[i] == offerCounter[-2]: 
                        cards[i] = typeGetFromOffer

                print("NEW HEAD OF CARDS : ",cards)

                # TEST IF WIN
                if (cards == [lookingFor]*5):

                    lockValue.acquire()
                    winner[0] = getPID
                    lockValue.release()
                    os.kill(getPID, signal.SIGUSR1)

                # UPDATE CARTES FOR EXCHANGE
                offering_cards = [x for x in cards if x != lookingFor]
                print("offering_cards = ",offering_cards)

                # UPDATE OFFRE COUNTER
                offerCounter.clear()


                makeOffer(offering_cards,request, lock)
                time.sleep(2)   # JUST FOR THE GAME
    
    