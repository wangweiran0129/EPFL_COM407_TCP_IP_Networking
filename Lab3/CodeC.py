# server

import socket

HOST = 'localhost'           
PORT = 5002  

# (AF_INET -> domain, SOCK_STREAM ->  指定socket类型)
# SOCK_STREAM 提供有序的、可靠的、双向的和基于连接的 字节流，
# 使用 带外数据传送机制，为Internet地址族使用TCP。
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# setting the reuse address socket option
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
while True:
	connection, addr = sock.accept()
	while True:
		data = connection.recv(16).decode()
		print("received:", data)
		if data:
			connection.sendall(data.encode())
		else:
			print("No more data from", addr)
			break
	
	connection.close()

'''
When we close the program (i.e., close the socket), the TCP socket may not close immediately.
Instead it may go to a state called ## TIME_WAIT ##.
The kernel closes the socket only after the socket stays in this state for a certain time called the ## Linger Time ##.

If we restart the program before the Linger Time of the previous session expires, ## Address already in use ##
because the address and port numbers are still in use by the socket that is in ## TIME_WAIT ## state.

This mechanism enusres that two different sessions are not mixed up in the case 
that there are delayed packets belonging to the first session
'''

'''
recv()
return value:
< 0 -> error
= 0 -> close the connection
> 0 -> the length of the message on successful completion
'''