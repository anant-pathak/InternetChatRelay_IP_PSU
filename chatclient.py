#!/usr/bin/python
# USAGE:   echo_client_sockets.py <HOST> <PORT> <MESSAGE>
#
# EXAMPLE: echo_client_sockets.py localhost 8000 Hello
import socket
import sys
import json

length_header = 100

if len(sys.argv) < 4:
    print("USAGE: echo_client_sockets.py <HOST> <PORT> <MESSAGE>")
    sys.exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host,port))
msg = json.dumps({"message":sys.argv[3]})
pack = f"{len(msg):<{length_header}}" + msg
s.send(pack.encode('utf-8'))    #default encoding of str.encode is utf-8

i = 0
data = s.recv(10000000)
print(data.decode('utf-8'))
print(f'received {len(data)} bytes')
s.close()
