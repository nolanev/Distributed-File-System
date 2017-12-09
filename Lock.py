from socket import *
import sys
import os
import os.path 
import threading
from threading import Thread
locked_files=[] 


def run():
	port=8001
	max_conn=5
	BUFFER_SIZE=1024
	
	#SETUP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serverSocket.bind((gethostbyname(gethostname()), port))
	
	#WAIT FOR CONNECTION
	print( 'The lock server is ready to listen \n')	  
	serverSocket.listen(max_conn)
	
	while True:	
	
		try:
				  
			#START THREAD FOR CONNECTION
			conn, addr = serverSocket.accept() #acept connection from browser
			threading.Thread(target=request, args=(conn, port)).start()
		
		except Exception as e:
			if serverSocket:
				serverSocket.close()
				print("Locking Error: could not connect")
			sys.exit(1) 
	
	#CLOSE CONNECTION 
	serverSocket.close()
	
def request(conn, port):

	msg=conn.recv(1024).decode()
	filename=parse(msg)
	if("REQUEST" in msg):
		if(request_handler(filename,conn)== True):
			reply= "GRANTED: " +filename
			conn.send(reply.encode())
			conn.close()
		else:
			reply= "DENIED: " +filename
			conn.send(reply.encode())
			conn.close()
	elif ("FINISHED" in msg):
		finish_handler(filename)
		conn.close()


def parse(msg): #get file name
	splitMessage = msg.split('\n')
	filename = splitMessage[0].split(':')[1].strip()
	
	return filename
	
def request_handler(filename, conn):
	if filename in locked_files:
		return False
	else:
		locked_files.append(filename)
		return True
		
	#check if mutex on file name if yes add conn to the queue and return false
	#if not put mutex and return true
	
def finish_handler(filename):
	locked_files.remove(filename)
	#when we change from polling pop next connection looking for file off the stack
	
	

if __name__ == "__main__":
	run()
	
	

	