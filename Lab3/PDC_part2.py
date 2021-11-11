# PDC Clinet

import socket
import sys

"""
# Part 2: TCP

# python3 PDC.py <server> <port> <command>
# <server> is either the IPv4 address of the server or its domain name
# <port> is the port number of the server
# <command> is the command to send to the server, i.e. either CMD_short:0 or CMD_short:1 or CMD_floodme
# CMD_short:d
# d is the time interval in seconds between two consecutive send()

# The server closes the connection after sending the n messages
# The PDC does not know the value of n a priori

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
"""



# Part 3 UDP
# The PDC sends a reset command RESET: n
# where n = 20 is the number of seconds
# by which the PMU has to advance its clock

# On receiving this command,
# the PMU chooses a random value X where 0<=X<=n
# is the actual offset it uses to reset its clock
# The PMU also informs the PDC about the exact offset value it uses

# The client (PDC) must keep retransmitting the message
# until it receives an acknowledgement from the PMU
# The acknowledgement from the PMU has the format OFFSET = X
# where X is the offset it chose to reset its clock
# Use a timeout value of 1 sec to wait for an acknowledgement
# from the PMU before retransmitting again

# PDC.py must be able to send the command to the server
# on both IPv4 and IPv6 sockets
# and should detect automatically if the server runs on IPv4 or on IPv6

# The prototype of PDC.py must be:
# python3 PDC.py <server> <port>

SERVER = sys.argv[1] # localhost
PORT = int(sys.argv[2]) # port 5004

length = 1024 # OFFSET=X
packet = 0 # how many packets I need to send before receiving an acknowledgement per loop
totalpacket = 0 # used for 60 times loop

message = 'RESET:20'
data = ''
data6 = ''
print("sending: ", message)

for i in range(60):

    packet = 0

    # UDP & IPv4
    sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # UDP & IPv6
    sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    sock4.connect((SERVER, PORT))
    sock6.connect((SERVER, PORT))

    sock4.settimeout(1)
    sock6.settimeout(1)

    while True:
        packet = packet + 1
        data4 = data6 = ''
        sock4.send(message.encode())
        sock6.send(message.encode())

        try:
            data4 = sock4.recv(length).decode()
        except:
            pass

        try:
            data6 = sock6.recv(length).decode()
        except:
            pass
        
        # when the acknowledgement is received, it will quit the true loop
        if data4:
            print("data4 = ", data4)
            # print("data4's counter = ", counter)
            break

        if data6:
            print("data6 = ", data6)
            # print("data6's counter = ", counter)
            break

    sock4.close()
    sock6.close()
    totalpacket = totalpacket + packet

print('total packet = ', totalpacket)
print('total packet rate = ', totalpacket/60)
# print('packets need to be sent before receiving an acknowledgement: ', packet)
