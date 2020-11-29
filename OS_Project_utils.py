import os
import json

ROOT_PATH  = ""
current_path = ROOT_PATH

print("Current Path: ", current_path)

with open("structure.json") as f:
  structure = json.load(f)

root = structure["root"]


def create(command_full):
        
        try:
            file_path      = command_full.split()[1]
            file_path      = current_path + file_path
            file_to_create = file_path.split("/")[-1]
            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)

            if type(hierarchy) == str:
                print(f"\nERROR: Directory '{hierarchy}' could not be found")
            else:
                try:
                    #Checking if the File already exists
                    hierarchy[file_to_create]
                    print(f"ERROR: File '{file_path}' already exists")

                except KeyError as ke:
                    hierarchy[file_to_create] = {
                                                    "type"     : "file",
                                                    "extension": ".txt"
                                                }

                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                    print(f"File '{file_path}.txt' created")


            #open(file_path, 'x')
            #print("'" + ROOT_PATH + "/" + file_path + "' File created")

        except IndexError as ie:
                print("\nERROR: No File name or path specified, usage: 'Create <filePath>'")

        #except FileExistsError as fee:
        #       print(f"\nERROR: File '{file_path}' already exists, delete the previous one to create new")

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
        #print("PATH in mkdir:", dir_path)
        dir_to_create = dir_path.split("/")[-1]
        parent_dir = dir_path.split("/")[:-1]
        hierarchy = checkHierarchy(parent_dir)

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
                    #print(f)  
                    #print(structure)                 
                    json.dump(structure, f)
                    #f.write(json_str)
                    #f.flush()
                    #print("Inside Write")

                print(f"Directory '{dir_path}' Created")
                    
            
        #os.mkdir(dir_path)
        #print("'" + ROOT_PATH + "/" + dir_path + "' Directory created")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")

    #except FileExistsError as fee:
    #    print(f"\nERROR: Directory '{dir_path}' already exists, delete the previous one to create new")


        

def  Move(command_full):
    
    try:
        source_file = command_full.split()[1]
        target_file = 


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



def checkHierarchy(path):

    #print("\nFILE PATH IN checkHierarchy():", file_path, "\n")
    """
    A Function tat checks the validity of a path in the file structure
    If the argument 'path' is valid, the function returns a dictionary Object of the file/dir,
    else returns a String that specifies the invalid path
    ARGUMENTS: path: list 
    """

    dir_dict = root
    dir_str = ""

    for idx, dir_name in enumerate(path):
        #print("for loop iteration", idx)
        if path[idx] in dir_dict.keys():
            #print(file_path[idx], "found inside", dirs)
            dir_str += "/" + path[idx]
            #print("dir_str:", dir_str)
            dir_dict = getDirDictFromPath(dir_str)
            #print("dirs updated:", dirs)
        else:
            #Returning invalid path string
            return dir_str + "/" + path[idx]

    #Returning Directory dictionary object
    return dir_dict

def getDirDictFromPath(dir_path):

    """   
    A fucntion that returns dictionary object of directory
    ARGUMENTS: dir_path: str 
    """

    found_dir_hierarchy = dir_path.split("/")[1:]
    #print("found_dir_hierarchy:", found_dir_hierarchy)

    temp = root

    for i in found_dir_hierarchy:
        temp = temp[i]

    return temp


            
        


