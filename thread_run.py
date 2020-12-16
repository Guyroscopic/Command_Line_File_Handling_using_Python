import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from thread_run_utils import *


id1, password1 = 1, "12345"
id2, password2 = 2, "123"
therad_user_passwords = ["12345", "12345"]

commands = ["create", "delete", "mkdir", "move", "movetext", "cd", "open", "close", "showmap", "read", "readfrom", "append", "write", "writeat", "truncate", "exit", "help"]

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
	
	#Iterating Over thread commands
	for command_full in thread_commands_full:

		command_func = command_full.split()[0]		

		#If the command is critical
		if isCritical(command_full):

			#If the Ciritical command requires a reader lock
			if isRead(command_full):
				##PERFORM READ
				if command_func == "read":
					read()
				else:
					readFrom(command_full)

            #If the Ciritical command requires a writer lock
			elif isWrite(command_full):
				#PERFORM WRITE
				if command_func == "append":
                    append()

                elif command_func == "write":
                    write()

                elif command_func == "writeat":
                    writeAt(command_full)
                        
                elif command_func == "truncate":
                    truncate(command_full)

                elif command_func == "movetext":
                    move_within_file(command_full)

            #If the Ciritical command requires a simple lock
			else:
				with simple_lock:
					## PERFORM OTHER FUCNTIONS
					if command_func == "create":                        
                        create(command_full)
				
	                elif command_func == "mkdir":                        
	                    mkDir(command_full)

	                elif command_func == "delete":                        
	                    delete(command_full)

	                elif command_func == "move":
                        move(command_full)                

	    #If the command is not critical
		else:
			##PERFORM NON_CRITICAL OPERATIONS
			if command_func == "cd":                       
                chDir(command_full)

            elif command_func == "showmap":
                showMap()

            elif command_func == "help":
                help()  

            elif command_func == "open":
                Open(command_full , user)

            elif command_func == "close":
                close(command_full, user)   

                
	print(f"{user} logged OUT")



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
