class User:

	#Constructor
	def __init__(self, id, username, password, current_files=[], current_path=""):
		self.id   		   = id
		self.username 	   = username
		self.password      = password
		self.current_files = current_files
		self.current_path  = current_path

	#toString
	def __repr__(self):
		return f"{self.username} {self.id}"








