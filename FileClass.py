import json

SPECIAL_CHAR = "⁃"

with open("structure.json") as f:
  structure = json.load(f)

root = structure["root"]
data = structure["data"]

class CustomFile:
	
	#Constructor
	def __init__(self, name, file_dict, mode):

		self.name 	   = name
		self.file_dict = file_dict
		self.mode 	   = mode


	def read(self):

		"""
		A function that returns the data of a file stored in the file structure
		and None if if the mode if not read

		@param self: The calling object
		@param data: The dict object of the data in our file structure 
		"""

		if self.mode != "r":
			print(f"ERROR: File is opened in {self.mode} mode, Please  open the file using 'Open <filename> r' for reading")
			return

		text_read = ""

		#Each iteration of this for loop reads one chunk and  appends its data to text_read
		for chunk, chunk_dict in self.file_dict["data"].items():

			page   = chunk_dict["page"]
			start  = int(chunk_dict["start"])
			length = int(chunk_dict["length"])

			text_read += data[page][start : start+length]
			
		return text_read


	def readFrom(self, data, index, size):
		
		"""
		A function that returns the data of a file from a specific index stored in 
		the file structure and None if the mode is not read or an invalid index is provided

		@param self: The calling object
		@param data: The dict object of the data in our file structure 
		@param index: The index to start reading from
		@param size: The number of bytes to be read
		"""

		if self.mode != "r":
			print(f"ERROR: File is opened in {self.mode} mode, Please open the file using 'open <filename> r' for reading")
			return

		#reading the file 
		text_read = self.read()

		if index > len(text_read):
			print(f"INDEX ERROR: Couldn't read file. Index greater than file length{len(text_read)}")
			return

		elif index < 0:
			print(f"INDEX ERROR: Invalid index - index less than zero")

		#reading file from given index
		text_read_from = text_read[index : index+size]

		return text_read_from
		

	def append(self, text, data):

		if self.mode != 'a':
			print(f"ERROR: File is opened in {self.mode} mode, Please  open the file using 'Open <filename> a' for appending")
			return


		#Checking if that page has memory
		if not hasEnoughMemory(text, data):
			print(f"ERROR: not enough memory")
			return

		#Getting the free memory chunks in the data storage
		free_memory  	  = getFreeMemory(data)
		last_chunk 		  = getLastChunk(self.file_dict)

		if last_chunk:
			chunk_to_append   = int(last_chunk[0]) + 1
		else:
			chunk_to_append   = 0

		"""if not self.file_dict["data"]:
			chunk_to_append = 1
		else:
			chunk_to_append   = int(getLastChunk(self.file_dict)[0]) + 1
			
		#Getting the free memory chunks in the data storage
		free_memory  	  = getFreeMemory(data)	"""	
		
		for page, free_memory_chunks in free_memory.items():

			for chunk in free_memory_chunks:

				chunk_start  = chunk[0]
				chunk_length = chunk[1]

				if len(text):				

					if chunk_length > len(text):
						text_to_add = text
						text = ""
					else:
						text_to_add = text[:chunk_length]
						text = text[chunk_length:]

					#Adding the data to our file storage
					data[page] = data[page][:chunk_start] + text_to_add + data[page][chunk_start+len(text_to_add):]

					#Adding the appended chunk to the data of file dictionary
					self.file_dict["data"][f"{chunk_to_append}"] = {
																		"page"  : page,
																		"start" : str(chunk_start),
																		"length": str(len(text_to_add))
									 							   }
					chunk_to_append += 1
			

	def truncate(self, data, size):

		"""
		A function that returns the given size of bytes from the end and replace with 
		null character stored in the file structure and None if the mode is not read
		or an invalid index is provided

		@param self: The calling object
		@param data: The dict object of the data in our file structure 
		@param size: The size of bytes to retain
		"""

		if self.mode != 't':
			print(f"ERROR: File is opened in {self.mode} mode, Please  open the file using 'Open <filename> t' to truncate\n")
			return
		#### APPLY CHECK FOR SIZE = 0 ####


		#Each iteration of this for loop reads one chunk and  appends its data to text_read
		self.mode = 'r'
		file_text = self.read()
		self.mode = 't'

		file_lentgh = len(file_text)
		if size > file_lentgh:
			print(f"EEROR: Total file size is {file_lentgh}")
			return

		# size = 0 means the user wants to remove the whole content of file
		# Emptying File
		if size == 0:
			self.file_dict, data = emptyFile(self.file_dict, data)
			return self.file_dict, data

		truncate_chunk, char_to_truncate = getChunksToTruncate(size, self.file_dict)

		chunks_to_pop = []

		for chunk, chunk_dict in self.file_dict["data"].items():

			if int(chunk) > int(truncate_chunk):
				chunks_to_pop.append(chunk)

		for chunk in chunks_to_pop:

			page   = self.file_dict["data"][chunk]["page"]
			start  = int(self.file_dict["data"][chunk]["start"])
			length = int(self.file_dict["data"][chunk]["length"])

			data[page] =  data[page][:start] + SPECIAL_CHAR * length + data[page][start+length:]
			self.file_dict["data"].pop(chunk)


		truncate_chunk_page = self.file_dict["data"][truncate_chunk]["page"]
		truncate_chunk_start = int(self.file_dict["data"][truncate_chunk]["start"])
		truncate_chunk_length = int(self.file_dict["data"][truncate_chunk]["length"])
		truncate_chunk_end = truncate_chunk_start + truncate_chunk_length

		start_truncate = truncate_chunk_end - int(char_to_truncate)
		#print(data[truncate_chunk_page][start_truncate:end])
		data[truncate_chunk_page] =  data[truncate_chunk_page][:start_truncate] + SPECIAL_CHAR * int(char_to_truncate) + data[truncate_chunk_page][truncate_chunk_end:]
		#data[truncate_chunk_page] = data[truncate_chunk_page].replace(data[truncate_chunk_page][start_truncate : end] , SPECIAL_CHAR * int(char_to_truncate))
		self.file_dict["data"][truncate_chunk]["length"] = str(int(self.file_dict["data"][truncate_chunk]["length"]) - int(char_to_truncate))


	def write(self, text):

		""" 
		This function overwrites the content of a file.

		@param data : dict object of our data storage
		@param text : The text to write into the file

		"""

		if self.mode != 'w':
			print(f"ERROR: File is opened in {self.mode} mode, Please  open the file using 'Open <filename> w' for writing")
			return

		#Deleting the content of file
		size = 0
		self.mode = 't'
		empty_file = self.truncate(data, size)


		#Writing the text into the empty file
		self.mode = 'a'
		write_text = self.append(text, data)
		
		#Setting the mode back to w
		self.mode = 'w'
		#print(self.file_dict)
		#print(data)
		#return write_text


	def writeAt(self, data, text, index):

		""" 
		This function writes the text into the given location of file

		@param data : dict obj of our data storage
		@param text : text to write into the file
		@param index : location to write on
		"""

		if self.mode != 'w':
			print(f"ERROR: File is opened in {self.mode} mode, Please  open the file using 'Open <filename> w' for writing")
			return

		self.mode = 'r'
		file_text = self.read()

		file_lentgh = len(file_text)
		if index > file_lentgh:
			print(f"EEROR: Total file size is {file_lentgh}")
			return

		#Deleting the data from the given index onwards
		self.mode = 't'
		truncate_file = self.truncate(data, index)

		#Writing the user data on the given index
		self.mode = 'a'
		write_text_at = self.append(text, data)
		
		#Reseting the mode back to w
		self.mode = 'w'

		''''page = self.file_dict["data"][chunk_to_write_at]["page"]
		print(len(data[page]))
		data[page] = data[page][:index] + text + data[page][index+len(text):]
		print(len(data[page]))
		print(data[page])'''

