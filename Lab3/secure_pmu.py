# prototype
# python3 secure_pmu.py <certificate> <key>
# <certificate> is the path to my signed certificate
# <key> is the path to my secret key

# This time, as opposed to previously
# I need to hardcode the address "localhost" as well as the port number 5003

# The provided client program Part5_PDC.pyc can be launched using:
# python3 Part5_PDC.pyc CMD_short:0 <ca-certificate>
# <ca-certificate> is the path to the CA certificate

import socket
import ssl
import sys

CERTIFICATE = sys.argv[1]
KEY = sys.argv[2]

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(CERTIFICATE, KEY)

# socket create success
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket bind success
sock.bind(('127.0.0.1', 5003))
# socket listen success
sock.listen(5)

ssock = context.wrap_socket(sock, server_side=True)

while True:
    sslsocket, fromaddr = ssock.accept()
    data = sslsocket.read(1024).decode()

    if data:
        print(data)
        sslsocket.send('This is PMU data 0'.encode())
    else:
        break

sslsocket.close()
sock.close()