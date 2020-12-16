import logging
import threading
import time
from queue import Queue
from user import *
import json
from run import *

with open("users.json", "r") as f:
	users_data = json.load(f)


id1, password1 = 1, "12345"
id2, password2 = 2, "123"
therad_user_passwords = ["12345", "12345"]

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

	password = therad_user_passwords[id-1]

	user = authenticate_user(id, password)

	print(f"{user} logged IN")
	time.sleep(0.1)

	#reading commands
	command_q = read_command(user.id)

	print(f"Executing Commands for {user.id}")
	if command_q:
		handle_commands(user, command_q)
	else:
		pass

	print(f"{user} logged OUT")



#function to read commands and push them into the queue
def read_command(id):

	commands_file = "user" + str(id) + "_commands.txt"
	try:
		with open(commands_file, "r") as f:
			user_commands = f.readlines()

		return user_commands

	except FileNotFoundError as fnfe:
		print(f"No commands found")
		return




thread1 = threading.Thread(target=thread_routine, args=(1,))
thread2 = threading.Thread(target=thread_routine, args=(2,))

thread1.start()
thread2.start()

"""
user1 = authenticate_user(id1, password1)
user2 = authenticate_user(id2, password2)


print(user1)
print(user2)"""

