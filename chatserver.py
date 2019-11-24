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
input = [server,sys.stdin]
running = 1

def get_message(client):
    #"client" must be a socket object connected to a client
    length = client.recv(length_header)
    length = length.decode()
    
    if length == '':
        print(length)
        return False                                                
    msg = client.recv(int(length.strip()))
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
            inputMsg = get_message(s)
            if not inputMsg:
                s.close()
                input.remove(s)
            else:
                outputMsg = inputMsg.encode()
                # Here I think we would  pass it to the  message handler
                # The message handler will process the data appropriately and then queue it for output.
                # I'm thinking that Rooms object will keep a list of client in that room and when a message is sent
                # to that room the handler will then broadcast the message to each of the client sockets.
                s.send(outputMsg)  #look up exactly functionality      
            
server.close()
