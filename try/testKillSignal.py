# Test kill avec signal

import multiprocessing
import os

def compteur(i):
    while True:
        i+=1

if __name__ == '__main__':
    tourne = [multiprocessing.Process(target=compteur, args = (i, ))for i in range (3)]

    for p in tourne:
        p.start()
    for p in tourne:
        p.join()

    # if cloche sonne
    os.kill(os.getpid())