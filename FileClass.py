import re
SPECIAL_CHAR = "⁃"

class CustomFile:
	"""Class to return file object"""

	#Constructor
	def __init__(self, name, file_dict, mode):

		self.name 	   = name
		self.file_dict = file_dict
		self.mode 	   = mode



	''' This function taken in a file object which contains
	 	the attributes of the file and data which contains
	 	the contents written in the file.

	 	It then prints out the content of file page wise
	def readFile(self, fileobj, data):
		page = fileobj["page"]

		for p in page:
			p = str(p)
			print(f"\nPage '{p}':")
			print(f"Length = {len(data[p])}")
			print("\t" + data[p]) '''

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
		

	def append(self, data, text):

		if self.mode != 'a':
			print(f"ERROR: File is opened in {self.mode} mode, Please  open the file using 'Open <filename> a' for appending")
			return

		'''last_chunk, last_chunk_dict = getLastChunk(self.file_dict)

		print(last_chunk_dict)
		#access the data in that chunk
		page = last_chunk_dict["page"]
		print(page)
		length = int(last_chunk_dict["length"])
		start = int(last_chunk_dict["start"])
		text_length = len(text)
		end = start + length
		total_index = end + text_length'''

		#checking if that page has memory
		free_memory = getFreeMemory(text, data)

		return
			#print(len(data[page][end:text_length+1]))
			#print(text_length)
			#temp = str.maketrans(data[page][end+1 : text_length+1], text)
			#data[page][end : text_length] = data[page][end : text_length].translate(temp)
		'''	print(data[page])
			data[page] = data[page].replace(data[page][end:total_index], text)
			print("done")
			print(data[page])
			return

		else:
			print("no memory")
			free_page = getFreePage(data, text)
			if free_page:
				print("got a free page")
				data[free_page] = text
				return
			else:
				print("Memory Full : Free Some Space")
				return'''

			

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


		truncate_chunk, char_to_truncate = getTruncateChunks(size, self.file_dict)


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



def getTruncateChunks(size, file_dict):

	a = 0
	last_chunk = ""

	for chunk, chunk_dict in file_dict["data"].items():

		if a >= size:
			return last_chunk, a-size
		a += int(chunk_dict["length"])
		last_chunk = chunk

	return list(file_dict["data"].keys())[-1], a-size



def getLastChunk(file_dict):

	last_chunk = ""

	#getting the last chunk
	for chunk, chunk_dict in file_dict["data"].items():
		last_chunk = chunk

	return last_chunk, chunk_dict
				

def hasMemory(text, page, data):

	text_length = len(text)
	free_space = data[page].count(SPECIAL_CHAR)
	
	if text_length < free_space:
		return True

	return False


def getFreeMemory(text, data):

	s = ""
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
			return





		