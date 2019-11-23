#!/usr/bin/env python

"""
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys

host = ''
port = 50000
backlog = 5
length_header = 100
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(backlog)
input = [server]
running = 1

def get_message(client):
    #"client" must be a socket object connected to a client
    length = client.recv(length_header)
    if not length:
        s.close()
        input.remove(s)                                                
    msg = client.recv(int(length.decode().strip()))
    return msg.decode()

while running:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

        if s == server:
            # handle the server socket
            client, address = server.accept()
            input.append(client)

        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = 0 
        else:
            # handle all other sockets
            #arbitrary = 10               Anant - Uncomment these and you will see that this section is getting executed twice
            #print(arbitrary)                     I have to figure out why my gdb is messed up so i dont have to "print debug" haha
            #arbitrary = arbitrary + 1
            #print(arbitrary)
            inputMsg = get_message(s)
            # Here I think we would  pass it to the  message handler
            # The message handler will process the data appropriately and then queue it for output.
            # I'm thinking that Rooms object will keep a list of client in that room and when a message is sent
            # to that room the handler will then broadcast the message to each of the client sockets.
            outputMsg = inputMsg.encode()
            if outputMsg:
                s.send(outputMsg)  #look up exactly functionality
            else:
                s.close()
                input.remove(s)
server.close()

