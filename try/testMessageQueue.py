# Test messages queues

import sysv_ipc
from multiprocessing import Process
import multiprocessing


# fonction processus
def f(a, b):
    keyJoueur = 128
    mq = sysv_ipc.MessageQueue(keyJoueur, sysv_ipc.IPC_CREAT)

    r = a+b
    print(r)

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
    message, t = mq.receive()
    value = message.decode()
    print(value)
    p.join()