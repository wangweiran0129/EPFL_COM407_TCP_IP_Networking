# PDC Clinet

# python3 PDC.py <server> <port> <command>
# <server> is either the IPv4 address of the server or its domain name
# <port> is the port number of the server
# <command> is the command to send to the server, i.e. either CMD_short:0 or CMD_short:1 or CMD_floodme
# CMD_short:d
# d is the time interval in seconds between two consecutive send()

# The server closes the connection after sending the n messages
# The PDC does not know the value of n a priori

import socket
import sys

# tcpip.epfl.ch
SERVER = sys.argv[1]
# 5003
PORT = int(sys.argv[2])
# CMD_short:1
COMMAND = sys.argv[3]

length = 1024
length_msg = len("This is PMU data i")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))
sock.sendall(COMMAND.encode())
#sock.sendto(COMMAND.encode(), (SERVER, PORT))

if COMMAND == "CMD_floodme":
    data = sock.recv(length).decode()
    no_of_recv = 0
    while data:
        print(data)
        data = sock.recv(length).decode()
        no_of_recv = no_of_recv + 1

else:
    count = 0
    flag = True
    data = sock.recv(length).decode()
    while data:
        # This is PMU data i
        # REQUIREMENT: Make sure you print ONE message PER line
        while len(data) >= length_msg:
            msg = data[:length_msg]
            print(msg)
            count = count + 1
            data = data[length_msg:]
            # the length of msg should +1
            # when it comes to
            # This is PMU data ii
            if count >= 10 and flag == True:
                length_msg = length_msg + 1
                flag = False
        data = sock.recv(length).decode()

#print("number of recv call is ", no_of_recv)
