#!/usr/bin/env python  
import socket 
 
listening_adapter = '' # Listen to all adapters 
listening_port =  85
listening_queue_size = 0 # Only an incomming connection at the same time 
listening_endpoint = (listening_adapter, listening_port) 
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(listening_endpoint) 
 
print('I_am'+str(sock.getsockname())+ 'and_I_am_listening_...') 
 
sock.listen(listening_queue_size) # This is a blocking command 
connection = sock.accept() # Return the TCP connection 
(sock,sender)=connection #only one connection, so we can reuse the socket 'sock'
print('A_connection_with: '+ str(sender)+' has_been_established') 
 
longest_message_size = 100 
message = sock.recv(longest_message_size) 
# It waits for a TCP segment of any payload length, but as much 100 
# bytes will be copied into the 'message' variable. 
 
print(message+'+', 'is_received_from,'+ sender) 
 
sock.close()  
