from custom_os_utils import *

commands = ["create", "delete", "mkdir", "move", "movetext", "cd", "open", "close", "showmap", "read", "readfrom", "append", "write", "writeat", "truncate", "exit", "help"]


for i, item in enumerate(commands):
	if i == 0:
		print(f"Chose a Command:\n\t{i+1}){item}")
	else:
		print(f"\t{i+1}){item}")
print("\nStarting custom CLI. NOTE: Type 'help' for more info")


def handle_commands(user, user_commands):

        for command_full in user_commands:

                #from custom_os_utils import current_path
                if user.current_path == ROOT_PATH:
                        command_full = "\nroot" + SPECIAL_CHAR +command_full
                else:
                        command_full = "\nroot/" + user.current_path + SPECIAL_CHAR + command_full

                try:
                        command_func = command_full.split()[0]
                except IndexError as ie:
                        print("\nERROR: No function entered")
                        continue

                if command_func not in commands:
                        print("\nERROR! No such command please try again")
                else:
                        if command_func == "create":                        
                                create(command_full)
        				
                        elif command_func == "mkdir":                        
                                mkDir(command_full)

                        elif command_func == "delete":                        
                                delete(command_full)

                        elif command_func == "cd":                       
                                user.current_path = chDir(command_full, user)

                        elif command_func == "open":
                                Open(command_full)

                        elif command_func == "close":
                                close(command_full)

                        elif command_func == "read":
                                read()

                        elif command_func == "readfrom":
                                readFrom(command_full)

                        elif command_func == "append":
                                append()

                        elif command_func == "write":
                                write()

                        elif command_func == "WriteAt":
                                writeAt(command_full)
                                
                        elif command_func == "truncate":
                                truncate(command_full)

                        elif command_func == "movetext":
                                move_within_file(command_full)
                                
                        elif command_func == "showmap":
                                showMap()

                        elif command_func == "move":
                                move(command_full)

                        elif command_func == "help":
                                help()     

                        elif command_func == "exit":
                                print("\nQuitting")
                                break


