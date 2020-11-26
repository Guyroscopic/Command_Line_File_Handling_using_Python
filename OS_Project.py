from OS_Project_utils import *
import os

ROOT_PATH  = "C:/OS_Project_root"
MENU_ITEMS = ["Create", "Delete", "MkDir", "ChDir", "Move", "Exit"]

os.system("cls")

#if the root os path does not exist
if not os.path.isdir(ROOT_PATH):
        os.chdir("C:/")
        os.mkdir("C:/OS_Project_root")
        print("Directory did not exist So created one")
        
os.chdir(ROOT_PATH)


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
                        file_path = command_full.split()[1]
                        create(file_path)
				
                elif command_func == "MkDir":
                        dir_path = command_full.split()[1]
                        mkDir(dir_path)

                elif command_func == "Delete":
                        file_path = command_full.split()[1]
                        delete(file_path)

                elif command_func == "ChDir":
                        dir_path = command_full.split()[1]
                        chDir(dir_path)

                elif command_func == "Exit":
                        print("\nQuitting")
                        break


