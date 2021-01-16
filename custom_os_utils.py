from FileClass import *
from user import *


current_path = ROOT_PATH
current_file = None
PAGE_SIZE    = 1024

commands     = ["create", "delete", "mkdir", "move", "movetext", "cd", "open", "close", "showmap", "showfilemap", "read", "readfrom", "append", "write", "writeat", "truncate", "exit", "help"]

opened_files = {}

######################      Function that operate on/modify File structure    ################

def create(command_full, user):
        server_response = ""
        try:
            file_path      = command_full.split()[1]
            file_path      = getAbsPathfromRelPath(file_path, user)
            file_to_create = file_path.split("/")[-1]
            file_extension = file_to_create.split(".")[-1]

            if not file_extension:
                server_response = "ERROR: No file extension specified"
                return server_response


            file_extension = file_to_create.split(".")[-1]
            file_to_create = "".join(file_to_create.split(".")[:-1])
            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)

            if type(hierarchy) == str:
                server_response = f"\nERROR: Directory '{hierarchy}' could not be found"
                return server_response

            else:
                try:
                    #Checking if the File already exists
                    hierarchy[file_to_create]
                    #print(f"ERROR: File '{file_path}' already exists")
                    server_response = f"ERROR: File '{file_path}' already exists"
                    return server_response

                except KeyError as ke:
                    hierarchy[file_to_create] = {
                                                   "type"     : "file",
                                                    "extension": "." + file_extension,
                                                    "data"     : {}
                                                }

                    with open("structure.json", "w") as f:
                        json.dump(structure, f)

                    #print(f"File '{file_path}' created by {user}")
                    server_response = f"File '{file_path}' created by {user}"

        except IndexError as ie:
                #print("\nERROR: No File name or path specified, usage: 'create <fileName>'")
                server_response = "\nERROR: No File name or path specified, usage: 'create <fileName>'"
                return server_response

        return server_response


def delete(command_full, user):

        server_response = ""
        try:
            file_path      = command_full.split()[1]
            file_path      = getAbsPathfromRelPath(file_path, user)

            file_to_delete = file_path.split("/")[-1]

            if not file_to_delete.split("."):
                #print("ERROR: No file extension specified")
                server_response = "ERROR: No file extension specified"
                return server_response

            file_extension = file_to_delete.split(".")[-1]
            file_to_delete = "".join(file_to_delete.split(".")[:-1])

            parent_dir     = file_path.split("/")[:-1]
            hierarchy      = checkHierarchy(parent_dir)


            #print("PATH: ", file_path)
            if type(hierarchy) == str:
                #print(f"\nERROR: Directory '{hierarchy}' could not be found")
                server_response = f"\nERROR: Directory '{hierarchy}' could not be found"
                return server_response

            else:
                try:
                    #Checking if the File exists
                    hierarchy[file_to_delete]
                    print(hierarchy[file_to_delete]["type"])

                    if hierarchy[file_to_delete]["type"] != "file":
                        #print(f"'{file_path}' is not a file")
                        server_response = f"'{file_path}' is not a file"
                        return server_response

                    else:
                        file_extension = hierarchy[file_to_delete]["type"]
                        file_to_delete_obj = CustomFile( file_to_delete, file_extension, hierarchy[file_to_delete], 't')
                        print(file_to_delete_obj)
                        # deleting the file content 
                        truncate_response = file_to_delete_obj.truncate(data, 0)
                       
                        hierarchy.pop(file_to_delete)

                        with open("structure.json", "w") as f:
                            json.dump(structure, f)

                        #print(f"File '{file_path}' deleted by {user}")
                        server_response = f"File '{file_path}' deleted"
                        return server_response

                except KeyError as ke:
                    #If the file does not Exist
                    #print(f"File {file_path} does not exist")
                    server_response = f"File {file_path} does not exist"
                    #server_response = str(e)
                    return server_response

        except IndexError as ie:
                #print("\nERROR: No Directory name or path specified, usage: 'delete <fileName>'")
                server_response = "\nERROR: No Directory name or path specified, usage: 'delete <fileName>'"
                return server_response

