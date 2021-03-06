#!/usr/bin/env python3

from multiprocessing import Queue
from multiprocessing.managers import SyncManager

HOST = ""
PORT0 = 5011
PORT1 = 5012
PORT2 = 5013
AUTHKEY = 600

name0 = "qm0"
name1 = "qm1"
name2 = "qm2"

description = "Queue Server"

def CreateQueueServer(HOST, PORT, AUTHKEY, name = None, description = None):
    name = name
    description = description
    q = Queue()

    class QueueManager(SyncManager):
        pass


    QueueManager.register("get_queue", callable = lambda: q)
    QueueManager.register("get_name", callable = name)
    QueueManager.register("get_description", callable = description)
    manager = QueueManager(address = (HOST, PORT), authkey = AUTHKEY)
    manager.start() # This actually starts the server

    return manager

# Start three queue servers
qm0 = CreateQueueServer(HOST, PORT0, AUTHKEY, name0, description)
qm1 = CreateQueueServer(HOST, PORT1, AUTHKEY, name1, description)
qm2 = CreateQueueServer(HOST, PORT2, AUTHKEY, name2, description)


input("return to end")