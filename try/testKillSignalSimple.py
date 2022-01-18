# Test kill avec signal

from multiprocessing import Process
import os
import signal
import time

def processus(i):
    time.sleep(3)
    os.kill(os.getppid(), signal.SIGKILL)


def signal_handler(signum, frame):
    if signum == signal.SIGUSR1:
        os.kill(childPID, signal.SIGKILL)
        print("Die")


if __name__ == '__main__':
    p = Process(target=processus, args=(2,))

    p.start()
    global childPID
    childPID = p.pid
    p.join()

