import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from thread_run_utils import *


id1, password1 = 1, "12345"
id2, password2 = 2, "123"
therad_user_passwords = ["12345", "12345",  "12345"]

commands = ["create", "delete", "mkdir", "move", "movetext", "cd", "open", "close", "showmap", "showmemorymap", "read", "readfrom", "append", "write", "writeat", "truncate", "exit", "help"]

simple_lock = threading.Lock()

def thread_routine(id):

	""" 
	This function provides the main thread execution routine.

	"""

	password = therad_user_passwords[id]
	user = authenticate_user(id, password)

	print(f"{user} logged IN")

	#Getting Thread commands
	thread_commands_full = getThreadCommandfromId(id)

	for i in range(len(thread_commands_full)):
		if thread_commands_full[i][-1] == "\n":
			thread_commands_full[i] = thread_commands_full[i][:-1]


	#Iterating Over thread commands
	for command_full in thread_commands_full:

		command_func = command_full.split()[0]
		#print("Command Full:", command_full)
		#print("Command Fucntion:", command_func, len(command_func))		

		#If the command is critical
		if isCritical(command_full):			

			with simple_lock:

				if command_func == "read":
					read(command_full, user)
					
				elif command_func == "readfrom":
					readFrom(command_full, user)
		      
				elif command_func == "append":
					append(command_full, user)

				elif command_func == "write":
					write(command_full, user)

				elif command_func == "writeat":
					writeAt(command_full)

				elif command_func == "truncate":
					truncate(command_full, user)

				elif command_func == "movetext":
					move_within_file(command_full, user)				
					
				elif command_func == "create":
					create(command_full, user)

				elif command_func == "mkdir":
					mkDir(command_full, user)

				elif command_func == "delete":
					delete(command_full, user)

				elif command_func == "move":
					move(command_full, user)

				elif command_func == "showmap":
					showMap(user)

				elif command_func == "showmemorymap":
					showMemoryMap(command_full, user)               

	    #If the command is not critical
		else:
			##PERFORM NON_CRITICAL OPERATIONS
			if command_func == "cd":
				chDir(command_full, user)			

			elif command_func == "help":
				help()

			elif command_func == "open":
				Open(command_full, user)

			elif command_func == "close":
				close(command_full, user)

	print(f"{user} logged OUT")
	


#thread0 = threading.Thread(target=thread_routine, args=(0,))
thread1 = threading.Thread(target=thread_routine, args=(1,))
#thread2 = threading.Thread(target=thread_routine, args=(2,))

"""args = [0, 1]
with ThreadPoolExecutor(max_workers=2) as executor:
		executor.map(thread_routine, args)


"""
#thread0.start()
thread1.start()
#thread2.start()

#thread0.join()
thread1.join()
#thread2.join()
