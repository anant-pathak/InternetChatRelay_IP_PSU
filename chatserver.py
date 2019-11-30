#!/usr/bin/env python

"""
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import json
import queue

host = ''
port = 50000
backlog = 5
length_header = 100
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.setblocking(0)
server.listen(backlog)
inputs = [server,sys.stdin]
outputs = []
client_queues = {}
running = 1

def getMessage(client):
    #"client" must be a socket object connected to a client
    length = ''
    templen = length_header
    while len(length) < length_header:
        buffer = ''
        buffer = client.recv(templen).decode()
        if buffer == '':
            return False 
        length += buffer
        templen -= len(buffer)

    intlength = int(length.strip())
    msg = ''       
    templen = intlength
    while len(msg) < intlength:
        buffer = ''
        buffer = client.recv(templen).decode()
        if buffer == '':
            return False 
        msg += buffer
        templen -= len(buffer)
    return msg

def sendMessage(client, message):
    #this will need to be adapted to pass a message object to it instead of a string
    #which will be pretty easy once I see the message class
    message = f"{len(message):<{length_header}}" + message
    message = message.encode()
    while len(message):
        transmit = client.send(message)
        message = message[transmit:]
        

#def handle_message():


while running:
    inputready,outputready,exceptready = select.select(inputs,outputs,inputs, 0.1)
    #print(inputready)
    #print(outputready)
    for s in inputready:
        if s == server:
            # handle the server socket
            client, address = server.accept()
            client.setblocking(0)
            inputs.append(client)
            outputs.append(client)
            client_queues[client] = queue.Queue()
            print(f"Established connection with: {address}")
        elif s == sys.stdin:
            # any input closes the serves. Does not work on Windows!
            junk = sys.stdin.readline()
            running = 0 
        else:
            # handle all other sockets
            inputMsg = getMessage(s)
            if not inputMsg:
                s.close()
                inputs.remove(s)
                outputs.remove(s)
            else:
                client_queues[s].put(inputMsg)

    for s in outputready:
        if not client_queues[s].empty():
            output = client_queues[s].get()
            output = json.dumps(output)
            sendMessage(s, output)


server.close()
