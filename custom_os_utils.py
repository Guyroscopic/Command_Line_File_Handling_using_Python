
from FileClass import *
from user import *

#ROOT_PATH  = ""
current_path = ROOT_PATH
current_file = None


#print(len(data["0"]))

######################      Function that operate on/modify File structure    ################

def create(command_full, user):
        
        try:
            file_path      = command_full.split()[1]
            file_path      = getAbsPathfromRelPath(file_path, user)
           
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
                                                    "extension": ".txt",
                                                    "data"     : {}
                                                }

                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                    print(f"File '{file_path}.txt' created by {user}")

        except IndexError as ie:
                print("\nERROR: No File name or path specified, usage: 'create <filePath>'")


def delete(command_full, user):

        try:
            file_path      = command_full.split()[1]
            file_path      = getAbsPathfromRelPath(file_path, user)
            file_to_delete = file_path.split("/")[-1]
            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)

            #print("PATH: ", file_path)
            if type(hierarchy) == str:
                print(f"\nERROR: Directory '{hierarchy}' could not be found")
            else:
                try:
                    #Checking if the File exists
                    hierarchy[file_to_delete]
                    
                    if hierarchy[file_to_delete]["type"] != "file":
                        print(f"'{file_path}' is not a file")

                    else:

                        #if current_file.file_dict == hierarchy:
                        #    print(f"ERROR: File {hierarchy}.txt is opened, close before deleting using 'close' command")
                        #    return

                        hierarchy.pop(file_to_delete)

                        with open("structure.json", "w") as f:
                            json.dump(structure, f)

                        print(f"File '{file_path}.txt' deleted by {user}")

                except KeyError as ke:
                    #If the file does not Exist
                    print(f"File {file_path}.txt does not exist")

        except IndexError as ie:
                print("\nERROR: No Directory name or path specified, usage: 'delete <filePath>'")


def mkDir(command_full, user):
       
    try:
        dir_path = command_full.split()[1]
        dir_path = getAbsPathfromRelPath(dir_path, user)
        
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
                hierarchy[dir_to_create] = {"type": "dir"}

                #print(structure)
                with open("structure.json", "w") as f:                  
                    json.dump(structure, f)

                print(f"Directory '{dir_path}' Created")

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'mkdir <directoryPath>'")
       

def chDir(command_full, user):

    global current_path
        
    try:
        dir_path = command_full.split()[1]

        if dir_path == "..":
            dir_path = getParent(user.current_path)
        else:
            dir_path = getAbsPathfromRelPath(dir_path, user)

        
        #Logic For moving upward in the File Structure to root
        if dir_path == ROOT_PATH:            
            if user.current_path == ROOT_PATH:
                print(f"Already in root")
                return
            else:

                user.current_path = ROOT_PATH
                print(f"Setting current path to root")
                return

        #Logic For moving upward or downward in the FIle Structure according to the user input
        hierarchy = checkHierarchy(dir_path.split("/"))
        
        if type(hierarchy) == str:
            print(f"\nERROR: Directory '{hierarchy}' could not be found")
            
        else:

            if hierarchy["type"] != "dir":
                print(f"ERROR: {dir_path} is not a directory")

            else:
                print(f"Setting current path to '{dir_path}' for {user}")
                user.current_path = dir_path 

    #Dispaying Error msg incase of incorrect use of command line
    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'cd <directoryPath>'")


def showMap(user):

    #global current_path
    
    current_dict = getDictFromPath(user.current_path)
    print("===================START OF MAP======================")
    prettyPrint(current_dict, 1)
    print("===================END OF MAP========================")


def move(command_full, user):

    try:
        src_file_path  = command_full.split()[1]
        src_file_path = getAbsPathfromRelPath(src_file_path, user)
        src_filename   = src_file_path.split("/")[-1]

        trgt_file_path = command_full.split()[2]
        trgt_file_path = getAbsPathfromRelPath(trgt_file_path, user)
        trgt_filename  = trgt_file_path.split("/")[-1]

        #print(src_file_path, trgt_file_path)
        #print(src_filename, trgt_filename)
        src_hierarchy  = checkHierarchy(src_file_path.split("/"))
        trgt_hierarchy = checkHierarchy(trgt_file_path.split("/"))

        #Checking if both files exist
        if type(src_hierarchy) == str:
            print(f"\nERROR: Source File '{src_hierarchy}'.txt could not be found")
            return
        if type(trgt_hierarchy) == str:
            print(f"\nERROR: Source File '{trgt_hierarchy}'.txt could not be found")
            return
        
        #Reading the data from the Source File
        src_file_obj = CustomFile(src_filename, src_hierarchy, "r")
        src_data     = src_file_obj.read()

        #Writing the data from the Source File
        trgt_file_obj = CustomFile(trgt_filename, trgt_hierarchy, "w") ###Either w or a
        trgt_file_obj.write(src_data)

    except IndexError as ie:
        print("\nERROR: No Directory name or path specified, usage: 'cd <directoryPath>'")    


######################    Functions that operate on/modify File Data    ######################

