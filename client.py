from socket import socket
from threading import Thread


client_alive = True
client_socket = None


# TODO: Kill server listener thread when command sender thread dies


def listen_to_server():
	global client_socket

	while 1:
		try:
			data = client_socket.recv(1024).decode()

			print('SERVER MESSAGE: ' + str(data))

		except ConnectionResetError:
			print("\nConnection lost.")
			break


def command_sender():
	global client_alive

	client_alive = True
	while client_alive:
		cmd = input('> ')
		process_command(*cmd.split())



def process_command(*args):
	global client_alive
	global client_socket

	if not args: return
	command = args[0].lower()

	if command == 'connect':
		addr, port = args[1].split(':')
		port = int(port)

		client_socket.connect(( addr, port ))
		server_listener = Thread(target=listen_to_server)
		server_listener.start()
		return

	if command == 'exit':
		client_alive = False
		return

	if client_socket:
		client_socket.send(' '.join(args).encode())
	else:
		print("Not connected to a socket.")


if __name__ == '__main__':
	client_socket = socket()

	command_sender_thread = Thread(target=command_sender)
	command_sender_thread.start()

	command_sender_thread.join()
