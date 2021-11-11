# PDC Clinet

import socket
import sys


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
lost = 0 # the number of packet that we lose
totallost = 0 # for 60 loops

message = 'RESET:20'
data = ''
data6 = ''
print("sending: ", message)

for i in range(60):

    packet = 0
    lost = 0

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
            lost = lost + 1

        try:
            data6 = sock6.recv(length).decode()
        except:
            lost = lost + 1
        
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
    totallost = totallost + lost

print('total packet = ', totalpacket)
print('average packet per loop = ', totalpacket/60)
print('lost rate1 = ', (totalpacket-60)/totalpacket)
print('lost are = ', totallost)
print('lost rate2 = ', lost/totalpacket)
