from socket import *
import sys
import os
import os.path
#import thread  
import threading
from threading import Thread
from Database import *
def run():
	port=8000
	max_conn=5
	BUFFER_SIZE=1024
	
	#SETUP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	#do i need to have threads here so the server is listening to every client node??
	serverSocket.bind((gethostbyname(gethostname()), port))
	#ip=(gethostbyname(gethostname()))
	
	
	#WAIT FOR CONNECTION
	print( 'The server is ready to listen \n')	  
	serverSocket.listen(max_conn)
	
	while True:	
	
	#ACCEPT CONNECTION
		try:
				  
			#START THREAD FOR CONNECTION
			conn, addr = serverSocket.accept() #acept connection from browser
			while True:	
				data=conn.recv(BUFFER_SIZE).decode()
				print(data)
				if "FILE" in data:
					print( 'Starting new file request thread \n')	
					threading.Thread(target=fileRequest, args=(conn, data)).start()
		
		except Exception as e:
			if serverSocket:
				serverSocket.close()
				#print "Could not open socket:", message
			sys.exit(1) 
	
	#CLOSE CONNECTION 
	serverSocket.close()
	
def fileRequest(conn, msg):
	splitMessage = msg.split('\n')
	filename = splitMessage[0].split(':')[1].strip()
	filepath=find_file(filename)
	print(" sending file path")
	print(str(filepath))	
	conn.send(filepath.encode())##cant send this for some reason
	
if __name__ == "__main__":
	run()