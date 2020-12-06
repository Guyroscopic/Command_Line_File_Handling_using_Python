from custom_os_utils import *

MENU_ITEMS = ["Create", "Delete", "MkDir", "Move", "ChDir", "Open", "Close", "ShowMap", "Read", "ReadFrom", "Append", "Truncate", "Exit"]

#os.system("cls")


#if the root os path does not exist
#if not os.path.isdir(ROOT_PATH):
#        os.chdir("C:/")
#        os.mkdir("C:/OS_Project_root")
#        print("Directory did not exist So created one")
        
#os.chdir(ROOT_PATH)


for i, item in enumerate(MENU_ITEMS):
	if i == 0:
		print(f"Chose a Command:\n\t{i+1}){item}")
	else:
		print(f"\t{i+1}){item}")


while True:

        command_full = input("\nEnter a Command: ")

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
                        
                elif command_func == "Truncate":
                        truncate()
                        
                elif command_func == "ShowMap":
                        showMap()                

                elif command_func == "Exit":
                        print("\nQuitting")
                        break