def Open(command_full, user):
    
    #global current_file
    #if current_file:
    #    print(f"ERROR: A file {current_file.name}.txt is already opened, Please close it using the 'close' command before opening another")
    #    return

    try:
        file_path      = command_full.split()[1]
        file_mode      = command_full.split()[2]

        if file_mode not in ["r", "m", "t", "a", "w"]:
            print(f"ERROR: Invalid mode, Please chose a mode from: 'r', 't', 'a', 'w', 'm'")
            return

        file_path   = getAbsPathfromRelPath(file_path, user)
        
        file_name   = file_path.split("/")[-1]

        #hierarchy is the required file json object
        hierarchy   = checkHierarchy(file_path.split("/"))

        if type(hierarchy) == str:
            print(f"File '{file_path}'.txt does not exist ({user})")

        else:

            if hierarchy["type"] != "file":
                print(f"'{file_path}' is not a file ({user})")

            else:
                file = CustomFile(file_name, hierarchy, file_mode)
                user.current_files.append(file)
                #print("OPEN:", user.getCurrentFileNames())
                print(f"'{file_path}.txt' succesfully Opened in '{file_mode}' mode for {user}")   
               

    except IndexError as ie:
        print("\nERROR: Invalid use of open command, usage: 'open <filename> <mode>'")


def close(command_full, user):

    """
    This is the function that is called for the 'Close' command.
    It sets the current_file global variable to None if it is not None

    @param command_full: The full command form the command line
    """

    #global current_file

    #Check if user has no files opened
    if len(user.current_files) == 0:
        print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'close' command")
        return

    try:
        file_to_close_name = command_full.split()[1]

        #Checking if the file is opened for the current user
        #user_opened_file_names = user.getCurrentFileNames()

        #if file_to_close not in user_opened_file_names:
        #    print(f"ERROR: No file {file_to_close}.txt opened for {user}")
        #    return
    
        #Closing the file for  user
        
        for file in user.current_files:
            if file.name == file_to_close_name:
                print(f"{file_to_close_name}.txt succesfully Closed for {user}")
                user.current_files.remove(file)
                #print("CLOSE:", user.getCurrentFileNames())
                break
        else:
            print(f"ERROR: No file {file_to_close_name}.txt opened for {user}")

    #current_file = None

    except IndexError as ie:
        print("\nERROR: Invalid use of close command, usage: 'close <filename>'")


def read(command_full, user):

    #global current_file

    if len(user.current_files) == 0:
        print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'read' command")
        return

    try:
        file_to_read_name = command_full.split()[1]

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_read_name:
                read_data = file.read()
                break
        else:
            print(f"ERROR: No file {file_to_read_name}.txt opened for {user}")
            return            

        
        if read_data:
            print(f"Contents of {file_to_read_name}.txt:")
            print(read_data)

    except IndexError as ie:
        print("ERROR: Invalid use of read command. Usage read <filename>")


def readFrom(command_full, user):

    #global current_file

    try:

        file_to_read_name = command_full.split()[1]
        start_index       = int(command_full.split()[2])
        size              = int(command_full.split()[3])

        if len(user.current_files) == 0:
            print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'readfrom' command")
            return

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_read_name:
                read_data = file.readFrom(data, start_index, size)
                break
        else:
            print(f"ERROR: No file {file_to_read_name}.txt opened for {user}")
            return        

        if read_data:
            print(f"Contents of {file_to_read_name}.txt:")
            print(read_data)

    except IndexError as e:
        print("\nERROR: Invalid use of ReadFrom command, usage: 'readfrom <filename> <index> <size>'")



def append(command_full, user):

    try:

        file_to_append_name = command_full.split()[1]
        text_to_append      = "This is the text to append"

        if len(user.current_files) == 0:
            print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'append' command")
            return

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_append_name:
                #text_to_append = input("\nEnter text to append : ")
                # append text to file
                file.append(text_to_append, data)
                break

        else:
            print(f"ERROR: No file {file_to_append_name}.txt opened for {user}")
            return 

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)
        

    except IndexError as ie:
        print("\nERROR: Invalid use of append command, usage: 'append <filename> <text>'")
            
   


def truncate(command_full, user):

    try:

        file_to_truncate_name = command_full.split()[1]
        size = int(command_full.split()[2])

        if len(user.current_files) == 0:
            print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'truncate' command")
            return

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_truncate_name:
                file.truncate(data, size)
                break

        else:
            print(f"ERROR: No file {file_to_truncate_name}.txt opened for {user}")
            return 

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of aruncate command, usage: 'truncate <filename> <size>'")



def write(command_full, user):

    try:

        file_to_write = command_full.split()[1]
        text = "This is the text of write command"

        if len(user.current_files) == 0:
            print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'write' command")
            return

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_write:
                file.write(text)
                break

        else:
            print(f"ERROR: No file {file_to_write}.txt opened for {user}")
            return 

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of write command, usage: 'write <filename> <text>'")


def writeAt(command_full, user):

    try:

        file_to_write_at_name = command_full.split()[1]
        write_at_index        = command_full.split()[2]
        text                  = "This is the text to write at command"

        if len(user.current_files) == 0:
            print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'writeat' command")
            return

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_write_at_name:
                file.writeAt(data, text, write_at_index)
                break

        else:
            print(f"ERROR: No file {file_to_write_at_name}.txt opened for {user}")
            return 

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of writeat command, usage: 'writeat <filename> <index>'")



