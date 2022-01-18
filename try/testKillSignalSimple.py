# Test kill avec signal

import multiprocessing
import os
import signal

def compteur(i):
    while True:
        pass
        if ( == 3):
            cloche = True
            signal.signal(signal.SIGTERM, signal_handler, i)


def signal_handler(signum, frame, i):
    if signum == signal.SIGUSR1:
        os.kill(childPID[i], signal.SIGUSR1)
        # il faut que ça tue tous les processus child

if __name__ == '__main__':
    tourne = [multiprocessing.Process(target=compteur, args = (i, ))for i in range (5)]
    global childPID
    global cloche
    cloche = False

    for p in tourne:
        p.start()
        childPID[i] = multiprocessing.process.pid()

    for p in tourne:
        p.join()

