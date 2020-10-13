from socket import socket
from threading import Thread

from stuf import stuf


class Dict(stuf):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@property
	def users(self):
		if not self: return []
		return [client.user for client in self.values()]



server_socket = None
clients = Dict(
	# thread: Thread,
	# user: None
)


def bind_socket(address: tuple, *args, **kwargs) -> None:
	"""Creates and binds the global server socket to the given address"""
	global server_socket

	sock = socket(*args, **kwargs)
	sock.bind(address)
	
	server_socket = sock


def accept_connections() -> None:
	"""Accepts incoming connection requests to the server socket"""
	global server_socket
	global client_sockets

	while True:
		client_socket, address_info = server_socket.accept()
		thread = Thread(target=process_client_events, args=(client_socket, ))

		clients[client_socket] = stuf(
			thread = thread,
			user = None
		)

		thread.start()


def process_client_events(client_socket):
	global server_socket
	global client_sockets

	while 1:
		try:
			data = client_socket.recv(1024).decode()

			process_command(client_socket, *data.split())


		except ConnectionResetError:
			print('Connection lost.')
			break


def process_command(sock, *args):
	if not args: return
	command = args[0].lower()

	if command == 'msg':
		print('Message command | Content: ' + ' '.join(list(args)[1:]))
		return

	if command == 'login':
		sock.send('loginok'.encode())
		return


	
if __name__ == '__main__':
	addr, port = input("Enter connection address: ").split(':')
	port = int(port)

	bind_socket(( addr, port ))
	server_socket.listen(5)
	connection_thread = Thread(target=accept_connections)
	connection_thread.start()