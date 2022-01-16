#!/usr/bin/env python3

import sysv_ipc

key = 128
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)







# Game block
def gameBlock():
    while True:
        try:
            value = int(input())
        except:
            print("Input error, try again!")
        message = str(value).encode()
        mq.send(message)


        message2, t = mq.receive()
        value2 = message2.decode()
        value2 = int(value2)
        
        if value2:
            print("received:", value2)
        else:
            print("exiting.")   # value = 0 -> exit
            break

    mq.remove()







if __name__ == "__main__":
    gameBlock()
