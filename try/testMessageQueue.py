# Test messages queues

import sysv_ipc
from multiprocessing import Process
import multiprocessing
import os
import signal

# fonction processus
def f(a, b):
    
    keyJoueur = 128
    mq = sysv_ipc.MessageQueue(keyJoueur, sysv_ipc.IPC_CREAT)
    while True:
        r = a+b
        a += 1
        if (a == 6):
            message = str(r).encode()
            mq.send(message)

            mq.remove()

if __name__ == '__main__':
    keyMain = 128
    mq = sysv_ipc.MessageQueue(keyMain, sysv_ipc.IPC_CREAT)

    a = 1
    b = 3

    p = Process(target=f, args=(a, b))
    p.start()
    pid = p.pid
    message, t = mq.receive()
    value = message.decode()
    os.kill(pid, signal.SIGKILL)
    print("Derniere valeur: ", value)