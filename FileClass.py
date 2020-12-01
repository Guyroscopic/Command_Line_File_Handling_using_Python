
class FileClass:
	"""Class to return file object"""

	def __init__(self, name, fileobj):
		self.name = name
		self.fileobj = fileobj["type"]


	''' This function taken in a file object which contains
	 	the attributes of the file and data which contains
	 	the contents written in the file.

	 	It then prints out the content of file page wise'''
	def readFile(self, fileobj, data):
		page = fileobj["page"]

		for p in page:
			p = str(p)
			print(f"\nPage '{p}':")
			print(f"Length = {len(data[p])}")
			print("\t" + data[p])



	def readFileFrom(self, fileobj, data):
		page = fileobj['page']

		start = int(input("Enter the start index"))
		end   = int(input("Enter the end index"))

		for p in page:
			p = str(p)
			print(f"\nPage '{p}':")
			print(f"Length = {len(data[p])}")

			file_content = data[p]
			read_content = file_content[start:end]
			print("\t" + read_content)


	def truncate(self, fileobj, data):

		page = fileobj['page']

		index = int(input("Enter the starting index to truncate file"))

		for p in page:
			text_to_truncate = data[str(p)]
			truncated_text = text_to_truncate[0 : index]

		return truncated_text


	def move(self, fileobj, data):

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

		return moved_text



	def appendFile(self, fileobj, data):
		page = fileobj["page"]

		text_to_append = input("Enter the text to append:\n")

		for p in page:
			p = str(p)
			
			file_content = data[p]
			file_content += text_to_append
		
		return file_content


	def writeAtFile(self, fileobj, data):
		page = fileobj["page"]

		index = int(input("Give the index where you want to write at \t"))

		text_to_write = input("Enter Text\n")

		for p in page:
			text = data[str(p)]

			write_at = text[:index] + text_to_write + text[index:]

		return write_at


			
			

				

		