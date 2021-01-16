import threading
from thread_run_utils import *

threads = {}
#invalid_creds = False
#command_full  = "not empty"
simple_lock   = threading.Lock()

#Adding the invalid creds command
commands.append("invalid_creds")

def thread_routine(client, client_addr):

	global command_full

	#invalid_creds = False
	command_full  = "not empty"

	#Send Initial Message to Client  
	client.send("\n  ***  Connecting to remote File Management System...\n".encode())

	#Recieving Client Credentials
	user_id 	  = client.recv(1024).decode()
	user_password = client.recv(1024).decode()

	#Authenticating User
	user = authenticate_user(user_id, user_password)
	if type(user) == str:		
		command_full = "invalid_creds"

	else:
		client.send(f"\n  ***  User Authenticated\n  ***  Welcome {user.username}\n  ***  Starting Custom CLI. NOTE: Type 'help' for more info".encode())
		
	while command_full:

		#Promoting the user to enter a Command
		if command_full != "invalid_creds":
			if user.current_path == ROOT_PATH:

				client.send(f"\nroot {SPECIAL_CHAR} ".encode())
				command_full = client.recv(1024).decode()
			else:
				client.send(f"\nroot/{user.current_path} {SPECIAL_CHAR} ".encode())
				command_full = client.recv(1024).decode()

		#Checking if any command is provided
		try:
			command_func = command_full.split()[0]
			#print("COMMAND FUNC: ",  command_func)

		except IndexError as ie:
			#print("\nERROR: No function entered")
			client.send("\nERROR: No function entered".encode())
			continue

		#Checking is the command is valid
		if command_func not in commands:
			#print("\nERROR! No such command please try again")
			client.send("\nERROR! No such command please try again".encode())

		else:
			#If Command is critical
			if(isCritical(command_full)):				

				#Applying Lock
				with simple_lock:

					if command_func == "create":
						response = create(command_full, user)
						client.send(response.encode())

					elif command_func == "mkdir":
						response = mkDir(command_full, user)
						client.send(response.encode())

					elif command_func == "delete":
						response = delete(command_full, user)
						client.send(response.encode())

					elif command_func == "append":
						client.send("Enter Text to Append:".encode())
						text = client.recv(1024).decode()

						response = append(command_full, user, text)
						client.send(response.encode())

					elif command_func == "write":
						client.send("Enter Text to Write:".encode())
						text = client.recv(1024).decode()

						response = write(command_full, user, text)
						client.send(response.encode())

					elif command_func == "writeat":
						client.send("Enter Text to Write:".encode())
						text = client.recv(1024).decode()

						response = writeat(command_full, user, text)
						client.send(response.encode())

					elif command_func == "truncate":
						response = truncate(command_full, user)
						client.send(response.encode())

					elif command_func == "movetext":
						response = movetext(command_full, user)
						client.send(response.encode())			

					elif command_func == "move":
						response = move(command_full, user)
						client.send(response.encode())

			#If command is not critical
			else:

				if command_func == "read":
					response = read(command_full, user)
					client.send(response.encode())

				elif command_func == "readfrom":
					response = readFrom(command_full, user)
					client.send(response.encode())

				elif command_func == "open":
					response = Open(command_full, user)
					client.send(response.encode())

				elif command_func == "close":
					response = close(command_full, user)
					client.send(response.encode())

				elif command_func == "showmap":
					response = showMap(user)
					client.send(response.encode())

				elif command_func == "showfilemap":
					response = showMemoryMap(command_full, user)
					client.send(response.encode())

				elif command_func == "cd":
					response = chDir(command_full, user)
					client.send(response.encode())

				elif command_func == "help":
					response = help()
					client.send(response.encode())

				elif command_func == "exit":					
					print(f"{user.username} is Quitting")
					client.send("exit".encode())
					command_full = ""
					#break

				elif command_func == "invalid_creds":
					print(f"Invalid Credentials...")
					client.send("invalid_creds".encode())
					command_full = ""
	
	#Closing Connection
	print(f"closing connection from {client_addr}")
	threads.pop(client_addr)
	client.close()