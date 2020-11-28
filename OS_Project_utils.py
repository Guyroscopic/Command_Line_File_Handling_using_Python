import os
import json

ROOT_PATH  = "C:/OS_Project_root"
MENU_ITEMS = ["Create", "Delete", "MkDir", "Move", "Exit"]

with open("structure.json") as f:
  structure = json.load(f)

root = structure["root"]


def create(command_full):

        file_path = command_full.split()[1]
        try:
                open(file_path, 'x')
                print("'" + ROOT_PATH + "/" + file_path + "' File created")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'Create <filePath>'")

        except FileExistsError as fee:
                print(f"\nERROR: File '{file_path}' already exists, delete the previous one to create new")

def delete(command_full):

        file_path = command_full.split()[1]
        try:
                os.remove(file_path)
                print("'" + ROOT_PATH + "/" + file_path + "' File deleted")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'Delete <filePath>'")

        except FileNotFoundError as ffe:
                print(f"\nERROR: File '{file_path}' does not exist")


def mkDir(command_full):
       
    try:
        dir_path = command_full.split()[1]
        dir_to_create = dir_path.split("/")[-1]
        dir_to_update = dir_path.split("/")[:-1]
        hierarchy = checkHierarchy(dir_to_update)

        if type(hierarchy) == str:
            print(f"\nERROR: Directory '{hierarchy}' could not be found")
        else:
            ##MAKE THE DIR IN STRUCTURE LOGIC
            print("\ndir found")
            try:
                #Checking if the Directorry already exists
                hierarchy[dir_to_create]
                print(f"ERROR: Directory '{dir_path}' already exists")
            except KeyError as ke:
                #Adding the directory to Parent Directory
                hierarchy[dir_to_create] = {"type": "dir"}

                #Updating the structure file
                str_to_exec = "root"
                for i in range(len(dir_to_update)):
                    str_to_exec += f"[dir_to_update[{i}]]"
                str_to_exec += " = hierarchy"

                #print("\nTO EXEC:", str_to_exec)
                #for i in range(len(dir_to_update)):
                #    print(dir_to_update[i])

                print("\nOLDD", structure, "\n")
                exec(str_to_exec)
                structure["root"] = root

                print(structure)
                with open("structure.json", "w") as f:
                    print("Inside Write")
                    json.dump(structure, f)
            
        #os.mkdir(dir_path)
        #print("'" + ROOT_PATH + "/" + dir_path + "' Directory created")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")

    #except FileExistsError as fee:
    #    print(f"\nERROR: Directory '{dir_path}' already exists, delete the previous one to create new")


        

def  Move():
    pass


def chDir(command_full):

        dir_path = command_full.split()[1]
        try:
                os.chdir(dir_path)
                print("'In directory " + dir_path + "'")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'ChDir <directoryPath>'")

        except FileNotFoundError as ffe:
                print(f"\nERROR: Directory '{dir_path}' not found")



def checkHierarchy(file_path):

    print("\nFILE PATH IN checkHierarchy():", file_path, "\n")

    dirs_without_keys = root
    dir_str = ""

    for idx, dir_name in enumerate(file_path):
        #print("for loop iteration", idx)
        if file_path[idx] in dirs_without_keys.keys():
            #print(file_path[idx], "found inside", dirs)
            dir_str += "/" + file_path[idx]
            #print("dir_str:", dir_str)
            dirs_without_keys = updateDirList(dir_str)
            #print("dirs updated:", dirs)
        else:
            return dir_str + "/" + file_path[idx]

    return dirs_without_keys

def updateDirList(dir_str):

    found_dir_hierarchy = dir_str.split("/")[1:]
    #print("found_dir_hierarchy:", found_dir_hierarchy)

    temp = root

    for i in found_dir_hierarchy:
        temp = temp[i]

    return temp
            
        


