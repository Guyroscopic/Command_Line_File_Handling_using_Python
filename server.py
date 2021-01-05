import socket
from rpc_utils import *


threads = []
port    = 95
ip      = "127.0.0.1" #socket.gethostname()
addr    = ip, port
server  = socket.socket()
print("Socket successfully created")

server.bind(addr)
print(f"Socket Binded to {port}")

server.listen()
print("Server is listening")

while True:

	client, client_addr = server.accept()
	#print("here")
	print(f"Got connection from {client_addr}")

	threads.append(threading.Thread(target=thread_routine, args=(client,)))
	threads[-1].start()