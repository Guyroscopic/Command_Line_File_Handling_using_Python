import socket
from rpc_utils import *


port    = 95
host    = socket.gethostname()
ip      = socket.gethostbyname(host)

addr    = ip, port
print(f"Hosting at '{ip}:{port}'")
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

	threads[client_addr] = threading.Thread(target=thread_routine, args=(client, client_addr))
	threads[client_addr].start()


server.close()