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
	lock_request("new.txt")

#requests access to file by polling	
def lock_request(filename):
	while True:
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
			send_request(filename)
	time.sleep(10)		
	
	
#when acess to file is granted we request file from server
##this is the one to be changed for chanching sends request to caching server which then sends on to sever
def send_request(filename):	
	clientSocket=socket(AF_INET,SOCK_STREAM) #may or may not need this line
	clientSocket.connect((gethostbyname(gethostname()),8002)) #connect to cahce
	file_request ="FILE REQUEST: " + str(filename)
	clientSocket.send(file_request.encode())
	clientSocket.close()
	
#	clientSocket = socket(AF_INET,SOCK_STREAM)
#	clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#	clientSocket.bind((gethostbyname(gethostname()), 8003)) ##new socket
#	clientSocket.listen(1)
#	try:
#		conn, addr = serverSocket.accept()
#	
	file_contence=conn.recv(BUFFER_SIZE).decode()
	print("RECIEVED: ", file_path)	
	#CLOSECONNECTION
	clientSocket.close()
	#do something with file
	complete_request(filename)
	
#When we are done with file we let the locking server know to unlock it
def complete_request(filename):
	#connect to lock server
	clientSocket=socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((gethostbyname(gethostname()),8001))
	
	finsihed ="FINISHED: " + str(filename)
	clientSocket.send(finished.encode())	

	
if __name__ == "__main__":
	run()