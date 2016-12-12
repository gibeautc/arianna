#!/usr/bin/env python
import socket
HOST=''
PORT=80
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
while 1:
	print("listening")
	s.listen(1)
	conn,addr=s.accept()
	print("Connected by: "+str(addr))
	while 1:
		data=conn.recv(1024)
		if not data: break
		print(data)
conn.close()
print("closed....")
