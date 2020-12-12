import logging
import threading
import time
from user import *
import json


with open("users.json", "r") as f:
	users_data = json.load(f)


id1, password1 = 1, "12345"
id2, password2 = 2, "123"


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


user1 = authenticate_user(id1, password1)
user2 = authenticate_user(id2, password2)


print(user1)
print(user2)