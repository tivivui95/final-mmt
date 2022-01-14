import numpy as np 
import socket, pickle
from _thread import *
import csv
from convertnumpy import bytes_to_array
from functionServer import changePassword, checkUser, parseRequest, setupInfo, encryptRecv

def checkMap(map_input):
    for row in map_input:
        for item in row:
            if item == 1: return False
    return True

def game_room(id, client_1, client_2, addr_1, addr_2):
    client_1.send(b'input')
    data_1 = client_1.recv(4096)
    # data_1.seek(0)
    map_1 = np.array(pickle.loads(data_1))
    # print(map_1)
    np.savetxt(str(id) + '.txt', map_1, delimiter=' ')
    client_2.send(b'input')
    data_2 = client_2.recv(4096)
    # data_2.seek(0)
    map_2 = np.array(pickle.loads(data_2))
    # print(map_2)
    np.savetxt(addr_2 + '.txt', map_2, delimiter=' ')
    client_1.send(b'Game Started!')
    while not checkMap(map_1) and not checkMap(map_2):
        client_1.send(b'Your Turn!')
        attack_1 = client_1.recv(2048).decode('utf-8')
        locate_1 = attack_1.split()
        while map_2[int(locate_1[1])][int(locate_1[2])] == 1:
            map_2[int(locate_1[1])][int(locate_1[2])] = 0
            if checkMap(map_2):
                break
            client_1.send(b'Your Turn!')
            attack_1 = client_1.recv(2048).decode('utf-8')
            locate_1 = attack_1.split()
        if checkMap(map_2):
            break
        if map_2[int(locate_1[1])][int(locate_1[2])] == 0:
            client_1.send(b'Miss!!!!!')
        
        client_2.send(b'Your Turn!')
        attack_2 = client_2.recv(2048).decode('utf-8')
        locate_2 = attack_2.split()
        while map_1[int(locate_2[1])][int(locate_2[2])] == 1:
            map_1[int(locate_2[1])][int(locate_2[2])] = 0
            if checkMap(map_1):
                break
            client_2.send(b'Your Turn!')
            attack_2 = client_2.recv(2048).decode('utf-8')
            locate_2 = attack_2.split()
        if checkMap(map_1):
            break
        if map_1[int(locate_2[1])][int(locate_2[2])] == 0:
            client_2.send(b'Miss!!!!!')
    
    if checkMap(map_1):
        client_2.send(b'win')
        client_1.send(b'lose')
    else:
        client_1.send(b'win')
        client_2.send(b'lose')
    check_1 = client_1.recv(2048).decode('utf-8')
    check_2 = client_2.recv(2048).decode('utf-8')
    if check_1 == check_2 and check_1 == 'Y':
        game_room(id, client_1, client_2, addr_1, addr_2)
    else:
        client_1.send(b'end')
        client_2.send(b'end')

def logout(client, addr, onliner, listSocks):
    for online in onliner:
        if online[0] == client:
            onliner.remove(online)
            break
    client.send(b'logout')

def change_password(client, addr, password, index, listAccount):
    client.send(b'change_password')
    data = encryptRecv(client, 0)
    changePassword(client, data, index, listAccount)

def check_user(client, addr, listAccount, onliner):
    client.send(b'input')
    data = client.recv(2048)
    data = data.decode('utf-8')
    print(str(addr[0]) + ':' + str(addr[1]) , 'Checking option:', data)
    checkUser(client, data, listAccount, onliner)

def setup_info(client, addr, listAccount, index):
    client.send(b'input')
    data = client.recv(2048)
    data = data.decode('utf-8')
    print(str(addr[0]) + ':' + str(addr[1]) , 'Setting up option:', data)
    setupInfo(client,data,listAccount,index)

def game_handler(client, addr, listSocks, onliner, check, username, gameStart):
    client.send(str.encode('User list:'))
    for onl in onliner:
        client.send(str.encode(onl[1]))
        client.send(b' ')
    client.send(b'input')
    room_info = client.recv(2048).decode('utf-8')
    gameStart = True
    f = open("check.txt", "w")
    f.write("True")
    f.close()
    print(str(addr[0]) + ':' + str(addr[1]), 'Recieved room info')
    room_info = room_info.split()
    if len(room_info) == 4:
        for onl in onliner:
            if room_info[3] == onl[1]:
                onl[0].send(b'join')
                onl[0].recv(2048)
                onl[0].send(str.encode('You got invitation from ' + username))
                data = onl[0].recv(2048)
                data = data.decode('utf-8')
                if data == 'Y':
                    print('Room created')
                    game_room(room_info[1], client, onl[0], addr, onl[1])
                    check = True
                    gameStart = False
                    f = open("check.txt", "w")
                    f.write("F")
                    f.close()
                    break
                else:
                    client.send('|> Invitation rejected! ')
                    onl[0].send('|> Invitation rejected! ')
                    break