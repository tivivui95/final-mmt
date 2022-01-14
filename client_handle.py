import numpy as np 
import socket, pickle
from _thread import *
from convertnumpy import array_to_bytes
from functionClient import changePassword
from os import system, name
import time
from tqdm import tqdm

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

def uploads_ship(client, data):
    data_send = np.array([])
    print('Upload file: ', data)
    for i in tqdm(range(100)):
        if i == 0:
            data_send = np.loadtxt(data, delimiter=' ')
            data_string = pickle.dumps(data_send.tolist())
            client.send(data_string)
        time.sleep(0.002)
    return data_send

def UI(status, data_send = np.array([])):
    if status == 'home':
        system('cls')
        print('| >>--DASHBOARD--<<')
        print('| List of commands can be used here: ')
        print('| - Start Game: start_game\n| - Check User: check_user\n| - Setup Account Info: setup_info')
        print('| - Join a game: join\n| - Change your password: change_password\n| - Log out: logout')
    elif status == 'check_user':
        print('| Options that can be checked:\n|> find\n|> online\n|> show_date\n|> show_fullname\n|> show_note\n|> show_point\n|> show_all')
        print('| - Command pallete: [option] [username]')
    elif status == 'setup_info':
        print('| Option to setup:\n|> fullname\n|> date (Birthday)\n|> note')
        print('| - Command pallete: [option] "your_input"')
    elif status == 'show_map':
        system('cls')
        print('| [0] : Blank, [1]: Shooted')
        print(data_send)
    elif status == 'game_start':
        print('| Upload map file to server (*.txt): upload_ships [file_name].txt')
def client_handle(client):
    cur_status = 'home'
    pause = False
    UI(cur_status)
    opponent_map = np.full((10, 10), 0)
    while True:
        try:
            data = client.recv(2048)
            if not data:
                break
            stringData = data.decode('utf-8')
            convert = stringData.split()
            
            if convert[len(convert) - 1] == 'input':
                for user_id in convert:
                    if user_id != 'input':
                        print(user_id)
                UI(cur_status)
                cin = input()
                if cin == 'check_user':
                    UI(cin)
                    pause = True
                elif cin == 'setup_info':
                    UI(cin)
                    pause = True
                elif cin == 'change_password':
                    pause = True
                cmdCheck = cin.split()
                if cmdCheck[0] == 'upload_ships':
                    uploads_ship(client, cmdCheck[1])
                    opponent_map = np.full((10, 10), 0)
                    UI('show_map', data_send=opponent_map)
                elif cmdCheck[0] == 'create_room':
                    UI('game_start')
                    client.send(str.encode(cin))
                else:
                    client.send(str.encode(cin))
            elif stringData == 'input':
                UI(cur_status)
                cin = input()
                if cin == 'check_user':
                    UI(cin)
                    pause = True
                elif cin == 'setup_info':
                    UI(cin)
                    pause = True
                elif cin == 'change_password':
                    pause = True
                client.send(str.encode(cin))
            elif stringData == 'Your Turn!':
                status = 'game_turn'
                print(stringData)
                data = input()
                spliter = data.split()
                opponent_map[int(spliter[1])][int(spliter[2])] = 1
                UI('show_map', data_send=opponent_map)
                client.send(str.encode(data))
            elif stringData=='logout':
                status = 'logout'
                print('Log out successfully!')
                check = False
                break
            elif stringData=='join':
                client.send(b'check')
                data = client.recv(2048)
                print(data.decode('utf-8'))
                print('Do you want to join? (Y/N)')
                data = input()
                if data == 'Y':
                    cur_status = 'game_start'
                    UI(cur_status)
                client.send(str.encode(data))
            elif stringData=='change_password':
                changePassword(client)
            elif stringData=='win':
                print('You Win!')
                print('Do you want to try again? (Y/N)')
                data = input()
                client.send(str.encode(data))
            elif stringData=='lose':
                print('You Lose!')
                print('Do you want to try again? (Y/N)')
                data = input()
                print('')
                client.send(str.encode(data))
            elif stringData=='end':
                print('End game!')
                client.send(b'end_game')
                cur_status = 'home'
                UI(cur_status)
            else:
                status = stringData
                print(stringData)
                if pause:
                    system('pause')
                    pause = False
                    cur_status = 'home'
                    UI(cur_status)
        except KeyboardInterrupt:
            break