import numpy as np 
import socket
from _thread import *
from useraction import logout, change_password, check_user, game_handler, setup_info
from functionServer import Login, parseFirstRequest, Register, checkName, encryptRecv
import csv

def login(client, addr, onliner, listAccount, listSocks, check, gameStart):
	# handle login
	# data = client.recv(2048)
	user = encryptRecv(client, addr)
	temp=user.split()
	index, username, password = Login(client, temp[1], temp[2], listAccount)
	if index == -1:
		return
	onliner.append([client, temp[1], addr])
	print(str(addr[0]) + ':' + str(addr[1]), 'User ' + username + ' logged in')
	# receive command
	client.recv(2048)
	while True:
		client.send(b'input')
		data = client.recv(2048)
		response = data.decode('utf-8')
		print(str(addr[0]) + ':' + str(addr[1]), response)
		# Handle command from client
		if response=='logout':
			logout(client, addr, onliner, listSocks)
			return
		elif response == 'change_password':
			change_password(client, addr, password, index, listAccount)
		elif response == 'check_user':
			check_user(client, addr, listAccount, onliner)
		elif response == 'setup_info':
			setup_info(client, addr, listAccount, index)
		elif response == 'start_game':
			game_handler(client, addr, listSocks, onliner, check, username, gameStart)
			if check == True:
				break
		elif response == 'join':
			while True:
				f = open("check.txt", "r")
				if str(f.read()) == 'F':
					break
		elif response == 'end_game':
			client.send(b' input ')
			pass
	return True

def register(client, addr, listAccount):
	# data = client.recv(2048)
	user = encryptRecv(client, addr)
	temp=user.split()
	Register(client, temp[1], temp[2], listAccount)