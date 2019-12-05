# #!/usr/bin/python
# # USAGE:   echo_client_sockets.py <HOST> <PORT> <MESSAGE>
# #
# # EXAMPLE: echo_client_sockets.py localhost 8000 Hello
# import socket
# import sys
# import json
#
# length_header = 100
#
# if len(sys.argv) < 4:
#     print("USAGE: echo_client_sockets.py <HOST> <PORT> <MESSAGE>")
#     sys.exit(0)
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# host = sys.argv[1]
# port = int(sys.argv[2])
# s.connect((host,port))
# msg = json.dumps({"message":sys.argv[3]})
# pack = f"{len(msg):<{length_header}}" + msg
# s.send(pack.encode('utf-8'))    #default encoding of str.encode is utf-8
#
# i = 0
# data = s.recv(10000000)
# print(data.decode('utf-8'))
# print(f'received {len(data)} bytes')
# s.close()
#!/usr/bin/python
# USAGE:   echo_client_sockets.py <HOST> <PORT> <MESSAGE>
#
# EXAMPLE: echo_client_sockets.py localhost 8000 Hello
import socket
import sys
import json
import select
from Message import MessageType
from Message import Message

length_header = 100
host = 'localhost' #sys.argv[1]
port = 50001  #int(sys.argv[2])
inputSocket = []
outputSocket = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
username = ""
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
            6: "Open and participate in rooms(send message)",
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
    chatRoomId = chatRoomId.strip()
    msgObj = Message(1, username, chatRoomId, "")
    encode_send_message(msgObj)

def send_receive_messages():
    print("enter 'Q' to quit chat and go back to main menu. ")
    running = True
    while running:
        inputready, outputready, exceptready = select.select(inputSocket, outputSocket, inputSocket, 0.1)
        for s in inputready:
            if s == sys.stdin:
                # any input closes the serves. Does not work on Windows!
                engMessage = sys.stdin.readline()
                engMessage = engMessage.rstrip()
                if engMessage == 'Q':
                    running = False
                    break
                chatRoomId = input("Input Chat Room ID: ")
                msgObj = Message(6, username, chatRoomId.strip(), engMessage.strip())
                encode_send_message(msgObj)
                #Create message
            else: #It's about to receive a message
                # handle all other sockets
                inputMsg = getMessage()
                if not inputMsg:
                    print("Didn't receive any message")
                else:
                    msgObj = process_incomming_message(inputMsg)
                    # if msgObj.msg_type == 2 or msgObj.msg_type == 5:
                    #     running = False
                    #     break
                    if msgObj.msg_type != 6:
                        running = False
                        break
    return


def encode_send_message(messageObj):
    # x = input("Enter the message: ")
    msg = json.dumps(messageObj.__dict__)  #sys.argv[3]
    pack = f"{len(msg):<{length_header}}" + msg
    pack = pack.encode('utf-8')
    while len(pack):
        transmittedBytes = s.send(pack)
        pack = pack[transmittedBytes:]

def getMessage():
    #"client" must be a socket object connected to a client
    length = ''
    templen = length_header
    while len(length) < length_header:
        buffer = ''
        buffer = s.recv(templen).decode()
        if buffer == '':
            return False
        length += buffer
        templen -= len(buffer)
    intlength = int(length.strip())
    msg = ''
    templen = intlength
    while len(msg) < intlength:
        buffer = ''
        buffer = s.recv(templen).decode()
        if buffer == '':
            return False
        msg += buffer
        templen -= len(buffer)
    return msg

def process_incomming_message(msg):
    msgDict = json.loads(msg)
    #Print the msg in the msg.
    msgObj = Message(msgDict["msg_type"], msgDict["sender"], msgDict["destination"], msgDict["message"])
    if msgObj.msg_type == 6:
        print("From: ",msgObj.sender, "ChatRoom: ", msgObj.destination, "Msg: ", msgObj.message)
    elif msgObj.msg_type == 2:
        print("All rooms: ", msgObj.message)
    elif msgObj.msg_type == 5:
        print("All members: ", msgObj.message)
    return msgObj

def list_all_rooms():
    msgObj = Message(2, username, 0, "")
    encode_send_message(msgObj)
    send_receive_messages()

def join_room():
    roomId = input("Room name to join: ")
    msgObj = Message(3, username, roomId.strip(), "")
    encode_send_message(msgObj)

def leave_room():
    roomId = input("Room name to leave: ")
    msgObj = Message(4, username, roomId.strip(), "")
    encode_send_message(msgObj)


def list_all_members_room():
    roomId = input("Room name for members list: ")
    msgObj = Message(5, username, roomId.strip(), "")
    encode_send_message(msgObj)
    send_receive_messages()

def log_out():
    s.close()

# i = 0
# data = s.recv(10000000)
# print(data.decode('utf-8'))
# print(f'received {len(data)} bytes')
# s.close()


choice_def = {
        1: create_a_room,
        2: list_all_rooms,
        3: join_room,
        4: leave_room,
        5: list_all_members_room,
        6: send_receive_messages,
        7: log_out,
        # 8: query8,
        # 9: query9,
        # 10: query10,
    }

def init_username():
    global username
    username = input("Input new username")
    msgObj = Message(8, username, 0, "")
    #str(MessageType.InitUsername)
    encode_send_message(msgObj)


if __name__ == '__main__':

    inputSocket.append(s)
    inputSocket.append(sys.stdin)
    init_username()
    client_console(s)


