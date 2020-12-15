import json
from user import *
from custom_os_utils import *

with open("users.json", "r") as f:
        users_data = json.load(f)



def authenticate_user(id, password):

        try:
                user = users_data[str(id)]

                if user["password"] == password:
                        return User(id, user["username"], password, [], "")
                else:
                        print(f"ERROR: Wrong Password for ID {id}")
                        return

        except KeyError as ke:
                print(f"ERROR: No user with ID '{id}'")
                return



def getThreadCommandfromId(id):

        """
        This function opens command file of a thread reads
        commands for that specific thread and returns 
        the commands list. If no command file is found,
        returns None

        @param id: ID of the particular thread
        """

        #unique command file name assosciated with each thread
        command_file = "Thread" + str(id+1) + "Commands.txt"

        try:
                with open(command_file) as f:
                        user_commands = f.readlines()

                #check if there are no commands in command file
                if not user_commands:
                        return
                else:
                        return user_commands 

        except FileNotFoundError as fnf:
                print("FILE ERROR: Command File does not exist")
                return


def getFunctionNamefromCommand(user_command, user):
        
        command_func = user_command.split()[0]

        if command_func == "create": 
                create(user_command)
                        
        elif command_func == "mkdir":
                mkDir(user_command)                       
                
        elif command_func == "delete":
                delete(user_command)

        elif command_func == "cd":                       
                user.current_path = chDir(user_command, user)

        elif command_func == "open":
                Open(user_command)

        elif command_func == "close":
                close(user_command)

        elif command_func == "read":
                read()

        elif command_func == "readfrom":
                readFrom(user_command)

        elif command_func == "append":
                append()

        elif command_func == "write":
                write()

        elif command_func == "WriteAt":
                writeAt(user_command)
                
        elif command_func == "truncate":
                truncate(user_command)

        elif command_func == "movetext":
                move_within_file(user_command)
                
        elif command_func == "showmap":
                showMap()

        elif command_func == "move":
                move(user_command)

        elif command_func == "help":
                help()     

        elif command_func == "exit":
                print("\nQuitting")


