import logging
import threading
import time
from user import *
import json


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

	print(f"User {user.id} has logged in")
	time.sleep(0.1)

	print(f"User {user.id} is going to perform some tasks")
	read_command(user.id)

	print(f"User {user.id} loggin out")



def read_command(id):

	commands_file = "user" + str(id) + "_commands.txt"

	try:
		with open(commands_file, "r") as f:
			commands = f.readlines()

		print(f"User {id} has asked to :")
		for command in commands:
			print(command.strip())
			
		print("")

	except Exception as FileNotFoundError:
		print(f"User {id} does not have privilage to run commands")



thread1 = threading.Thread(target=thread_routine, args=(1,))
thread2 = threading.Thread(target=thread_routine, args=(2,))

thread1.start()
thread2.start()

"""
user1 = authenticate_user(id1, password1)
user2 = authenticate_user(id2, password2)


print(user1)
print(user2)"""

