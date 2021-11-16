# PDC Clinet
# This python script is used for EPFL server test

import socket
import sys

SERVER = sys.argv[1] # localhost
PORT = int(sys.argv[2]) # port 5004

length = 1024 # OFFSET=X
packet = 0 # how many packets I need to send before receiving an acknowledgement
lost = 0

message = 'RESET:20'
data4 = ''
data6 = ''
print("sending: ", message)

# UDP & IPv4
sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# UDP & IPv6
sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

sock4.settimeout(1)
sock6.settimeout(1)

sock4.connect((SERVER, PORT))
sock6.connect((SERVER, PORT))

while True:
    packet = packet + 1
    lost = lost + 1
    data4 = data6 = ''
    sock4.sendall(message.encode())
    sock6.sendall(message.encode())

    try:
        data4 = sock4.recv(length).decode()
    except:
        lost = lost + 1

    try:
        data6 = sock6.recv(length).decode()
    except:
        lost = lost + 1
    
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

print('packets need to be sent before receiving an acknowledgement: ', packet)
print('lost: ', lost)