def mkDir(command_full, user):

    server_response = ""   
    try:
        dir_path = command_full.split()[1]
        dir_path = getAbsPathfromRelPath(dir_path, user)
        
        dir_to_create = dir_path.split("/")[-1]
        parent_dir = dir_path.split("/")[:-1]
        
        hierarchy = checkHierarchy(parent_dir)
       
        if type(hierarchy) == str:
            #print(f"\nERROR: Directory '{hierarchy}' could not be found")
            server_response =  f"\nERROR: Directory '{hierarchy}' could not be found"
            return server_response
        else:
            #MAKE THE DIR IN STRUCTURE LOGIC
            try:
                #Checking if the Directorry already exists
                hierarchy[dir_to_create]
                #print(f"ERROR: Directory '{dir_path}' already exists")
                server_response = f"ERROR: Directory '{dir_path}' already exists"
                return server_response
            except KeyError as ke:

                #Adding the directory to Parent Directory
                hierarchy[dir_to_create] = {"type": "dir"}

                #print(structure)
                with open("structure.json", "w") as f:                  
                    json.dump(structure, f)

                #print(f"Directory '{dir_path}' Created")
                server_response = f"Directory '{dir_path}' Created"
                return server_response

    except IndexError as ie:
        #print("\nERROR: No Directory name or path specified, usage: 'mkdir <directoryPath>'")
        server_response += "\nERROR: No Directory name or path specified, usage: 'mkdir <directoryPath>'"
        return server_response

def chDir(command_full, user):

    global current_path
    server_response = ""
        
    try:
        dir_path = command_full.split()[1]

        if dir_path == "..":
            dir_path = getParent(user.current_path)
        else:
            dir_path = getAbsPathfromRelPath(dir_path, user)

        
        #Logic For moving upward in the File Structure to root
        if dir_path == ROOT_PATH:            
            if user.current_path == ROOT_PATH:
                #print(f"Already in root")
                server_response = f"Already in root"
                return server_response
            else:

                user.current_path = ROOT_PATH
                server_response = f"Setting current path to root"
                return server_response
        #Logic For moving upward or downward in the FIle Structure according to the user input
        hierarchy = checkHierarchy(dir_path.split("/"))
        
        if type(hierarchy) == str:
            server_response = f"\nERROR: Directory '{hierarchy}' could not be found"
            return server_response
            
        else:

            if hierarchy["type"] != "dir":
                server_response = f"ERROR: {dir_path} is not a directory"
                return server_response

            else:
                server_response = f"Setting current path to '{dir_path}' for {user}"
                user.current_path = dir_path 
                return server_response
    #Dispaying Error msg incase of incorrect use of command line
    except IndexError as ie:
        server_response = "\nERROR: No Directory name or path specified, usage: 'cd <directoryPath>'"
        return server_response


def showMap(user):

    server_response = ""
    #global current_path
    
    current_dict = getDictFromPath(user.current_path)
    server_response += "\n===================START OF MAP======================"
    server_response += prettyPrint(current_dict, 1)
    server_response += "\n===================END OF MAP========================"

    return server_response


def showMemoryMap(command_full, user):

    server_response = ""
    try:
        file_path   = command_full.split()[1]

        file_path   = getAbsPathfromRelPath(file_path, user)        
        file_name   = file_path.split("/")[-1]

        #Checking is user provided an extension for the file
        if not file_name.split("."):
                #print("ERROR: No file extension specified for the source file")
                server_response = "ERROR: No file extension specified for the source file"
                return server_response

        file_extension = "." + file_name.split(".")[-1]

        #removing the extension from src_filename and src_file_path
        file_name  = "".join(file_name.split(".")[:-1])
        file_path = "".join(file_path.split(".")[:-1])

        #hierarchy is the required file json object
        hierarchy   = checkHierarchy(file_path.split("/"))

        if type(hierarchy) == str:
            #print(f"File '{file_path}{file_extension}' does not exist ({user})")
            server_response = f"File '{file_path}{file_extension}' does not exist ({user})"
            return server_response

        else:

            #total number of chunks of a file
            number_of_chunks = len(hierarchy['data'])

            #print("===================START OF MEMORY MAP======================")
            #print(f"File {file_name}.txt has {number_of_chunks} chunks")
            #print("Here is the memory location of all the chunks :")

            server_response += "\n===================START OF MEMORY MAP======================"
            server_response += f"\nFile {file_name}.txt has {number_of_chunks} chunks"
            server_response += "\nHere is the memory location of all the chunks :"
            #printing memory location of file chunk by chunk
            for chunk_data in hierarchy['data']:

                chunk_number = hierarchy['data'][chunk_data]

                page = int(chunk_number['page'])

                start = int(chunk_number['start'])
                end   = start + int(chunk_number['length'])

                start_mem_location = start + page * PAGE_SIZE 
                end_mem_location   = end + page * PAGE_SIZE 

                #print(f"Chunk Number {chunk_data}--> {start_mem_location} - {end_mem_location}")
                server_response += f"\nChunk Number {chunk_data}--> {start_mem_location} - {end_mem_location}"
            #print("===================END OF MEMORY MAP========================")
            server_response += "\n===================END OF MEMORY MAP========================"
            return server_response

    except IndexError as ie:
        #print("\nERROR: No File name or path specified, usage: 'showfilemap <filePath>'")         
        server_response = "\nERROR: No File name or path specified, usage: 'showfilemap <filePath>'"
        return server_response

