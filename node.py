from socket import *
import sys
import os
import os.path
#import thread  
import threading
from threading import Thread

def run():
	#port = int(sys.argv[1])
	port =8000
	BUFFER_SIZE=1024

	#SETUPANDCONNECT
	clientSocket=socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((gethostbyname(gethostname()),port))
	file_request ="FILE REQUEST: text.txt"
	clientSocket.send(file_request.encode())
	file_path=clientSocket.recv(BUFFER_SIZE).decode()
	print("RECIEVED: ", file_path)	
	file_request ="FILE REQUEST: new.txt"
	clientSocket.send(file_request.encode())
	file_path=clientSocket.recv(BUFFER_SIZE).decode()
	print("RECIEVED: ", file_path)	
	#CLOSECONNECTION
	clientSocket.close()
		
if __name__ == "__main__":
	run()