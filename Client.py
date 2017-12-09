from socket import *
import sys
import os
import os.path
import time
import threading
from threading import Thread

BUFFER_SIZE=1024

def run():
	lock_request("text.txt") #test file that is in chache
	lock_request("new.txt") #test file that is not in cache
	

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
		
		reply=clientSocket.recv(BUFFER_SIZE).decode()
		print("RECIEVED: ", reply)
		if  "GRANTED: " in reply:
			clientSocket.close()# close connection to lock server once our request to use the file has been granted
			requesting_lock=False
			send_request(filename)
		#if we dont get a granted reply poll until we do
			
	
	
#when acess to file is granted we request file from server
def send_request(filename):	
	conn_to_cache=socket(AF_INET,SOCK_STREAM) #may or may not need this line
	conn_to_cache.connect((gethostbyname(gethostname()),8002)) #connect to cahce
	file_request ="FILE REQUEST: " + str(filename)
	conn_to_cache.send(file_request.encode())

	
	file_contence=conn_to_cache.recv(BUFFER_SIZE).decode()
	print("NODE RECIEVED: ", file_contence)	 

	conn_to_cache.close()
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