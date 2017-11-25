from socket import *
import sys
import os
import os.path
#import thread  
import threading
from threading import Thread

def run():
	port=8000
	BUFFER_SIZE=102

	#SETUPANDCONNECT
	clientSocket=socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((gethostbyname(gethostname()),port))
	file_request ="FILE REQUEST: test.txt"
	clientSocket.send(file_request.encode())
	file_path=clientSocket.recv(BUFFER_SIZE)
	print(file_path)	
	#CLOSECONNECTION
	clientSocket.close()
		
if __name__ == "__main__":
	run()