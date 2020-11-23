from OS_Project_utils import *

ROOT_PATH  = "C:/OS_Project_root"
MENU_ITEMS = ["Create", "Delete", "MkDir", "Move", "Exit"]

os.system("cls")
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
		
		if command_func == "MkDir":
			try:
				dir_path = command_full.split()[1]
				mkDir(dir_path)
				print("'" + ROOT_PATH + "/" + dir_path + "' Directory created")

			except IndexError as ie:
				print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")

			except FileExistsError as fee:
				print(f"\nERROR: Directory '{dir_path}' already exists, delete the previous one to create new")


