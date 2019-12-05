#!/usr/bin/env python

"""
A TCP Socket Chat Server
By Michael Samuels and Anant Pathak
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
        self.client_queues = {} #index of client queues by socket object -> client queue
        self.rooms = {} #index of rooms by room name -> room object
        self.clients = {} #index of client by client username -> socket object
        self.socket_to_user = {} #index of client queues by socket object -> client queue

    def getMessage(self, client):
        #"client" must be a socket object connected to a client
        length = ''
        templen = self.length_header
        while len(length) < self.length_header:
            buffer = ''
            try:
                buffer = client.recv(templen)
                if not len(buffer):
                    return False 
                length += buffer.decode()
                templen -= len(buffer)
            except:
                return False
        intlength = int(length.strip())
        msg = ''       
        templen = intlength
        while len(msg) < intlength:
            buffer = ''
            try:
                buffer = client.recv(templen).decode()
                if buffer == '':
                    return False
                msg += buffer
                templen -= len(buffer)
            except:
                return False
        msg = json.loads(msg)
        msgObject = Message(msg['msg_type'], msg['sender'], msg['destination'], msg['message'])
        print(msgObject.__dict__)
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
        print(self.rooms[room].messages)
        print(msg.destination)
        print(self.rooms[room].members)
        for x in self.rooms[room].members:
            self.client_queues[self.clients[x]].put(msg)
    
    def all_broadcast(self, msg):
        for val in self.client_queues.values():
            val.put(msg)

    def handleMessage(self, requesting_socket, msg):

        if msg.msg_type == 8:
            if msg.sender not in self.clients:
                self.clients[msg.sender] = requesting_socket
                self.socket_to_user[requesting_socket] = msg.sender
                #print(self.clients)
                #print(self.client_queues)
                print(self.rooms)
            else:
                #self.sendMessage(requesting_socket, Message(1, 'server', msg.sender, f'Username {msg.sender} already exists'))
                requesting_socket.close()
                self.inputs.remove(requesting_socket)
                self.outputs.remove(requesting_socket)
                del self.client_queues[requesting_socket]

        elif msg.sender not in self.clients.keys():
            requesting_socket.close()

        elif msg.msg_type == 1:
            #create room
            if msg.destination not in self.rooms:
                self.rooms[msg.destination] = Room(msg.destination)
                self.rooms[msg.destination].addMember(msg.sender)
                #output_message = Message(1, "server", msg.sender, f"Room {msg.destination} created")
                #self.all_broadcast(output_message)
            #else:
                #output_message = Message(1, "server", msg.sender, f"Room {msg.destination} already exists")
                #self.client_queues[requesting_socket].put(output_message)

        elif msg.msg_type == 2:
            #list rooms
            output_message = Message(2, "server", msg.sender, list(self.rooms.keys()))
            self.client_queues[requesting_socket].put(output_message)
            
        elif msg.msg_type == 3:
            #join room
            if msg.destination in self.rooms.keys():
                self.rooms[msg.destination].addMember(msg.sender)
                #output_message1 = Message(3, "server", msg.sender, self.rooms[msg.destination].returnDict())
                #self.room_broadcast(msg.destination, output_message1)
                #output_message2 = Message(3, "server", msg.sender, f"{msg.sender} joined room {msg.destination}")
                #self.room_broadcast(msg.destination, output_message2)
            #else:
                #output_message = Message(3, "server", msg.sender, f"Cannot join room {msg.destination}, because it does not exist")
                #self.client_queues[requesting_socket].put(output_message)

        elif msg.msg_type == 4:
            #leave room
            if msg.destination in self.rooms.keys() and msg.sender in  self.rooms[msg.destination].members:
                self.rooms[msg.destination].removeMember(msg.sender)
                #output_message = Message(3, "server", msg.sender, f"{msg.sender} left room {msg.destination}")
                #self.room_broadcast(msg.destination, output_message)
            #else:
            #    output_message = Message(4, "server", msg.sender, f"Cannot leave room {msg.destination}, because it does not exist")
            #    self.client_queues[requesting_socket].put(output_message)

        elif msg.msg_type == 5:
            #list members for a room
            if msg.destination in self.rooms.keys():
                output_message = Message(5, "server", msg.sender, self.rooms[msg.destination].members)
                self.client_queues[requesting_socket].put(output_message)
            #else:
            #    output_message = Message(5, "server", msg.sender, f"Cannot provide member list for {msg.destination}, because it does not exist")
            #    self.client_queues[requesting_socket].put(output_message)

        elif msg.msg_type == 6:
            if msg.destination in self.rooms.keys() and msg.sender in self.rooms[msg.destination].members:
                self.room_broadcast(msg.destination, msg)
            #else:
            #    output_message = Message(3, "server", msg.sender, f"Cannot send message to {msg.destination}, because it does not exist")
            #    self.client_queues[requesting_socket].put(output_message)
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
                        outputready.remove(s)
                        del self.clients[self.socket_to_user[s]]
                        del self.socket_to_user[s]
                        del self.client_queues[s]
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