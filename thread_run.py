from custom_os_utils import *
import threading
commands = ["create", "delete", "mkdir", "move", "movetext", "cd", "open", "close", "showmap", "read", "readfrom", "append", "write", "writeat", "truncate", "exit", "help"]

lock = threading.Lock()

for i, item in enumerate(commands):
	if i == 0:
		print(f"Chose a Command:\n\t{i+1}){item}")
	else:
		print(f"\t{i+1}){item}")
print("\nStarting custom CLI. NOTE: Type 'help' for more info")


def handle_commands(user_command, user):


        #from custom_os_utils import current_path
        """if user.current_path == ROOT_PATH:
                command_full = print("\nroot" + SPECIAL_CHAR + user_command)
        else:
                command_full = print("\nroot/" + user.current_path + SPECIAL_CHAR + user_command)"""
        try:
                command_func = user_command.split()[0]
        except IndexError as ie:
                print("\nERROR: No function entered")
                

        if command_func not in commands:
                print("\nERROR! No such command please try again")
        else:
                if command_func == "create": 
                        with lock:
                                create(user_command)
				
                elif command_func == "mkdir":
                        with lock:
                                mkDir(user_command)                       
                        
                elif command_func == "delete":
                        with lock:
                                delete(user_command)

                elif command_func == "cd":                       
                        user.current_path = chDir(user_command, user)

                elif command_func == "open":
                        Open(user_command)

                elif command_func == "close":
                        close(user_command)

                elif command_func == "read":
                        read()

                elif command_func == "readfrom":
                        readFrom(user_command)

                elif command_func == "append":
                        append()

                elif command_func == "write":
                        write()

                elif command_func == "WriteAt":
                        writeAt(user_command)
                        
                elif command_func == "truncate":
                        truncate(user_command)

                elif command_func == "movetext":
                        move_within_file(user_command)
                        
                elif command_func == "showmap":
                        showMap()

                elif command_func == "move":
                        move(user_command)

                elif command_func == "help":
                        help()     

                elif command_func == "exit":
                        print("\nQuitting")


