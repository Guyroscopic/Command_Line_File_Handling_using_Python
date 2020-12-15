import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from thread_run import *


id1, password1 = 1, "12345"
id2, password2 = 2, "123"
therad_user_passwords = ["12345", "12345"]

commands = ["create", "delete", "mkdir", "move", "movetext", "cd", "open", "close", "showmap", "read", "readfrom", "append", "write", "writeat", "truncate", "exit", "help"]

lock = threading.Lock()

def thread_routine(id):

	""" 
	This function provides the main thread execution routine.

	"""

	password = therad_user_passwords[id]

	user = authenticate_user(id, password)

	print(f"{user} logged IN")

	# reading user commands from user command file
	user_commands = getThreadCommandfromId(id)

	if user_commands is None:
		print(f"No command found for {user.username}")

	else:
		for command in user_commands:

			#check if a command is criical

			#if its a critical command, it is locked
			if isCritical(command):
				with lock:
					getFunctionNamefromCommand(command, user)

			elif isCritical(command) is None:
				pass

			else:
				getFunctionNamefromCommand(command, user)

	print(f"{user} logged OUT")



def isCritical(user_command):

	"""
	This function checks if a command is critical. If 
	the command is critical it returns True otherwise
	returns False
	"""

	command_func = user_command.split()[0]
	
	# first cehck if user command is valid   
	if command_func not in commands:
		print("\nERROR! No such command please try again")
		return

	#list of critical commands
	critical_commands = ["open", "create", "delete", "mkDir", "write", "truncate", "append", "writeat"]

	if user_command in critical_commands:
		return True

	else:
		return False



thread1 = threading.Thread(target=thread_routine, args=(0,))
thread2 = threading.Thread(target=thread_routine, args=(1,))

"""args = [0, 1]
with ThreadPoolExecutor(max_workers=2) as executor:
		executor.map(thread_routine, args)


"""

thread1.start()
thread2.start()

thread1.join()
thread2.join()
