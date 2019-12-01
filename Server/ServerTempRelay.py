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
serverSocket.setblocking(0)
inputSockets = []
outputSockets = []

inputSockets.append(serverSocket)

def myreceive(clientSocket):
    chunks = []
    bytesRcvd = 0
    # while bytesRcvd < max_size:
    # while 1:
    try:
        chunk = clientSocket.recv(max_size)
        chunk = chunk.decode("utf-8")
        if chunk:
            chunks.append(chunk)
            bytesRcvd += len(chunk)
        else:
            # raise RuntimeError("socket connection broken")
            print("Socket connection broken, returning FALSE")
            return False
    except:
        print("connection lost, returning FALSE")
        return False
    return ''.join(chunks)

while 1:
    readable, writable, exceptional = select.select(inputSockets, outputSockets, inputSockets, 0.3) #3 seconds

    for s in readable:
        if s == serverSocket:
            (clientSocket, clientAddress) = serverSocket.accept()
            clientSocket.setblocking(0)
            inputSockets.append(clientSocket)
        else: # the socket in readable is a client socket having sent some data.
            clientMsg = myreceive(s)
            if clientMsg:
                print("client: ", clientSocket, "said: ", clientMsg)
                s.sendall(b"your message received")
            else:
                inputSockets.remove(s)
                s.close()
            # inputSockets.remove(s)
            # s.close()
    for w in writable:
        print("in writable::: for ", w)

    for e in exceptional:
        inputSockets.remove(e)
        e.close()













