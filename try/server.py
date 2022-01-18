#!/usr/bin/env python3

# Echo Server

'''
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # creates a socket object that supports the context manager type, so you can use it in a with statement. 
    s.bind((HOST, PORT))
    s.listen()      # enables a server to accept() connections, making a "listening" socket
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


# pass  # Use the socket object without calling s.close()
'''

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

'''
Since the listening socket was registered for the event selectors.EVENT_READ, 
it should be ready to read. We call sock.accept() and 
then immediately call conn.setblocking(False) to put the socket in non-blocking mode.
'''
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE       # object to hold the data we want included along with the socket 
    sel.register(conn, events, data=data)

'''
If the socket is ready for reading, then mask & selectors.EVENT_READ is true, and sock.recv() is called. 
Any data that’s read is appended to data.outb so it can be sent later.
'''
def service_connection(key, mask):
    sock = key.fileobj  # socket object 
    data = key.data     # contains the events that are ready
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:   # block if no data is received
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
            '''
            This means that the client has closed their socket, so the server should too. 
            But don’t forget to first call sel.unregister() so it’s no longer monitored by select().
            '''
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:] 
            '''
            When the socket is ready for writing, which should always be the case for a healthy socket, 
            any received data stored in data.outb is echoed to the client using sock.send(). The bytes sent are then removed from the send buffer
            '''

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)            # to configure the socket in non-blocking mode
sel.register(lsock, selectors.EVENT_READ, data=None)    # registers the socket to be monitored with sel.select() for the events you’re interested in

try:
    while True:
        events = sel.select(timeout=None)   # blocks until there are sockets ready for I/O. It returns a list of (key, events) tuples, one for each socket
        for key, mask in events:
            if key.data is None:    # hen we know it’s from the listening socket and we need to accept() the connection
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask) # If key.data is not None, then we know it’s a client socket that’s already been accepted, and we need to service it. service_connection() is then called and passed key and mask, which contains everything we need to operate on the socket.
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()