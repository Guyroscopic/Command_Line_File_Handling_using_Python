import logging
import threading
import time
#import json
from concurrent.futures import ThreadPoolExecutor
from custom_os_utils import *
from thread_run import *

with open("users.json", "r") as f:
	users_data = json.load(f)

lock = threading.Lock()

id1, password1 = 1, "12345"
id2, password2 = 2, "123"
therad_user_passwords = ["12345", "12345"]

commands_full = [["cd pop/mno", "delete thread2File"], ["cd pop/mno", "create thread2File"]]

def authenticate_user(id, password):

	try:
		user = users_data[str(id)]

		if user["password"] == password:
			return User(id, user["username"], password, [], "")
		else:
			print(f"ERROR: Wrong Password for ID {id}")
			return

	except KeyError as ke:
		print(f"ERROR: No user with ID '{id}'")
		return



def thread_routine(id):

	""" 
	This function provides the main thread execution routine.

	"""

	password = therad_user_passwords[id]

	user = authenticate_user(id, password)

	print(f"{user} logged IN")

	# reading user commands from user command file
	user_commands = readCommands(id)

	if not user_commands:
		print(f"No command found for {user.username}")

	else:
		for c in user_commands:

			#check if a command is criical
			critical = criticalCommand(c)

			#if its a critical command, it is locked
			if critical:
			    with lock:
			    	handle_commands(c, user)

			else:
				handle_commands(c, user)


	#handle_commands(commands_full[id][0], user)
	#handle_commands(commands_full[id][1], user)
	#chDir(commands_full[id][0], user)

	#with lock:
	#	create(commands_full[id][1])

	#print(f"Current  Path of {user}:", user.current_path)
	
	print(f"{user} logged OUT")


def readCommands(id):

	"""
	This function reads command file and returns 
	the commands list. If no command is found it
	return None

	"""

	#unique command file name assosciated with each thread
	command_file = "Thread" + str(id+1) + "Commands.txt"

	try:
		with open(command_file) as f:
			user_commands = f.readlines()

		#check if there are no commands in command file
		if not user_commands:
			return
		else:
			return user_commands 

	except FileNotFoundError as fnf:
		print("FILE ERROR: Command File does not exist")
		return


def criticalCommand(user_command):

	"""
	This function checks if a command is critical. If 
	the command is critical it returns True otherwise
	returns False
	"""

	#list of critical commands
	critical_commands = ["create", "delete", "mkDir", "write", "truncate", "append", "writeat"]

	user_command = user_command.split()[0]
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

"""user1 = authenticate_user(id1, password1)
user2 = authenticate_user(id2, password2)

print(user1)
print(user2)"""

