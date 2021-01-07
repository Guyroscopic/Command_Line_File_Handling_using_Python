import socket             
  
# Create a socket object  
server = socket.socket()       
port   = 95

# connect to the server 
server.connect(('127.0.0.1', port))  


# the commands which require additional text input from client
input_commands = ["write", "append", "writeat"]

welcome_msg = server.recv(1024).decode()
print (welcome_msg)

#Prompting the user to get credentials and sending them to server
user_id 	  = input("Enter Your User ID: ")
user_password = input("Enter Your Password: ")

server.send(user_id.encode())
server.send(user_password.encode())

# server returns user instance upon successful authentication and proceeds
# else returns an error string and terminates the connection
response = server.recv(1024).decode()
if(response == "exit"):
	print("Invalid Credentials!\n Exiting..")
	server.close()

else:
	print(response)

	command_full_input_prompt = "not empty"
	while command_full_input_prompt:	

		command_full_input_prompt = server.recv(1024).decode()	
		command_full    		  = input(command_full_input_prompt)

		server.send(command_full.encode())

		if command_full.split()[0] in input_commands:
			input_response = server.recv(1024).decode()
			text_input = input(input_response)
			server.send(text_input.encode())

		server_response = server.recv(1024).decode()
		print(server_response)

		if server_response == "exit":
			print("Quitting...")
			break
	#user_password = input("Enter Your Password: ")

	

# receive data from the server  
 
# close the connection  
server.close()  