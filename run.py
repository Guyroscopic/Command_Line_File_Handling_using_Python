from custom_os_utils import *

MENU_ITEMS = ["Create", "Delete", "MkDir", "Move", "ChDir", "Open", "Close", "ShowMap", "Read", "ReadFrom", "Append", "Write", "WriteAt", "Truncate", "Exit"]


for i, item in enumerate(MENU_ITEMS):
	if i == 0:
		print(f"Chose a Command:\n\t{i+1}){item}")
	else:
		print(f"\t{i+1}){item}")


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

        if command_func not in MENU_ITEMS:
                print("\nERROR! No such command please try again")
        else:
                if command_func == "Create":                        
                        create(command_full)
				
                elif command_func == "MkDir":                        
                        mkDir(command_full)

                elif command_func == "Delete":                        
                        delete(command_full)

                elif command_func == "ChDir":                       
                        current_path = chDir(command_full)

                elif command_func == "Open":
                        Open(command_full)

                elif command_func == "Close":
                        close(command_full)

                elif command_func == "Read":
                        read()

                elif command_func == "ReadFrom":
                        readFrom()

                elif command_func == "Append":
                        append()

                elif command_func == "Write":
                        write()

                elif command_func == "WriteAt":
                        writeAt()
                        
                elif command_func == "Truncate":
                        truncate()
                        
                elif command_func == "ShowMap":
                        showMap()                

                elif command_func == "Exit":
                        print("\nQuitting")
                        break


