#!/usr/bin/env python3

from multiprocessing.managers import SyncManager

HOST = ""
PORT0 = 5011
PORT1 = 5012
PORT2 = 5013
AUTHKEY = 600

def QueueServerClient(HOST, PORT, AUTHKEY):
    class QueueManager(SyncManager):
        pass
    QueueManager.register("get_queue")
    QueueManager.register("get_name")
    QueueManager.register("get_description")
    manager = QueueManager(address = (HOST, PORT), authkey = AUTHKEY)
    manager.connect() # This starts the connected client
    return manager

# create three connected managers
qc0 = QueueServerClient(HOST, PORT0, AUTHKEY)
qc1 = QueueServerClient(HOST, PORT1, AUTHKEY)
qc2 = QueueServerClient(HOST, PORT2, AUTHKEY)
# Get the queue objects from the clients
q0 = qc0.get_queue()
q1 = qc1.get_queue()
q2 = qc2.get_queue()
# put stuff in the queues
q0.put("some stuff")
q1.put("other stuff")
q2.put({1:123, 2:"abc"})
# check their sizes
print("q0 size", q0.qsize())
print("q1 size", q1.qsize())
print("q2 size", q2.qsize())

# pull some stuff and print it
print(q0.get())
print(q1.get())
print(q2.get())