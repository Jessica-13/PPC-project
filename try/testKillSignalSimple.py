# Test kill avec signal qui marche

from multiprocessing import Process
import os
import signal
import time

# méthode compter les cartes
def processus(i):
    time.sleep(3)
    os.kill(os.getppid(), signal.SIGKILL)

# à ajouter au definitivo
def signal_handler(signum, frame):
    if signum == signal.SIGUSR1:
        os.kill(childPID, signal.SIGKILL)
        print("Die")


# main avec les processus
if __name__ == '__main__':
    p = Process(target=processus, args=(2,))

    p.start()
    global childPID
    childPID = p.pid
    p.join()

