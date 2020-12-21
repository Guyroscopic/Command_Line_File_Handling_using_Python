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

def isCritical(command_full):

    """
    A function that checks if a command is critical. If the command is critical it returns True otherwise
    returns False

    @param command_full: A string of user entered command
    """

    command_func = command_full.split()[0]    
    
    #list of critical commands
    critical_commands = ["showmap", "create", "delete", "mkdir", "move", "write", "truncate", "append", "writeat", "movetext", "read", "readfrom"]

    if command_func in critical_commands:
        return True
    
    return False


def isRead(command_full):

    """
    A funtion that checks if a command is read or readfrom, returns True if it is otherwise retuns False

    @param command_full: A string of user entered command
    """

    command_func = command_full.split()[0]

    if command_func in ["read", "readfrom"]:
        return True

    return False

def isWrite(command_full):

    """
    A funtion that checks if a command is one of "write", "truncate", "append", "writeat", "movetext",
    returns True if it is otherwise retuns False

    @param command_full: A string of user entered command
    """

    command_func = command_full.split()[0]

    if command_func in ["write", "truncate", "append", "writeat", "movetext"]:
        return True

    return False


def getThreadCommandfromId(id):

    """
    This function opens command file of a thread reads
    commands for that specific thread and returns 
    the commands list.

    @param id: ID of the particular thread
    """

    #unique command file name assosciated with each thread
    thread_command_file = "Thread" + str(id) + "Commands.txt"
    
    with open(thread_command_file) as f:
        user_commands = f.readlines()
    
    return user_commands