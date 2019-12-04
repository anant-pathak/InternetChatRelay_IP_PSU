#!/usr/bin/python
# USAGE:   echo_client_sockets.py <HOST> <PORT> <MESSAGE>
#
# EXAMPLE: echo_client_sockets.py localhost 8000 Hello
import socket
import sys
import json
import select
import Message

length_header = 100
host = 'localhost' #sys.argv[1]
port =  50000  #int(sys.argv[2])
inputSocket = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
# if len(sys.argv) < 4:
#     print("USAGE: echo_client_sockets.py <HOST> <PORT> <MESSAGE>")
#     sys.exit(0)

#Anonymous chat room
def client_console(s):

    while True:
        user_choices = {
            1: "Create a room",
            2: "List all rooms",
            3: "Join a room",
            4: "Leave a room",
            5: "List all members of a room",
            6: "Open and participate in a room(send message)",
            7: "Log out",
        }
        for eachChoice in user_choices:
            print(eachChoice, user_choices[eachChoice])
        x = input("Enter  a number from the above: ")
        if not x.isnumeric():
            print("Plz enter only the number in range")
            continue
        choice_def[int(x)]()

def create_a_room():
    chatRoomId = input("Enter chat room id")
    msgObj = Message(Message.MessageType.CreateRoom, s, chatRoomId, engMessage )

def send_receive_chatRoomM():
    while running:
        inputready, outputready, exceptready = select.select(inputs, outputs, inputs, 0.1)
        # print(inputready)

        for s in inputready:
            # if s == :
            #     # handle the server socket
            #     client, address = self.server.accept()
            #     client.setblocking(0)
            #     self.inputs.append(client)
            #     self.outputs.append(client)
            #     self.client_queues[client] = queue.Queue()
            #     # we could make it so that the first thing the server expects is message containing a username
            #     # which would be a special message type
            #     print(f"Established connection with: {address}")
            pass
        if s == sys.stdin:
            # any input closes the serves. Does not work on Windows!
            engMessage = sys.stdin.readline()
            chatRoomId = input("Input Chat Room ID: ")
            msgObj = Message(Message.MessageType.SendMsgRoom, s, chatRoomId, engMessage )
            encode_send_message(msgObj)
            #Create message
        else:
            # handle all other sockets
            inputMsg = getMessage(s)
            print("From while Client and in which Chat room  and what message")
            # if not inputMsg:
            #     s.close()
            #     self.inputs.remove(s)
            #     self.outputs.remove(s)
            # else:
            # self.client_queues[s].put(inputMsg)

        for s in outputready:
            if not self.client_queues[s].empty():
                output = self.client_queues[s].get()
                output = json.dumps(output)
                self.sendMessage(s, output)


def encode_send_message(messageObj)
    # x = input("Enter the message: ")
    msg = json.dumps({"message": messageObj})  #sys.argv[3]
    pack = f"{len(msg):<{length_header}}" + msg
    s.send(pack.encode('utf-8'))    #default encoding of str.encode is utf-8

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
    return msg

# i = 0
# data = s.recv(10000000)
# print(data.decode('utf-8'))
# print(f'received {len(data)} bytes')
# s.close()


choice_def = {
        1: create_a_room,
        2: query2,
        3: query3,
        4: query4,
        5: query5,
        6: send_receive_chatRoomM,
        7: query7,
        # 8: query8,
        # 9: query9,
        # 10: query10,
    }



if __name__ == '__main__':

    inputSocket.append(s)
    inputSocket.append(sys.stdin)
    client_console(s)