def move_within_file(command_full, user):    

    try:

        file_to_move_text_name = command_full.split()[1]
        index_to_move_from     = int(command_full.split()[2])
        index_to_move_to       = int(command_full.split()[3])
        size_to_move           = int(command_full.split()[4])

        if len(user.current_files) == 0:
            print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'move' command")
            return

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_move_text_name:
                file.move(index_to_move_from, index_to_move_to, size_to_move)
                break

        else:
            print(f"ERROR: No file {file_to_move_text_name}.txt opened for {user}")
            return 

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

    except IndexError as ie:
        print("\nERROR: Invalid use of move command, usage: 'move <filename> <fromIndex> <toIndex> <size>'")


######################    Utility Functions    ###############################################


def help():
    print("mkdir:"    + "\t\t" + "Used to create a directory. Usage: mkdir <directoryPath>\n"                                              + 
          "cd:"       + "\t\t" + "Used to change the  current directory. Usage: cd <directoryPath>\n"                                      +
          "create:"   + "\t\t" + "Used to create a file. Usage: create <fileName>\n"                                              +
          "delete:"   + "\t\t" + "Used to delete a file. Usage: delete <filename>\n"                                              +
          "showmap:"  + "\t"   + "Used to print the map of directories from current directory. Usage: showmap\n"                           +
          "move:"     + "\t\t" + "Used to copy content of a file to another. Usage: move <srcfilenmae> <trgtfilename>\n" +
          "open:"     + "\t\t" + "Used to open a file to perform operations. Usage: open <filename> <mode>\n"                     +
          "close:"    + "\t\t" + "Used to close an opened file. Usage: close <filename>\n"                                                           +
          "read:"     + "\t\t" + "Used to read data from an opened file. Usage: read <filename>\n"                                                    +
          "readfrom:" + "\t"   + "Used to read data from an opened file at given index. Usage: readfrom <filename> <index> <size>\n"                  +
          "truncate:" + "\t"   + "Used to delete data from an opened file onwards from a given index. Usage: truncate <filename> <size>\n"            +
          "append:"   + "\t\t" + "Used to appened data to an opened file. Usage: appened <filename>\n"                                                +
          "write:"    + "\t\t" + "Used to write to an opened file. Usage: write <filename>\n"                                                         +
          "writeat:"  + "\t"   + "Used to write to an opened file at given index. Usage: writeat <filename> <index>\n"                                +
          "movetext:" + "\t"   + "Used to move text within a file. Usage: movetext <filename> <from> <to> <size>"                                   
         )


def checkHierarchy(path):

    """
    A Function tat checks the validity of a path in the file structure
    If the argument 'path' is valid, the function returns a dictionary Object of the file/dir,
    else returns a String that specifies the invalid path

    @param path: a list all the directoires in the hierarchy
    """

    dir_str  = ""
    dir_dict = getDictFromPath(dir_str)
    
    for idx, dir_name in enumerate(path):
        
        if path[idx] in dir_dict.keys():
            
            if dir_str == "":
                dir_str +=  path[idx]
            else:
                dir_str += "/" + path[idx]
            
            dir_dict = getDictFromPath(dir_str)
            
        else:
            #Returning invalid path string
            return dir_str + "/" + path[idx]

    #Returning Directory dictionary object
    return dir_dict

def getDictFromPath(dir_path):

    """   
    A fucntion that returns dictionary object of directory

    @param dir_path: The path of the directory
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

    @param d:      A dict object to pretty print
    @param indent: The indent from which to start printing, defaults to 0
    """

    for key, value in d.items():

        if key not in ["type", "extension", "data", "page"]:
            
            if isinstance(value, dict):
                if value["type"] == "file":
                    print('  ' * indent + str(key) + ": " + str(value["type"]) + " (" + str(getSizeOfFile(value)) + " bytes)")                    
                else:
                    print('  ' * indent + str(key) + ": " + str(value["type"]))

                prettyPrint(value, indent+1)
            else:
                print('  ' * (indent+1) + str(value))

def getAbsPathfromRelPath(rel_path, user):

    """
    A function that takes in a relative path 
    and returns the absolute path i.e from the root

    @param rel_path: The path relative to the current path
    """

    #global current_path

    if user.current_path:
        return user.current_path + "/" + rel_path
        
    return rel_path

def getParent(path):

    """
    A Function that returns the parent directory's path of a given directory/file.
    Returns ROOT_PATH is path is ROOT_PATH, else returns the parent.

    @param path: A String of the path of directory or file 
    """

    if path == ROOT_PATH:
        return ROOT_PATH

    path_list = path.split("/")[:-1]

    if len(path_list):
        print("/".join(path_list))
        return "/".join(path_list)

    return ROOT_PATH


def getSizeOfFile(file_dict):

    total_size = 0 
    for chuck_num, chunk_dict in file_dict["data"].items():
        total_size += int(chunk_dict["length"])

    return total_size