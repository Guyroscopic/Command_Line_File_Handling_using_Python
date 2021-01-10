import socket
import getpass


# Create a socket object  
server = socket.socket()       
port   = 95

#prompting user to input ip of server
ip = input("Enter IP address where you want to connect: ")
addr = ip, port

# connect to the server 
server.connect(addr)

#The commands which require additional text input from client
additional_input_commands = ["write", "append", "writeat"]

welcome_msg = server.recv(1024).decode()
print (welcome_msg)

#Prompting the user to get credentials and sending them to server
user_id 	  = input("Enter Your User ID: ")
user_password = getpass.getpass('Enter Your Password: ')

server.send(user_id.encode())
server.send(user_password.encode())

#Closing the connection in case of invalid credentials
response = server.recv(1024).decode()
if(response == "invalid_creds"):
	print("Invalid Credentials!\nExiting...")
	server.close()

else:
	print(response)

	command_full_input_prompt = "not empty"
	while command_full_input_prompt:	

		command_full_input_prompt = server.recv(1024).decode()	
		command_full    		  = input(command_full_input_prompt)

		server.send(command_full.encode())

		if command_full.split()[0] in additional_input_commands:
			input_response = server.recv(1024).decode()
			text_input = input(input_response)
			server.send(text_input.encode())

		server_response = server.recv(1024).decode()		

		if server_response == "exit":
			print("Quitting...")
			command_full_input_prompt = ""
			#break
		else:
			print(server_response)	

#Closing the connection  
server.close()  