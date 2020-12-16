ROOT_PATH  = ""

class User:

	#Constructor
	def __init__(self, id, username, password, current_files=[], current_path=ROOT_PATH):
		self.id   		   = id
		self.username 	   = username
		self.password      = password
		self.current_files = current_files
		self.current_path  = current_path

	#for printing the object
	def __repr__(self):
		return f"User: {self.username} with ID {self.id}"

	def getCurrentFileNames(self):
		return [file.name for  file in self.current_files]








