import socket
from datetime import datetime
import select

sock_add = ('localhost', 6789)
max_size = 4096

#UDP
# print("starting the server at ", datetime.now())
# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM )
# server.bind(sock_add)
#
# data, client = server.recvfrom(max_size)
#
# print("At ", datetime.now(), client, "said", data)
# server.sendto(b"Are you talking to me? ", client )
# server.close()

#TCP:
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(sock_add)
serverSocket.listen(7)

def myreceive(clientSocket):
    chunks = []
    bytesRcvd = 0
    # while bytesRcvd < max_size:
    chunk = clientSocket.recv(max_size-bytesRcvd)
    chunk = chunk.decode("utf-8")
    if chunk == '':
        raise RuntimeError("socket connection broken")
    chunks.append(chunk)
    bytesRcvd += len(chunk)
    return ''.join(chunks)

while 1:
    (clientSocket, clientAddress) = serverSocket.accept()
    clientMsg = myreceive(clientSocket)
    print("client: ", clientSocket, "said: ", clientMsg)
    clientSocket.sendall("your message received")
    clientSocket.close()