def move(command_full, user):

    server_response = ""
    try:
        #Getting the source file path and name
        src_file_path  = command_full.split()[1]
        src_file_path = getAbsPathfromRelPath(src_file_path, user)
        src_filename   = src_file_path.split("/")[-1]


        #Checking is user provided an extension for source file
        if not src_filename.split("."):
                #print("ERROR: No file extension specified for the source file")
                server_response = "ERROR: No file extension specified for the source file"
                return server_response

        src_file_extension = "." + src_filename.split(".")[-1]

        #removing the extension from src_filename and src_file_path
        src_filename  = "".join(src_filename.split(".")[:-1])
        src_file_path = "".join(src_file_path.split(".")[:-1])        

        #Getting the target file path and name
        trgt_file_path = command_full.split()[2]
        trgt_file_path = getAbsPathfromRelPath(trgt_file_path, user)
        trgt_filename  = trgt_file_path.split("/")[-1]

        #Checking is user provided an extension for target file
        if not trgt_filename.split("."):
                #print("ERROR: No file extension specified for the target file")
                server_response = "ERROR: No file extension specified for the target file"
                return server_response

        trgt_file_extension = "." + trgt_filename.split(".")[-1]        

        #removing the extension from trgt_filename and trgt_file_path
        trgt_filename  = "".join(trgt_filename.split(".")[:-1])
        trgt_file_path = "".join(trgt_file_path.split(".")[:-1])

        #print(src_file_path, trgt_file_path)
        #print(src_filename, trgt_filename)
        src_hierarchy  = checkHierarchy(src_file_path.split("/"))
        trgt_hierarchy = checkHierarchy(trgt_file_path.split("/"))

        #Checking if both files exist
        if type(src_hierarchy) == str:
            #print(f"\nERROR: Source File '{src_hierarchy}' could not be found")
            server_response = f"\nERROR: Source File '{src_hierarchy}' could not be found" 
            return server_response

        if type(trgt_hierarchy) == str:
            #print(f"\nERROR: Source File '{trgt_hierarchy}' could not be found")
            server_response = f"\nERROR: Source File '{trgt_hierarchy}' could not be found"
            return server_response
        
        #Reading the data from the Source File
        src_file_obj = CustomFile(src_filename, src_file_extension, src_hierarchy, "r")
        src_data     = src_file_obj.read()

        #Writing the data from the Source File
        trgt_file_obj = CustomFile(trgt_filename, trgt_file_extension, trgt_hierarchy, "w") ###Either w or a
        trgt_file_obj.write(src_data)

        ##WRITE TO THE STRUCTURE
        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

        server_response = f"Content of {src_filename}{src_file_extension}  copied to {trgt_filename}{trgt_file_extension}"
        return server_response

    except IndexError as ie:
        #print("\nERROR: No Directory name or path specified, usage: 'cd <directoryPath>'")    
        server_response = "\nERROR: No Directory name or path specified, usage: 'cd <directoryPath>'"
        return server_response

######################    Functions that operate on/modify File Data    ######################