def getChunksToTruncate(size, file_dict):

	a = 0
	last_chunk = ""

	for chunk, chunk_dict in file_dict["data"].items():

		if a >= size:
			return last_chunk, a-size
		a += int(chunk_dict["length"])
		last_chunk = chunk

	return list(file_dict["data"].keys())[-1], a-size



def getLastChunk(file_dict):

	if file_dict["data"].items():
		return list(file_dict["data"].items())[-1]
				

def hasEnoughMemory(text_to_insert, data):

	"""
	####	INSERT EXPLANATION

	@param text_to_insert: str to insert in our data storge
	@param data 	     : dict object of out total data storage
	"""

	free_space = 0
	for value in data.values():
		free_space += value.count(SPECIAL_CHAR)
	
	if len(text_to_insert) < free_space:
		return True

	return False


def getFreeMemory(data):

	"""
	A utillity fucntion that returns a dictionary of free chunks of memory in every page 

	@param data: dict object of our total data storage
	"""

	free_memory = {}
	for i in range(len(data)):
		free_memory[str(i)] = [] 

	
	#Iterate data page by page
	for page_num, page_data in data.items():

		start  = 0
		length = 0

		#Iterate page char by char
		for i in range(len(page_data)):

			#if empty space is found in the page
			if page_data[i] == SPECIAL_CHAR:
				
				if page_data[i-1] != SPECIAL_CHAR:
					start = i
					length += 1
				else:
					length += 1 

				#if page ends at empty space
				if i == len(page_data) - 1:
					temp   = [start, length]
					length = 0
					
					free_memory[page_num].append(temp)

			#if empty space ends and data is found in the page
			else:
				if page_data[i-1] == SPECIAL_CHAR and i != 0:
					temp   = [start, length]
					start  = 0
					length = 0
										
					free_memory[page_num].append(temp)				

	return free_memory


def emptyFile(file_dict, data):


	"""
	This function delets the content of a file while 
	retaining the file itself.

	@param data :  dict object of our total data storage
	@param file_dict : dict object of our file object
	"""

	chunks_to_pop = []

	for chunk, chunk_dict in file_dict["data"].items():
		chunks_to_pop.append(chunk)


	for chunk in chunks_to_pop:

		page   = file_dict["data"][chunk]["page"]
		start  = int(file_dict["data"][chunk]["start"])
		length = int(file_dict["data"][chunk]["length"])

		data[page] =  data[page][:start] + SPECIAL_CHAR * length + data[page][start+length:]
		file_dict["data"].pop(chunk)
	return file_dict, data



	