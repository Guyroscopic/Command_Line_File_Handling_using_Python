import threading
from thread_run_utils import *

command_full = "not empty"
simple_lock = threading.Lock()

def thread_routine(client):

	global command_full

	#Send Initial Message to Client  
	client.send("\n  ***  Connecting to remote File Management System...\n".encode())


	user_id 	  = client.recv(1024).decode()
	user_password = client.recv(1024).decode()

	user = authenticate_user(user_id, user_password)
	if type(user) == str:
		client.send(user.encode())
		return

	client.send(f"\n  ***  User Authenticated\n  ***  Welcome {user.username}\n  ***  Starting Custom CLI. NOTE: Type 'help' for more info".encode())
	while command_full:

		#Promoting the user to enter a Command
		if user.current_path == ROOT_PATH:

			client.send(f"\nroot {SPECIAL_CHAR} ".encode())
			command_full = client.recv(1024).decode()
		else:
			client.send(f"\nroot/{user.current_path} {SPECIAL_CHAR} ".encode())
			command_full = client.recv(1024).decode()

		#Checking if any command is provided
		try:
			command_func = command_full.split()[0]

		except IndexError as ie:
			#print("\nERROR: No function entered")
			client.send("\nERROR: No function entered".encode())
			continue

		#Checking is the command is valid
		if command_func not in commands:
			#print("\nERROR! No such command please try again")
			client.send("\nERROR! No such command please try again".encode())

		else:
			client.send("\nValid Command".encode())
			#If Command is critical
			if(isCritical(command_full)):				

				#Applying Lock
				with simple_lock:

					if command_func == "create":
						#create(command_full)
						pass

					elif command_func == "mkdir":
						#response = mkDir(command_full)
						#client.send(response.encode())
						#mkDir(command_full)
						pass

					elif command_func == "delete":
						#delete(command_full)
						pass

					elif command_func == "append":
						#append()
						pass

					elif command_func == "write":
						#write()
						pass

					elif command_func == "writeat":
						#writeAt(command_full)
						pass

					elif command_func == "truncate":
						#truncate(command_full)
						pass

					elif command_func == "movetext":
						#move_within_file(command_full)
						pass			

					elif command_func == "move":
						#move(command_full)
						pass

			#If command is not critical
			else:

				if command_func == "read":
					#read()
					pass

				elif command_func == "readfrom":
					#readFrom(command_full)
					pass

				elif command_func == "open":
					#Open(command_full)
					pass

				elif command_func == "close":
					#close(command_full)
					pass

				elif command_func == "showmap":
					#showMap()
					pass

				elif command_func == "cd":
					#chDir(command_full)
					pass

				elif command_func == "help":
					#help()
					pass

				elif command_func == "exit":
					##ASK IF USER WANTS AN OUTPUT FILE
					#print("\nQuitting")
					break
	
	client.close()