def Open(command_full, user):
    
    #global current_file
    #if current_file:
    #    print(f"ERROR: A file {current_file.name}.txt is already opened, Please close it using the 'close' command before opening another")
    #    return
    server_response = ""
    try:
        file_path      = command_full.split()[1]
        file_mode      = command_full.split()[2]

        if file_mode not in ["r", "m", "t", "a", "w"]:
            #print(f"ERROR: Invalid mode, Please chose a mode from: 'r', 't', 'a', 'w', 'm'")
            server_response = f"ERROR: Invalid mode, Please chose a mode from: 'r', 't', 'a', 'w', 'm'"
            return server_response

        file_path   = getAbsPathfromRelPath(file_path, user)        
        file_name   = file_path.split("/")[-1]

        #Checking is user provided an extension for the file
        if not file_name.split("."):
                #print("ERROR: No file extension specified for the file")
                server_response = "ERROR: No file extension specified for the file"
                return server_response

        file_extension = "." + file_name.split(".")[-1]        

        #removing the extension from trgt_filename and trgt_file_path
        #file_name  = "".join(file_name.split(".")[:-1])
        file_path = "".join(file_path.split(".")[:-1])
        
        #hierarchy is the required file json object
        hierarchy   = checkHierarchy(file_path.split("/"))

        if type(hierarchy) == str:
            #print(f"File '{file_path}' does not exist ({user})")
            server_response = f"File '{file_name}{file_extension}' does not exist ({user})"
            return server_response
        else:

            if hierarchy["type"] != "file":
                #print(f"'{file_path}' is not a file ({user})")
                server_response = f"'{file_path}' is not a file ({user})"
                return server_response

            else:
                
                #Checking if user has already opened five files
                if(len(user.getCurrentFileNames()) == 5):
                    server_response = "ERROR! You already have 5 files opened, Please close a file before opening more"
                    return server_response

                #Checking if the requested file is already opened by 3 users
                try:
                    temp = opened_files[file_name]
                    if(len(list(opened_files[file_name].keys())) < 3):
                        opened_files[file_name][user.id] = file_mode
                    else:
                        server_response = f"ERROR! File '{file_name}' is already opened by 3 users, Please wait"
                        return server_response
                except KeyError as ke:
                    opened_files[file_name] = {user.id : file_mode}

                print("Global Array: ",opened_files)

                #Adding file to user's opened files
                file = CustomFile(file_name, file_extension, hierarchy, file_mode)
                user.current_files.append(file)
                #print(f"'{file_path}{file_extension}' succesfully Opened in '{file_mode}' mode for {user}")
                print(f"Files Opened by {user.username}: ", user.getCurrentFileNames())
                server_response = f"'{file_path}{file_extension}' succesfully Opened in '{file_mode}' mode for {user}"
                return server_response

    except IndexError as ie:
        #print("\nERROR: Invalid use of open command, usage: 'open <filename> <mode>'")
        server_response = "\nERROR: Invalid use of open command, usage: 'open <filename> <mode>'"
        return server_response

def close(command_full, user):

    """
    This is the function that is called for the 'Close' command.
    It sets the current_file global variable to None if it is not None

    @param command_full: The full command form the command line
    """

    server_response = ""

    #Check if user has no files opened
    if len(user.current_files) < 0:
        #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'close' command")
        server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'close' command"
        return server_response

    try:
        file_to_close_name = command_full.split()[1]

        #Checking if the file is opened for the current user
        #user_opened_file_names = user.getCurrentFileNames()
    
        #Closing the file for  user
        for file in user.current_files:
            if file.name == file_to_close_name:
                #print(f"{file_to_close_name} succesfully Closed for {user}")

                #Removing the file from the global opened files array
                opened_files[file_to_close_name].pop(user.id)
                print("Global Array: ", opened_files)

                #Removing the file from user's opened files
                user.current_files.remove(file)
                print(f"Files Opened by {user.username}: ", user.getCurrentFileNames())

                server_response = f"{file_to_close_name} succesfully Closed for {user}"
                return server_response
                #print("CLOSE:", user.getCurrentFileNames())
                break
        else:
            #print(f"ERROR: No file {file_to_close_name} opened for {user}")
            server_response = f"ERROR: No file {file_to_close_name} opened for {user}"
            return server_response
    #current_file = None

    except IndexError as ie:
        #print("\nERROR: Invalid use of close command, usage: 'close <filename>'")
        server_response = "\nERROR: Invalid use of close command, usage: 'close <filename>'"
        return server_response


def read(command_full, user):

    #global current_file
    server_response = ""
    
    if len(user.current_files) == 0:
        #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'read' command")
        server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'read' command"
        return server_response

    try:
        file_to_read_name = command_full.split()[1]

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_read_name:
                read_data = file.read()
                break
        else:
            #print(f"ERROR: No file {file_to_read_name} opened for {user}")
            server_response = f"ERROR: No file {file_to_read_name} opened for {user}"
            return server_response            
        
        if read_data:
            #print(f"Contents of {file_to_read_name}:")
            server_response = f"Contents of {file_to_read_name}:\n"
            server_response += read_data

        # if the file is empty
        else:
            server_response = f"!!!File {file_to_read_name} is empty!!!\n Try adding some text to it"

        return server_response

    except IndexError as ie:
        #print("ERROR: Invalid use of read command. Usage read <filename>")
        server_response = "ERROR: Invalid use of read command. Usage read <filename>"
        return server_response

