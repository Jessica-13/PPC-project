# Test kill avec signal

import multiprocessing
import os
import signal

def compteur(i,c):
    while True:
        a = 0
        a+=1
        print(a)
        if (i == 3 and a == 20):
            cloche = True
            signal.signal(signal.SIGTERM, signal_handler,c)


def signal_handler(signum, frame):
    if signum == signal.SIGUSR1:
        os.kill(childPID[c], signal.SIGUSR1)
        # il faut que ça tue tous les processus child

if __name__ == '__main__':
    tourne = [multiprocessing.Process(target=compteur, args = (i, c))for i in range (5)]
    global childPID = []

    c = 0

    for p in tourne:
        p.start()
        childPID[c] = multiprocessing.process.pid()
        c += 1
    for p in tourne:
        p.join()

    global cloche
    cloche = False

    '''def list_childrens(pid):
        return [int(c) for c in os.listdir('/proc/%s/task' % pid)]'''