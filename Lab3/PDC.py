import websocket
import sys

# python3 PDC.py <server> <port> <command>

SERVER = sys.argv[1] # tcpip.epfl.ch
PORT = sys.argv[2] # 5006
COMMAND = sys.argv[3]

ws = websocket.WebSocket() # ws://tcpip.epfl.ch:5006
ws.connect("ws://"+SERVER+":"+PORT)
ws.send(COMMAND)
no_recv = 0

if COMMAND == "CMD_floodme":
    data = ws.recv()
    while data:
        print("received:", data.decode())
        data = ws.recv()
        no_recv = no_recv + 1
else:
    data = ws.recv()
    no_recv = no_recv + 1
    while(data):
        print("received: ", data.decode())
        data = ws.recv()
        no_recv = no_recv + 1

ws.close()
print("no_recv = ", no_recv)

