

def find_file(filename):
	print("the file we are looking for is ", filename)

	if filename in  os.listdir("DB_Files/"):
		print("file exists on db")
		file_path= "DB_files/" + filename
		return file_path
	else:
		print("file does not exist on db. creating file")
		file_path= "DB_files/" + filename
		f=open(file_path,"w+")
		f.close()
		return file_path

