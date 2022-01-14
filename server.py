import numpy as np 
import socket
from _thread import *
from router import login, register
from functionServer import readAll, parseFirstRequest
# Set up server
server = socket.socket()
# host = '192.168.1.5'
print('Enter host IP: ')
host = input()
print('Enter host port')
# host = '192.168.1.5'
port = int(input())
# port = 1234
onliner = []
server.settimeout(0.5)

# Load accout list from file to array
listAccount = []
listAccount = readAll('Account.txt')

try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))

print('Server is waiting for a connection...')
server.listen(5)
listSocks = []

gameStart = False
f = open("check.txt", "w")
f.write("False")
f.close()

def threaded_client(client, addr):
	try:
		check = True

		while check:
			respone = ''
			if check:
				data = client.recv(2048)
				response = data.decode('utf-8')
			if response == 'login':
				print('An user is logging in...')
				check = False
				login(client, addr, onliner, listAccount, listSocks, check, gameStart)
				check = True
				# client.send(b' input')
			elif response == 'register':
				register(client, addr, listAccount)
				client.send(b'input')
			elif response == 'end':
				print('Closing connection with ' + str(addr[0]) + ':' + str(addr[1]))
				listSocks.remove(client)
				break
			elif response == 'join':
				while True:
					f = open("check.txt", "r")
					if str(f.read()) == 'F':
						break

	except KeyboardInterrupt:
		listSocks.remove(client)
		client.close()

while True:
	try:
		client, addr = server.accept()
		print('Connected to client ' + str(addr[0]) + ':' + str(addr[1]))
		listSocks.append(client)
		start_new_thread(threaded_client, (client, addr))
	except socket.timeout:
		a = 0
	except KeyboardInterrupt():
		print('Server is closing...')
		break
server.close()