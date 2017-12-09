from socket import *
import sys
import os
import os.path
import threading
from threading import Thread
import time

def run():
	port=8002
	max_conn=5
	BUFFER_SIZE=1024
	
	#SETUP
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serverSocket.bind((gethostbyname(gethostname()), port))

	#WAIT FOR CONNECTION
	print( 'The cache server is ready to listen \n')	  
	serverSocket.listen(max_conn)
	
	while True:	
	
	#ACCEPT CONNECTION
		try:
				  
			#START THREAD FOR CONNECTION
			conn_to_client, addr = serverSocket.accept()
			print( 'Cache connection made \n')	
			threading.Thread(target=request, args=(conn_to_client, port)).start()
		
		except Exception as e:
			if serverSocket:
				serverSocket.close()
				#print "Could not open socket:", message
			sys.exit(1) 
	
	serverSocket.close()
	
def request(conn_to_client, port):
	msg=conn_to_client.recv(1024).decode()
	
	filename=parse(msg)
	request_handler(filename, conn_to_client)

	

def parse(msg):
	splitMessage = msg.split('\n')
	filename = splitMessage[0].split(':')[1].strip()
	return filename

def request_handler(filename, conn_to_client):
	if filename in  os.listdir("cached_files/"):
		print("CHACHE HIT", filename)
		filpath="cached_files/" +str(filename)
		f = open(filepath,'rb')
		l = f.read(1024)
		conn_to_client.send(l)
		print('CACHE SENT ',repr(l))
		f.close()
	else:
		print("CACHE MISS", filename)
		time.sleep(3)
		conn_to_directory=socket(AF_INET,SOCK_STREAM)
	
		conn_to_directory.connect((gethostbyname(gethostname()),8000)) #connect to directory and request the file to be cached and sent on to the client
	
		request= "CACHE REQUEST: " + str(filename)
		conn_to_directory.send((request).encode())
		responce=conn_to_directory.recv(1024).decode()
		conn_to_directory.close()
		#Get a responceof a file name and path
		#f.open
		f = open(responce,'rb')
		l = f.read(1024)
		conn_to_client.send(l)
		print('CACHE SENT ',repr(l))
	
		#save the file into my cache
		filename="cached_files/" +str(filename)
		f_new= open(filename,"w+")
		f_new.write(repr(l))
		f_new.close()
	
if __name__ == "__main__":
	run()
		