import os

filename='test.txt'
if filename in  os.listdir("cached_files/"):
		#return file TODO
		filename="cached_files/" +str(filename)
		f = open(filename,'rb')
		l = f.read(1024)
		
		print('Sent ',repr(l))
		f.close()
