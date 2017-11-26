file_dictionary={"text.txt" : "A//etc//"}

def find_file(filename):
	print("the file we are looking for is ", filename)

	if filename in file_dictionary.keys():
		print("file exists on db")
		return file_dictionary[filename]
	else:
		print("file does not exist on db. creating file")
		file_path= "B//temp//" + filename
		f=open(file_path,"w+")
		f.close()
		file_dictionary[filename]=file_path
		return file_path

