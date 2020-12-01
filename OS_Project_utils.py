import os
import json
from FileClass import FileClass

f = ""
ROOT_PATH  = ""
current_path = ROOT_PATH

print("Current Path: ", current_path)

with open("structure.json") as f:
  structure = json.load(f)

root = structure["root"]
data = structure["data"]

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

        except IndexError as ie:
                print("\nERROR: No File name or path specified, usage: 'Create <filePath>'")


def delete(command_full):

        try:
            file_path      = command_full.split()[1]
            file_path      = current_path + file_path
            file_to_delete = file_path.split("/")[-1]
            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)

            if type(hierarchy) == str:
                print(f"\nERROR: Directory '{hierarchy}' could not be found")
            else:
                try:
                    #Checking if the File exists
                    hierarchy[file_to_delete]
                    
                    if hierarchy[file_to_delete]["type"] != "file":
                        print(f"'{file_path}' is not a file")

                    else:
                        hierarchy.pop(file_to_delete)

                        with open("structure.json", "w") as f:
                            json.dump(structure, f)

                        print(f"File '{file_path}.txt' DELETED")

                except KeyError as ke:
                    #If the file does not Exist
                    print(f"File {file_path}.txt does not exist")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'Delete <filePath>'")


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

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'MkDir <directoryPath>'")
       

def  Move(command_full):    
    pass


def showMap():

    global current_path

    current_dict = getDirDictFromPath(current_path)
    prettyPrint(current_dict, 1)



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

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'ChDir <directoryPath>'")



def Open(command_full):
    
    global f

    try:
        file_path      = command_full.split()[1]
        mode = command_full.split()[2]
        file_path      = current_path + file_path
        file_to_open = file_path.split("/")[-1]
        parent_dir     = file_path.split("/")[:-1]
        hierarchy      = checkHierarchy(parent_dir)


        if type(hierarchy) == str:
            print("File does not exist")
            
        try:
            #Checking if the File exists
            hierarchy[file_to_open]
                    
            if hierarchy[file_to_open]["type"] != "file":
                print(f"'{file_path}' is not a file")

            else:
                f = FileClass(file_to_open, hierarchy[file_to_open])
                print("File Opened")

                if mode == 'r':
                    print("reading file")

                    f.readFile(hierarchy[file_to_open], data)

                elif mode == 'rf':
                    f.readFileFrom(hierarchy[file_to_open], data)

                elif mode == 'a':
                    text_appended = f.appendFile(hierarchy[file_to_open], data)

                    file_ob = hierarchy[file_to_open]
                    page = file_ob["page"]

                    for p in page:
                        data[str(p)] = text_appended
                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                elif mode == 't':
                    truncate_text = f.truncate(hierarchy[file_to_open], data)

                    file_ob = hierarchy[file_to_open]
                    page = file_ob["page"]
                    for p in page:
                        data[str(p)] = truncate_text
                    with open("structure.json", "w") as f:
                            json.dump(structure, f)
                            

                elif mode == 'mov':
                    move_text = f.move(hierarchy[file_to_open], data)
                    file_ob = hierarchy[file_to_open]
                    page = file_ob["page"]
                    for p in page:
                        data[str(p)] = move_text
                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                elif mode == 'wa':
                    write_text = f.writeAtFile(hierarchy[file_to_open], data)
                    file_ob = hierarchy[file_to_open]
                    page = file_ob["page"]
                    for p in page:
                        data[str(p)] = write_text
                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                else:
                    print("Invalid Mode")

        except KeyError as ke:
            #If the file does not Exist
            print(f"File {file_path}.txt does not exist")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'Open <fileName> <mode[r, rf, w, wa, a, t]>'")


''' This functioon closes the file '''

def close(command_full):
    global f
    try:
        file_path      = command_full.split()[1]
        file_path      = current_path + file_path
        file_to_close = file_path.split("/")[-1]
        parent_dir     = file_path.split("/")[:-1]
        hierarchy      = checkHierarchy(parent_dir)

        if type(hierarchy) == str:
            print("File does not exist")
            
        try:
            #Checking if the File exists
            hierarchy[file_to_close]
                    
            if hierarchy[file_to_close]["type"] != "file":
                print(f"'{file_path}' is not a file")

            else:
                if file_to_close == f.name:
                    f = None
                    print("File Closed\n")

                else:
                    print("File is not opened")

        except KeyError as ke:
            #If the file does not Exist
            print(f"File {file_path}.txt does not exist")
    

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'Open <fileName> <mode[r, w, a]>'")


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
            if dir_str == "":
                dir_str +=  path[idx]
            else:
                dir_str += "/" + path[idx]
            #print("dir_str:", dir_str)
            dir_dict = getDirDictFromPath(dir_str)
            #print("dirs updated:", dir_dict.keys())
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

    temp = root

    if not dir_path:
        return temp
    
    found_dir_hierarchy = dir_path.split("/")
    for i in found_dir_hierarchy:
        temp = temp[i]

    return temp


def prettyPrint(d, indent=0):

    """
    A function used to pretty print the file structure
    """

    for key, value in d.items():

        if key != "type" and key != "extension" and key != "data":
            
            if isinstance(value, dict):
                print('  ' * indent + str(key) + ": " + str(value["type"]))
                prettyPrint(value, indent+1)
            else:
                print('  ' * (indent+1) + str(value))


            
        


