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
from Message import Message
from Message import MessageType
from Room import Room

class ChatServer:
    def __init__(self, host='', port=50001, backlog=5, length_header=100):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.length_header = length_header
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.server.setblocking(0)
        self.server.listen(backlog)
        self.inputs = [self.server,sys.stdin]
        self.outputs = []
        self.client_queues = {} #index of cleint queues by socket object -> client queue
        self.rooms = {} #index of rooms by room name -> room object
        self.clients = {} #index of client by client username -> socket object

    def getMessage(self, client):
        #"client" must be a socket object connected to a client
        length = ''
        templen = self.length_header
        while len(length) < self.length_header:
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
        msg = json.loads(msg)
        msgObject = Message(msg['msg_type'], msg['sender'], msg['destination'], msg['message'])
        return msgObject

    def sendMessage(self, client_socket, message):
        #this will need to be adapted to pass a message object to it instead of a string
        #which will be pretty easy once I see the message class
        message = json.dumps(message.__dict__)
        message = f"{len(message):<{self.length_header}}" + message
        message = message.encode()
        while len(message):
            transmitted = client_socket.send(message)
            message = message[transmitted:]
            
    def room_broadcast(self, room, msg):
        self.rooms[room].addMessage(msg)
        for x in self.rooms[msg.destination].members:
            self.client_queues[self.clients[x]].put(msg)
    
    def all_broadcast(self, msg):
        for val in self.client_queues.values():
            val.put(msg)

    def handleMessage(self, requesting_socket, msg):

        if msg.msg_type == 8:
            self.clients[msg.sender] = requesting_socket

        elif msg.sender not in self.clients.keys():
            requesting_socket.close()

        elif msg.msg_type == 1:
            if msg.destination not in self.rooms:
                self.rooms[msg.destination] = Room(msg.destination)
                self.rooms[msg.destination].addMember(msg.sender)

        elif msg.msg_type == 2:
            output_message = Message(2, "server", msg.sender, list(self.rooms.keys()))
            self.client_queues[requesting_socket].put(output_message)
            
        elif msg.msg_type == 3:
            if msg.destination in self.rooms.keys():
                self.rooms[msg.destination].addMember(msg.sender)

        elif msg.msg_type == 4:
            if msg.destination in self.rooms.keys():
                self.rooms[msg.destination].removeMember(msg.sender)

        elif msg.msg_type == 5:
            if msg.destination in self.rooms.keys():
                output_message = Message(5, "server", msg.sender, self.rooms[msg.destination].members)
                self.client_queues[requesting_socket].put(output_message)

        elif msg.msg_type == 6:
            if msg.destination in self.rooms.keys() and msg.sender in self.rooms[msg.destination].members:
                self.room_broadcast(msg.destination, msg)
        else:
            pass
        
           #create room

    def runServer(self):
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(self.inputs, self.outputs, self.inputs, 0.1)
            #print(inputready)
            #print(outputready)
            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    client.setblocking(0)
                    self.inputs.append(client)
                    self.outputs.append(client)
                    self.client_queues[client] = queue.Queue()
                    #we could make it so that the first thing the server expects is message containing a username
                    # which would be a special message type 
                    print(f"Established connection with: {address}")
                elif s == sys.stdin:
                    # any input closes the serves. Does not work on Windows!
                    junk = sys.stdin.readline()
                    running = 0 
                else:
                    # handle all other sockets
                    inputMsg = self.getMessage(s)
                    if not inputMsg:
                        s.close()
                        self.inputs.remove(s)
                        self.outputs.remove(s)
                    else:
                        self.handleMessage(s,inputMsg)
                        # self.client_queues[s].put(inputMsg)

            for s in outputready:
                if not self.client_queues[s].empty():
                    output = self.client_queues[s].get()  # output = json.dumps(output.__dict__)
                    self.sendMessage(s, output)

        self.server.close()


if __name__ == '__main__':
    server = ChatServer()
    server.runServer()