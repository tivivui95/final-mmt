import numpy as np 
import socket
from _thread import *
from os import error
from client_handle import client_handle
client = socket.socket()
from functionClient import Login, Register
from os import system, name
import time
from tqdm import tqdm
# UI Process Bar
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 25, fill = '█', printEnd = "\r"):
    total = len(iterable)
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    printProgressBar(0)
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    print()
system('cls')

for i in tqdm(range(100)):
    time.sleep(0.01)

system('cls')
print('| Welcome to BATTLE SHIP!\n| Enter IP server to connect\n| - Command format: connect [ip] port [port]')
inp_connect = input()
inp = inp_connect.split()

items = list(range(0, 57))
temp = 0
check = True
for item in progressBar(items, prefix = '| Connecting:', suffix = ' ', length = 20):
    if item == 0:
        try:
            client.connect((inp[1], int(inp[3])))
            print('|>> Connecting to server ' + inp[1] + ' ')
        except socket.error as e:
            print('|>> Fail to connect to the server! Restart the client to connect again!')
            print(str(e))
            check = False
            client.close()
            break
    temp+=1
    time.sleep(0.02)   


while check:
    system('cls')
    print('| >>--LOGIN/ REGISTER--<<')
    print('| Command:\n| - Login: login [username]\n| - Register: register [username]\n| - Exit: end')
    data = input()
    parser = data.split()
    client.send(str.encode(parser[0]))
    if parser[0] == 'login' and len(parser) == 2:
        login_code = Login(parser, client)

        if login_code == 1:
            for i in tqdm(range(100)):
                time.sleep(0.005)
            client.send(b' ')
            client_handle(client)
        elif login_code == -1:
            print('| Please try again!')
            time.sleep(0.2)
        else:
            break
    elif parser[0] == 'register':
        Register(parser, client)
        system('pause')
    elif parser[0] == 'end':
        client.close()
        check = False
    
client.close()