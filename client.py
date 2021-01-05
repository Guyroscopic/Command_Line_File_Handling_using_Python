import socket             
  
# Create a socket object  
server = socket.socket()       
port   = 95                
 
server.connect(('127.0.0.1', port))  

welcome_msg = server.recv(1024).decode()
print (welcome_msg)

#Promting the user to get credentials and sending them to server
user_id 	  = input("Enter Your User ID: ")
user_password = input("Enter Your Password: ")

server.send(user_id.encode())
server.send(user_password.encode())

print(server.recv(1024).decode())

command_full_input_prompt = "not empty"
while command_full_input_prompt:	

	command_full_input_prompt = server.recv(1024).decode()	
	command_full    		  = input(command_full_input_prompt)
	server.send(command_full.encode())

	server_response = server.recv(1024).decode()
	print(server_response)

	#user_password = input("Enter Your Password: ")

	

# receive data from the server  
 
# close the connection  
server.close()  