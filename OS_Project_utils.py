import os
import json

ROOT_PATH  = ""

current_path = ROOT_PATH

with open("structure.json") as f:
  structure = json.load(f)

print(structure)

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
        dir_path = current_path + dir_path
        print("PATH in mkdir:", dir_path)
        dir_to_create = dir_path.split("/")[-1]
        dir_to_update = dir_path.split("/")[:-1]
        hierarchy = checkHierarchy(dir_to_update)

        if type(hierarchy) == str:
            print(f"\nERROR: Directory '{hierarchy}' could not be found")
        else:
            #MAKE THE DIR IN STRUCTURE LOGIC
            try:
                #Checking if the Directorry already exists
                hierarchy[dir_to_create]
                print(f"ERROR: Directory '{dir_path}' already exists")
            except KeyError as ke:

                #Adding the directory to Parent Directory
                print("Creating the Dir")
                hierarchy[dir_to_create] = {"type": "dir"}

                #print(structure)
                with open("structure.json", "w") as f: 
                    print(f)  
                    print(structure)                 
                    json_str = json.dumps(structure)
                    f.write(json_str)
                    f.flush()
                    print("Inside Write")

                print("Directory Created")
                    
            
        #os.mkdir(dir_path)
        #print("'" + ROOT_PATH + "/" + dir_path + "' Directory created")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")

    #except FileExistsError as fee:
    #    print(f"\nERROR: Directory '{dir_path}' already exists, delete the previous one to create new")


        

def  Move():
    pass


def chDir(command_full):

    global current_path
        
    try:
        dir_path = command_full.split()[1]
        hierarchy = checkHierarchy(dir_path.split("/"))

        if type(hierarchy) == str:
            print(f"\nERROR: Directory '{hierarchy}' could not be found")
        else:
            print(f"Setting current path to '{dir_path}'")
            current_path = dir_path + "/"
            #print(current_path)

            #os.chdir(dir_path)
            #print("'In directory " + dir_path + "'")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'ChDir <directoryPath>'")

        #except FileNotFoundError as ffe:
        #       print(f"\nERROR: Directory '{dir_path}' not found")



def checkHierarchy(file_path):

    #print("\nFILE PATH IN checkHierarchy():", file_path, "\n")

    dirs_without_keys = root
    dir_str = ""

    for idx, dir_name in enumerate(file_path):
        #print("for loop iteration", idx)
        if file_path[idx] in dirs_without_keys.keys():
            #print(file_path[idx], "found inside", dirs)
            dir_str += "/" + file_path[idx]
            #print("dir_str:", dir_str)
            dirs_without_keys = getDirDictFromPath(dir_str)
            #print("dirs updated:", dirs)
        else:
            return dir_str + "/" + file_path[idx]

    return dirs_without_keys

def getDirDictFromPath(dir_str):

    found_dir_hierarchy = dir_str.split("/")[1:]
    #print("found_dir_hierarchy:", found_dir_hierarchy)

    temp = root

    for i in found_dir_hierarchy:
        temp = temp[i]

    return temp


            
        


