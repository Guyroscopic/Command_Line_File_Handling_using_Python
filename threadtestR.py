import logging
import threading
import time
#import json
from concurrent.futures import ThreadPoolExecutor
from custom_os_utils import *


with open("users.json", "r") as f:
	users_data = json.load(f)

lock = threading.Lock()

id1, password1 = 1, "12345"
id2, password2 = 2, "123"
therad_user_passwords = ["12345", "12345"]

#commands_full = [["cd pop/mno", "create thread1File"], ["cd pop/mno", "create thread1File"]]

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

	password = therad_user_passwords[id]

	user = authenticate_user(id, password)

	print(f"{user} logged IN")

	chDir(commands_full[id][0], user)

	with lock:
		create(commands_full[id][1])

	print(f"Current  Path of {user}:", user.current_path)
	
	print(f"{user} logged OUT")



#thread1 = threading.Thread(target=thread_routine, args=(0,))
#thread2 = threading.Thread(target=thread_routine, args=(1,))

args = [0, 1]
with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(thread_routine, args)


"""

thread1.start()
thread2.start()

user1 = authenticate_user(id1, password1)
user2 = authenticate_user(id2, password2)


print(user1)
print(user2)"""

