import re
SPECIAL_CHAR = "⁃"

class CustomFile:
	
	#Constructor
	def __init__(self, name, file_dict, mode):

		self.name 	   = name
		self.file_dict = file_dict
		self.mode 	   = mode


	def read(self, data):

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
		text_read = self.read(data)

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
		if not hasEnoughMemory("BCSS", data):
			print(f"ERROR: not enough memory")
			return

		#Getting the free memory chunks in the data storage
		free_memory  	  = getFreeMemory(data)
		chunk_to_append   = int(getLastChunk(self.file_dict)[0]) + 1

		
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
										"start" : chunk_start,
										"length": len(text_to_add)
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

		#### APPLY CHECK FOR SIZE = 0 ####


		#Each iteration of this for loop reads one chunk and  appends its data to text_read
		self.mode = 'r'
		file_text = self.read(data)
		self.mode = 't'

		file_lentgh = len(file_text)
		if size > file_lentgh:
			print(f"EEROR: Total file size is {file_lentgh}")
			return

		#truncate_size = file_lentgh- size


		truncate_chunk, char_to_truncate = getChunksToTruncate(size, self.file_dict)


		print("TRUNCATE CHUNK: ", truncate_chunk)
		print("\nCHAR TO TRUNCATE: ",char_to_truncate)


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

		print("TRUNC PAGE: ", truncate_chunk_page)
		print("\nTRUNC START: ", truncate_chunk_start)
		print("\nTRUNC length: ", truncate_chunk_length)
		print("\nTRUNC end: ", truncate_chunk_end)

		start_truncate = truncate_chunk_end - int(char_to_truncate)
		#print(data[truncate_chunk_page][start_truncate:end])
		print("Start Trunc: ", start_truncate)
		data[truncate_chunk_page] =  data[truncate_chunk_page][:start_truncate] + SPECIAL_CHAR * int(char_to_truncate) + data[truncate_chunk_page][truncate_chunk_end:]
		#data[truncate_chunk_page] = data[truncate_chunk_page].replace(data[truncate_chunk_page][start_truncate : end] , SPECIAL_CHAR * int(char_to_truncate))
		self.file_dict["data"][truncate_chunk]["length"] = str(int(self.file_dict["data"][truncate_chunk]["length"]) - int(char_to_truncate))

		print(data)
		print(len(data["0"]))
		print(self.file_dict)
		return self.file_dict

		'''for chunk, chunk_dict in self.file_dict["data"].items():


			page   = chunk_dict["page"]
			start  = int(chunk_dict["start"])
			chunk_length = int(chunk_dict["length"])

			text = data[page][start + total_length]

			length = 0
			for s in text:
				if (length == size) or (length > size):
					data[page][start+chunk_length].replace(data[page][length: length+1], SPECIAL_CHAR)
				else:
					pass
				length += 1
							
		print(data)
		return data'''


	'''def move(self, fileobj, data):

		to_move_start_index = int(input("Enter the start index of the content to be moved"))
		to_move_end_index = int(input("Enter the end index of the content to be moved"))
		
		final_index = int(input("Enter the final index"))

		page = fileobj['page']
		for p in page:
			text = data[str(p)]
			text_to_move = text[to_move_start_index : to_move_end_index]
			length = len(text_to_move)
			length_full = len(text)
			move_text = text[final_index : length]

			moved_text = text[:final_index] + text_to_move + text[final_index:length_full]

		return moved_text'''



	'''def appendFile(self, fileobj, data):
		page = fileobj["page"]

		text_to_append = input("Enter the text to append:\n")

		for p in page:
			p = str(p)
			
			file_content = data[p]
			file_content += text_to_append
		
		return file_content'''


	'''def writeAtFile(self, fileobj, data):
		page = fileobj["page"]

		index = int(input("Give the index where you want to write at \t"))

		text_to_write = input("Enter Text\n")

		for p in page:
			text = data[str(p)]

			write_at = text[:index] + text_to_write + text[index:]


		return write_at'''



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

	@param data: dict object of out total data storage
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


	"""s = ""
	free_chunks = {}

	for page, page_data in data.items():
		a = 0
		start_index = 0
		end_index = 0
		free_chunk_length = 0
		

		i = 0
		chunk_id = 1
		for c in page:
			
			matches = re.finditer(SPECIAL_CHAR, page_data)

			free_memory = [match.start() for match in matches]
>>>>>>> e7edd211459ab30b90a21b90f8beb6793b81f643
			
			free_chunks = {}
			end_index = 0
			free_chunk_length = 0

			for i in range(len(free_memory)-1):

				prev_index = free_memory[i]
				next_index = free_memory[i+1]
				diff = next_index - prev_index

				if diff == 1:
					end_index += 1
					free_chunk_length += 1

				elif diff > 1 or next_index == 1023:
					free_chunk_length += 1
					start_index = prev_index - free_chunk_length
					#free_chunks[page] = {str(chunk_id) : {"start" : start_index, "end" : start_index+free_chunk_length}}
					
					free_chunk_length = 0
					chunk_id += 1
					end_index+1
			print(free_chunks)
		if len(free_memory) > len(text):
			return free_memory

		else:
			print("Memory Full")
			return"""





		