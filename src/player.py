#!/usr/bin/env python3

# Python 3
# sudo apt-get install python3-tk
# sudo apt-get install python3-pil python3-pil.imagetk



from distutils import ccompiler
from random import *

from posixpath import split

from multiprocessing import Process, Manager, Lock
from random import *
import random

import time
import signal
import os
import sys
import sysv_ipc


def player(cards, request, lock, mq1, mq2, mq3, mq4, lockValue, winner):

   
   # TO GET MESSAGE QUEUE=F(PID)
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
    def handlerPlayer(sig, frame):  # ?
        if sig == signal.SIGUSR2:
            print("DIED")
            sys.exit(1)
    


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
            print([os.getpid(), " ", r , " ", offType])  # OFFRE
            
            # UPDATE SHARED MEMORY
            lock.acquire()
            request.append([os.getpid(), r])
            lock.release()
            
            # UPDATE REQUEST IN PROGRESS
            offerCounter.append(offType)
            offerCounter.append(r)



    signal.signal(signal.SIGUSR2, handlerPlayer)
    lookingFor = max(cards,key = cards.count)  # Cards that player is looking for
    offCard = [c for c in cards if c != lookingFor] # Cards other than those the player needs
    offerCounter = [] # Liste des offres en attente


    makeOffer(offCard, request, lock)
    time.sleep(2)   # Just for the game 


    # PID ACCESS
    lock.acquire()
    pid1 = request[0][0]
    pid2 = request[1][0]
    pid3 = request[2][0]
    pid4 = request[3][0]
    lock.release()



    # Each player checks if it is first on the waiting list, and stores this value
    lock.acquire()
    askIfPriorityToTake = request[0][0] == os.getpid()
    lock.release()
    time.sleep(1)

    
    # GAME FOR SELECTED PLAYER -> WHO MADE THE OFFER
    while (cards != [lookingFor]*5): # STOP only when family is completed
        # I the selected player is the one that have the priority to start making an offer
        if askIfPriorityToTake: # Lead the exchange

            # PRINT OFFRE COUNTER
            print()
            print("*** The exchanges have begun ***")
            print('OFFERS :', request)

            print("The player want to give some cards")
            lock.acquire()
            notExchange = True  # To check if the exchange is made
            N = 0

            # LOOK INTO THE SHARED MEMORY
            for i in range (1,len(request)):  
                if request[0][1] == request[i][1] and notExchange: # If the offer is compatible with the number of cards the player needs
                    N = i   # Player reference 

                    # SEND MESSAGE TO LET OTHERS KNOW
                    message = str(1) + ';' + str(offerCounter[-2]) + ';' + str(os.getpid())
                    message = message.encode()
                    mq = askForPid(request[i][0])
                    mq.send(message)
                    print("PLAYER SENDS : ", offerCounter[-2])

                    # IF GET A MESSAGE FROM OTHERS
                    try:
                        # GET CARDS 
                        mq = askForPid(os.getpid())
                        m,t = mq.receive()  # get the message
                        typeGetFromOffer = m.decode()   # decode de message
                        print("PLAYER GETS : ", typeGetFromOffer)

                        # EXCHANGE CARDS
                        for i in range(0,len(cards)):
                            if cards[i] == offerCounter[-2]: 
                                cards[i] = typeGetFromOffer

                        print("NEW HEAD OF CARDS : ", cards)

                        # TEST IF WIN
                        if (cards == [lookingFor]*5):
                            
                            lockValue.acquire()
                            winner[0] = os.getpid()
                            lockValue.release()
                            os.kill(os.getpid(), signal.SIGUSR1)

                        # UPDATE CARTES FOR EXCHANGE
                        offCard = [x for x in cards if x != lookingFor]

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
                mq = askForPid(request[2][0])
                mq.send(message)
            elif N == 2:
                print("MEX : PASS THE TURN.")
                message = str(2)
                message = message.encode()
                mq = askForPid(request[3][0])
                mq.send(message)
            elif N == 3:
                print("MEX : PASS THE TURN.")
                message = str(2)
                message = message.encode()
                mq = askForPid(request[1][0])
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
                makeOffer(offCard,request, lock)

        


        # GAME FOR PLAYER -> WHO TAKE THE OFFER
        else:
            print("The player need to take some cards")
            # IF GET A MESSAGE FROM OTHERS
            try:
                mq = askForPid(os.getpid())
                m,t = mq.receive()      # get the message
                mes = m.decode()        # decode de message
                mexDecod = [str(s) for s in mes.split(";")]
                lookIntoMex = mexDecod[0]
                lookIntoMex = int(lookIntoMex) ###


                if lookIntoMex == 1:   
                    typeGetFromOffer = mexDecod[1]
                    pidGOT = mexDecod[2]
                    pidGOT = int(pidGOT)
                    print("PLAYER GETS : " , typeGetFromOffer)

                if lookIntoMex == 2:
                    print("No exchange")
                
                if lookIntoMex == 3:    ###
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
                    winner[0] = os.getpid()
                    lockValue.release()
                    
                    # POINTS
                    if lookingFor == "Velo":
                        nPoints = 3
                    else:
                        if lookingFor == "Autobus":
                            nPoints = 5
                        else:
                            if lookingFor == "Voiture":
                                nPoints = 7
                            else:
                                if lookingFor == "Avion":
                                    nPoints = 9
                                else:
                                    print("ERROR with points.")
                    print("FAMILY ", lookingFor, "has been completed. The player get ", nPoints, " points.")
                    os.kill(os.getpid(), signal.SIGUSR1)

                # UPDATE CARTES FOR EXCHANGE
                offCard = [x for x in cards if x != lookingFor]

                # UPDATE OFFRE COUNTER
                offerCounter.clear()


                makeOffer(offCard, request, lock)
        time.sleep(2)   # JUST FOR THE GAME


        # +++ +++ +++ +++ +++ +++ +++ 
        # FOR RESTART
        if askIfPriorityToTake:
            print('RESTART OFFERS :', request)

        lock.acquire()
        print("RESTART PRIORITY")
        askIfPriorityToTake = request[0][0] == os.getpid()
        lock.release()

        # time.sleep(2)   # Just for the game
    
    