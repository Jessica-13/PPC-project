#!/usr/bin/env python3


import sysv_ipc

key = 128
mq = sysv_ipc.MessageQueue(key)







# Game block
def playerBlock():
    while True:
        message, t = mq.receive()
        value = message.decode()
        value = int(value)
        
        if value:
            print("received:", value)
        else:
            print("exiting.")   # value = 0 -> exit
            break
        
        
        try:
            value2 = int(input())
        except:
            print("Input error, try again!")
        message2 = str(value2).encode()
        mq.send(message2)







if __name__ == "__main__":
    playerBlock()