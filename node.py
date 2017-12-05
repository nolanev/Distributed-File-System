from socket import *
import sys
import os
import os.path
import time
#import thread  
import threading
from threading import Thread

BUFFER_SIZE=1024

def run():
	lock_request("text.txt")
	print("got here")
	lock_request("new.txt")
	

#requests access to file by polling	
def lock_request(filename):
	requesting_lock=True
	while requesting_lock:
		#connect to lock server
		clientSocket=socket(AF_INET,SOCK_STREAM)
		clientSocket.connect((gethostbyname(gethostname()),8001))
		#send request
		file_request ="FILE REQUEST: " + str(filename)
		clientSocket.send(file_request.encode())
		#if reply granted
		reply=clientSocket.recv(BUFFER_SIZE).decode()
		print("RECIEVED: ", reply)
		if  "GRANTED: " in reply:
			clientSocket.close()# close connection to lock server
			requesting_lock=False
			send_request(filename)
			
	
	
#when acess to file is granted we request file from server
##this is the one to be changed for chanching sends request to caching server which then sends on to sever
def send_request(filename):	
	conn_to_cache=socket(AF_INET,SOCK_STREAM) #may or may not need this line
	conn_to_cache.connect((gethostbyname(gethostname()),8002)) #connect to cahce
	file_request ="FILE REQUEST: " + str(filename)
	conn_to_cache.send(file_request.encode())
	#clientSocket.close()
	
#	clientSocket = socket(AF_INET,SOCK_STREAM)
#	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#	clientSocket.bind((gethostbyname(gethostname()), 8003)) ##new socket
#	clientSocket.listen(1)
#	try:
#		conn, addr = serverSocket.accept()
#	
	file_contence=conn_to_cache.recv(BUFFER_SIZE).decode()
	print("NODE RECIEVED: ", file_contence)	 
	#CLOSECONNECTION
	conn_to_cache.close()
	#do something with file
	complete_request(filename)
	
#When we are done with file we let the locking server know to unlock it
def complete_request(filename):
	#connect to lock server
	
	clientSocket=socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((gethostbyname(gethostname()),8001))
	
	finished ="FINISHED: " + str(filename)
	clientSocket.send(finished.encode())
	clientSocket.close()	

	
if __name__ == "__main__":
	run()