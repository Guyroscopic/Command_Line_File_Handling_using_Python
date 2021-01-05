from custom_os_utils import *

"""for i, item in enumerate(MENU_ITEMS):
	if i == 0:
		print(f"Chose a Command:\n\t{i+1}){item}")
	else:
		print(f"\t{i+1}){item}")"""
print("\nStarting custom CLI. NOTE: Type 'help' for more info")


while True:
        from custom_os_utils import current_path
        if current_path == ROOT_PATH:
                command_full = input(f"\nroot {SPECIAL_CHAR} ")
        else:
                command_full = input(f"\nroot/{current_path} {SPECIAL_CHAR} ")

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
                        chDir(command_full)

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

                elif command_func == "writeat":
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


