import os

ROOT_PATH  = "C:/OS_Project_root"
MENU_ITEMS = ["Create", "Delete", "MkDir", "Move", "Exit"]


def create(file_path):
        try:
                open(file_path, 'x')
                print("'" + ROOT_PATH + "/" + file_path + "' File created")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'Create <filePath>'")

        except FileExistsError as fee:
                print(f"\nERROR: File '{file_path}' already exists, delete the previous one to create new")

def delete(file_path):
        try:
                os.remove(file_path)
                print("'" + ROOT_PATH + "/" + file_path + "' File deleted")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'Delete <filePath>'")

        except FileNotFoundError as ffe:
                print(f"\nERROR: File '{file_path}' does not exist")


def mkDir(dir_path):
        try:
                os.mkdir(dir_path)
                print("'" + ROOT_PATH + "/" + dir_path + "' Directory created")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")

        except FileExistsError as fee:
                print(f"\nERROR: Directory '{dir_path}' already exists, delete the previous one to create new")


        

def  Move():
        pass


def chDir(dir_path):
        try:
                os.chdir(dir_path)
                print("'In directory " + dir_path + "'")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'ChDir <directoryPath>'")

        except FileNotFoundError as ffe:
                print(f"\nERROR: Directory '{dir_path}' not found")