def readFrom(command_full, user):

    #global current_file
    server_response = ""

    try:

        file_to_read_name = command_full.split()[1]
        start_index       = int(command_full.split()[2])
        size              = int(command_full.split()[3])

        if len(user.current_files) == 0:
            #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'readfrom' command")
            server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'readfrom' command"
            return server_response

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_read_name:
                read_data = file.readFrom(data, start_index, size)
                break
        else:
            #print(f"ERROR: No file {file_to_read_name} opened for {user}")
            server_response = f"ERROR: No file {file_to_read_name} opened for {user}"
            return server_response       

        if read_data:
            #print(f"Contents of {file_to_read_name}:")
            #print(read_data)
            server_response = f"Contents of {file_to_read_name}:\n"
            server_response += read_data
            return server_response

    except IndexError as e:
        #print("\nERROR: Invalid use of ReadFrom command, usage: 'readfrom <filename> <index> <size>'")
        server_response = "\nERROR: Invalid use of ReadFrom command, usage: 'readfrom <filename> <index> <size>'"
        return server_response


def append(command_full, user, text_to_append):

    server_response = ""
    try:

        file_to_append_name = command_full.split()[1]

        if len(user.current_files) == 0:
            #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'append' command")
            server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'append' command"
            return server_response

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_append_name:
                #text_to_append = input("\nEnter text to append : ")
                # append text to file
                server_response = file.append(text_to_append, data)
                return server_response
                break

        else:
            #print(f"ERROR: No file {file_to_append_name} opened for {user}")
            server_response = f"ERROR: No file {file_to_append_name} opened for {user}"
            return server_response

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)
        

    except IndexError as ie:
        server_response = "\nERROR: Invalid use of append command, usage: 'append <filename> <text>'"
        return server_response
        #print("\nERROR: Invalid use of append command, usage: 'append <filename> <text>'")
            
   
def truncate(command_full, user):

    server_response = ""
    try:

        file_to_truncate_name = command_full.split()[1]
        size = int(command_full.split()[2])

        if len(user.current_files) == 0:
            #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'truncate' command")
            server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'truncate' command" 
            return server_response

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_truncate_name:
                server_response = file.truncate(data, size)
                break

        else:
            #print(f"ERROR: No file {file_to_truncate_name}.txt opened for {user}")
            server_response = f"ERROR: No file {file_to_truncate_name}.txt opened for {user}"
            return server_response

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

        return server_response

    except IndexError as ie:
        #print("\nERROR: Invalid use of aruncate command, usage: 'truncate <filename> <size>'")
        server_response = "\nERROR: Invalid use of aruncate command, usage: 'truncate <filename> <size>'"
        return server_response

def write(command_full, user, text):

    server_response = ""
    try:

        file_to_write = command_full.split()[1]
        #text = command_full.split()[2:] # PROMPT USER FOR TEXT TO WRITE

        if len(user.current_files) == 0:
            #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'write' command")
            server_response += f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'write' command"
            return server_response

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_write:
                server_response = file.write(text)
                break

        else:
            #print(f"ERROR: No file {file_to_write}.txt opened for {user}")
            server_response = f"ERROR: No file {file_to_write}.txt opened for {user}"
            return server_response

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

        return server_response

    except IndexError as ie:
        #print("\nERROR: Invalid use of write command, usage: 'write <filename> <text>'")
        server_response += "\nERROR: Invalid use of write command, usage: 'write <filename> <text>'"
        return server_response

def writeAt(command_full, user, text):

    server_response = ""
    try:

        file_to_write_at_name = command_full.split()[1]
        write_at_index        = command_full.split()[2]
        text                  = command_full.split()[3:]

        if len(user.current_files) == 0:
            #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'writeat' command")
            server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'writeat' command"
            return server_response

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_write_at_name:
                server_response = file.writeAt(data, text, write_at_index)
                break

        else:
            #print(f"ERROR: No file {file_to_write_at_name}.txt opened for {user}")
            server_response = f"ERROR: No file {file_to_write_at_name}.txt opened for {user}"
            return server_response

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

        return server_response

    except IndexError as ie:
        #print("\nERROR: Invalid use of writeat command, usage: 'writeat <filename> <index>'")
        server_response = "\nERROR: Invalid use of writeat command, usage: 'writeat <filename> <index>'"
        return server_response

