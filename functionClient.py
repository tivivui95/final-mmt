import socket
import stdiomask
from os import system, name

def encrypt(message, client):
    print('Do you want to encrypt the message ? (Y/N)')
    check = input()
    if check == 'Y':
        client.send(b'e')
        client.recv(2048)
        client.send(str.encode(message.encode('utf-8').hex()))
        print('| v | Data encrypted')
    else:
        client.send(b'n')
        client.recv(2048)
        client.send(str.encode(message))
        print('| ! | Data is not encrypted')

def Login(data,ClientSocket):
    username=data[1]
    password=stdiomask.getpass('>>password: ')
    message='login ' + username + ' ' + password
    encrypt(message, ClientSocket)
    # ClientSocket.send(str.encode(message))
    respone=ClientSocket.recv(2048)
  
    try:
        result=int(respone)
        if(result==1):
            print('| Login successfully.')
            #return 1: Login successfully.
            return 1
        elif result==-1:
            print('| ! | Invalid username or password. Please try again.')
            return -1
    except:
        print('Invalid respone.')
        return -1
   
def Register(data, ClientSocket):
    if len(data)<2: 
        print('Invalid username. Please input again')
        return
    username=data[1]
    password=stdiomask.getpass('>>password: ')
    message='register ' +username+' '+password

    #checkEncrypt,message=encryptMessage(message)
    encrypt(message, ClientSocket)
    # ClientSocket.send(str.encode(message))
    respone=ClientSocket.recv(1024)
    while int(respone)==-1:
        print('User exists. Please enter another name.')
        username=input('register ')
        password=stdiomask.getpass('>>password: ')
        message=username+' '+password
        
        
        #checkEncrypt,message=encryptMessage(message)

        ClientSocket.send(str.encode(message))
        respone=ClientSocket.recv(1024)
        respone=respone.decode('utf-8')

    ClientSocket.send(str.encode('1'))
    respone=ClientSocket.recv(1024)
    print(respone.decode('utf-8'))

def changePassword(ClientSocket):
    password=stdiomask.getpass('>>password: ')
    message='change_password '+password
    encrypt(message, ClientSocket)
    respone=ClientSocket.recv(1024)
    while int(respone)==-1:
        print('Wrong password. Please input again.')
        password=stdiomask.getpass('>>password: ')
        message=password
        encrypt(message, ClientSocket)
        respone=(ClientSocket.recv(1024)).decode('utf-8')
    if int(respone)==1:
        newpassword=stdiomask.getpass('>>new password: ')
        message = newpassword
        encrypt(message, ClientSocket)
        # ClientSocket.send(str.encode(message))
    respone=ClientSocket.recv(1024)
    print(respone.decode('utf-8'))
    system('pause')

def startGame(client):
    print('Starting')
    while True:
        res = client.recv(1024).decode('utf-8')
        print(res)
        if not res:
            break