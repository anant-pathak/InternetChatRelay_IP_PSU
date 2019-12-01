import datetime
import socket
import json

server_address = ('localhost', 6789)
max_size = 10

# UDP:
# print("Starting client at: ", datetime.datetime.now())
# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client.sendto(b"Hey!", server_address)
# data, server = client.recvfrom(max_size)
# print("At", datetime.datetime.now(), server, "said", data)
# client.close()

# TCP:
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)
customInputStr = ""
# while customInputStr != "Q":
customInputStr = input("Enter message to send to the humble server: ")
client.sendall(customInputStr.encode("utf-8"))

data = client.recv(max_size)
print('At', datetime.datetime.now(), 'someone replied', data)
client.close()
