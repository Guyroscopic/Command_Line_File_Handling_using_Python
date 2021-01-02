from thread_run_utils import *

def thread_routine(client):

	# send a thank you message to the client.  
	client.send("\n  *  Connected to remote FMS\n  *  Starting Custom CLI. NOTE: Type 'help' for more info\n".encode())

	user_id 	  = client.recv(1024).decode()
	user_password = client.recv(1024).decode()

	user = authenticate_user(user_id, user_password)
	if type(user) == str:
		client.send(user.encode())
		return

	client.send(f"Welcome {user.username}".encode())

	#while True:

		
		#print(msg)

		# Close the connection with the client  
	
	client.close()