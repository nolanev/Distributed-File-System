from socket import *
import sys
import os
import os.path
#import thread  
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
	
	#CLOSE CONNECTION 
	#serverSocket.listen(max_conn)
	serverSocket.close()
	
def request(conn_to_client, port):
	msg=conn_to_client.recv(1024).decode()
	#conn_to_client.close()
	filename=parse(msg)
	request_handler(filename, conn_to_client)

	

def parse(msg):
	splitMessage = msg.split('\n')
	filename = splitMessage[0].split(':')[1].strip()
	return filename

#TODO parse to return file object
	
def request_handler(filename, conn_to_client):
	if filename in  os.listdir("cached_files/"):
		print("CHACHE HIT", filename)
		#return file TODO
		filename="cached_files/" +str(filename)
		f = open(filename,'rb')
		l = f.read(1024)
		conn_to_client.send(l)
		print('CACHE SENT ',repr(l))
		f.close()
	else:
		print("CHACHE MISS", filename)
		#NEW SOCKET#
		time.sleep(3)
		socketwserver=socket(AF_INET,SOCK_STREAM)
	
		socketwserver.connect((gethostbyname(gethostname()),8000))
	
		request= "CACHE REQUEST: " + str(filename)
		socketwserver.send((request).encode())
		responce=socketwserver.recv(1024).decode()
		socketwserver.close()
		#Get a responceof a file name and path
		#f.open
		f = open(responce,'rb')
		l = f.read(1024)
		conn_to_client.send(l)
		print('CACHE SENT ',repr(l))
		#TODO
		#save the file into my database
		filename="cached_files/" +str(filename)
		f_new= open(filename,"w+")
		f_new.write(repr(l))
		f_new.close()
		
		#save to cachedfiles list
		
	
if __name__ == "__main__":
	run()
		