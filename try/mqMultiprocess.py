# Message Queue multiprocess
import sysv_ipc
import signal
import os
from multiprocessing import Process
import multiprocessing
import signal


class Joueur(multiprocessing.Process):
    def __init__(self, nom, age):
        multiprocessing.Process.__init__(self)
        self.nom = nom
        self.age = age

    # fonction processus
    def f(a, b):
        
        keyJoueur = 128
        mq = sysv_ipc.MessageQueue(keyJoueur, sysv_ipc.IPC_CREAT)
        r = a+b
        message = str(r).encode()
        mq.send(message)

        mq.remove()



if __name__ == '__main__':

    players = [multiprocessing.Process(target=player, args = (i, ))for i in range (5)]

    # Création d'une liste de pid pour pouvoir arrêter les processus une fois le jeu fini
        childPID = []

        # Pour recevoir les messages queues
        keyMain = 128
        mq = sysv_ipc.MessageQueue(keyMain, sysv_ipc.IPC_CREAT)


        # Start + order of process
        a = 0
        for p in players:
            # Card assignment
            giveCards(j)
            p.start()
            childPID[a] = p.pid
            a += 1
        # Si on reçoit un message, on arrête les processus
        message, t = mq.receive()
        value = message.decode()
        for a in range(5):
            os.kill(childPID[a], SIGKILL)