def move_within_file(command_full, user):    

    server_response = ""
    try:

        file_to_move_text_name = command_full.split()[1]
        index_to_move_from     = int(command_full.split()[2])
        index_to_move_to       = int(command_full.split()[3])
        size_to_move           = int(command_full.split()[4])

        if len(user.current_files) == 0:
            #print(f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'move' command")
            server_response = f"ERROR: No file is opened, Please open a file using 'open <filename> <mode>' before using 'move' command"
            return server_response

        #Checking if the file is opened for the current user, if opened, reading it
        for file in user.current_files:
            if file.name == file_to_move_text_name:
                server_response = file.move(index_to_move_from, index_to_move_to, size_to_move)
                break

        else:
            #print(f"ERROR: No file {file_to_move_text_name}.txt opened for {user}")
            server_response = f"ERROR: No file {file_to_move_text_name}.txt opened for {user}"
            return server_response

        #Updating the File Structure and Data Storage in Non-Volatile memory
        with open("structure.json", "w") as f:
            json.dump(structure, f)

        return server_response

    except IndexError as ie:
        #print("\nERROR: Invalid use of move command, usage: 'move <filename> <fromIndex> <toIndex> <size>'")
        server_response = "\nERROR: Invalid use of move command, usage: 'move <filename> <fromIndex> <toIndex> <size>'"
        return server_response

######################    Utility Functions    ###############################################

def help():
    server_response = ""
    server_response ="mkdir:"     + "\t\t" + "Used to create a directory. Usage: mkdir <directoryPath>\n"                                              
    server_response +="cd:"       + "\t\t" + "Used to change the  current directory. Usage: cd <directoryPath>\n"                                     
    server_response +="create:"   + "\t\t" + "Used to create a file. Usage: create <fileName>\n"                                                      
    server_response +="delete:"   + "\t\t" + "Used to delete a file. Usage: delete <filename>\n"                                                     
    server_response +="showmap:"  + "\t"   + "Used to print the map of directories from current directory. Usage: showmap\n"                           
    server_response +="move:"     + "\t\t" + "Used to copy content of a file to another. Usage: move <srcfilenmae> <trgtfilename>\n"                   
    server_response +="open:"     + "\t\t" + "Used to open a file to perform operations. Usage: open <filename> <mode>\n"                              
    server_response +="close:"    + "\t\t" + "Used to close an opened file. Usage: close <filename>\n"                                                 
    server_response +="read:"     + "\t\t" + "Used to read data from an opened file. Usage: read <filename>\n"                                         
    server_response +="readfrom:" + "\t"   + "Used to read data from an opened file at given index. Usage: readfrom <filename> <index> <size>\n"       
    server_response +="truncate:" + "\t"   + "Used to delete data from an opened file onwards from a given index. Usage: truncate <filename> <size>\n" 
    server_response +="append:"   + "\t\t" + "Used to appened data to an opened file. Usage: appened <filename>\n"                                     
    server_response +="write:"    + "\t\t" + "Used to write to an opened file. Usage: write <filename>\n"                                              
    server_response +="writeat:"  + "\t"   + "Used to write to an opened file at given index. Usage: writeat <filename> <index>\n"                     
    server_response +="movetext:" + "\t"   + "Used to move text within a file. Usage: movetext <filename> <from> <to> <size>\n" 

    return server_response


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
    pretty_print_response = ""
    for key, value in d.items():

        if key not in ["type", "extension", "data", "page"]:
            
            if isinstance(value, dict):
                if value["type"] == "file":
                    #print('  ' * indent + str(key)  + str(value["extension"]) +": " + str(value["type"]) + " (" + str(getSizeOfFile(value)) + " bytes)")                    
                    pretty_print_response += '\n  ' * indent + str(key)  + str(value["extension"]) +": " + str(value["type"]) + " (" + str(getSizeOfFile(value)) + " bytes)"

                else:
                    #print('  ' * indent + str(key) + ": " + str(value["type"]))
                    pretty_print_response += '\n  ' * indent + str(key) + ": " + str(value["type"])
                prettyPrint(value, indent+1)
            else:
                #print('  ' * (indent+1) + str(value))
                pretty_print_response += '\n  ' * (indent+1) + str(value)

    return pretty_print_response

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