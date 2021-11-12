# A program that reads text from the keyboard
# and sends the text to the multicast group in the same format
# as the messages from Swisscom

# python3 sender.py <group> <port> <sciper>
# <group> is the multicast group address on which to send the message
# <port> is the port number on which to send
# <sciper> it my sciper number

import socket
import sys

GROUP = sys.argv[1]
PORT = int(sys.argv[2])
SCIPER = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
message = SCIPER + input()

sock.sendto(message.encode(), (GROUP, PORT))

sock.close()
