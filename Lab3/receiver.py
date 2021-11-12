# Write a multicast receiver that joins the multicast group
# listens on port 10505
# displays the exchanged multicast messages

# python3 receiver.py <group> <port>
# <group> is the multicast group address on which to listen
# <port> is the port number on which to listen

# The receiver application must print the received messages (one message per line)
# Check the multicast server is running: ps aux | grep python

import socket
import sys
import struct

GROUP = sys.argv[1] # 224.1.1.1
PORT = int(sys.argv[2]) # 10505

# UDP & IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((GROUP, PORT))

mreq = struct.pack('4sl', socket.inet_aton(GROUP), socket.INADDR_ANY)
# IPPROTO_IP -> This is useful for reliable error handling on unconnected sockets
# IP_ADD_MEMBERSHIP -> 
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    data = sock.recv(1024)
    if data:
        print(data.decode(), flush=True)
    else:
        break

sock.close()
