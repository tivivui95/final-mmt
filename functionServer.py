import classAccount

#def manage_account():

def checkName(listAccount, username):
  for i in range(len(listAccount)):
    if username==listAccount[i].username:
      return i
  return -1

def encryptRecv(client, addr):
    check = client.recv(2048).decode('utf-8')
    client.send(b'rec')
    data = client.recv(2048).decode('utf-8')
    if check == 'e':
        a_string = bytes.fromhex(data)
        a_string = a_string.decode("utf-8")
        return a_string
    elif check == 'n':
        return data

def readAll(filename):
    with open(filename,'r') as reader:
        listAccount=[]
        line=reader.readline()
        while line!='':
            #remove the white space (at the beggining, end)
            line=line.strip()

            #split return a listAccount of string
            temp=line.split(',')
            
            #take out the value
            username=temp[0]
            name=temp[1]
            password=temp[2]
            dob=temp[3]
            note=temp[4]
            point=temp[5]

            p1=classAccount.Account(username,name,password,dob,note,point,[])
            #push the value into listAccount
            listAccount.append(p1)
            #read the next line
            line=reader.readline() 
    reader.close()  
    return listAccount

def writeAll(filename,listAccount):
    with open(filename,'w') as writer:
        for i in range(len(listAccount)):
            writer.write(listAccount[i].username)
            writer.write(',')
            writer.write(listAccount[i].name)
            writer.write(',')
            writer.write(listAccount[i].password)
            writer.write(',')
            writer.write(listAccount[i].dob)
            writer.write(',')
            writer.write(listAccount[i].note)
            writer.write(',')
            writer.write(listAccount[i].point)
            writer.write('\n')
    writer.close()

def parseFirstRequest(data):
    temp=data.split()
    option=temp[0]
    username=temp[1]
    password=temp[2]
    if option=='login': return option,username,password
    elif option=='register': return option,username,password
    else: return '-1','-1','-1'

def parseRequest(data):
    temp=data.split()
    #temp=[option,value] value: password/fullname/dob/note,..
    option=temp[0]
    if option=='change_password' and len(temp)==2: return option,temp[1]
    else:
        temp=data.split('-')
        option=temp[0].strip()
        if len(temp)<2:
            return '-1'
        elif option == 'setup_info': return option,temp[1]
        elif option == 'check_user': return option,temp[1]
        else: return '-1','-1'

#LOGIN
def manage_account(connection, username, password, listAccount, index, listOfClients, listRooms):
    for i in range(len(listOfClients)):
        if connection in listOfClients[i]:
            client = (connection, username)
            listOfClients.remove(listOfClients[i])
            listOfClients.append(client)
    while True:
        for i in range(len(listAccount)):
            if username == listAccount[i].username:
                user_index = i
        data = (connection.recv(1024)).decode('utf-8')
        checkEncrypt=0
        try: 
            data=bytes.fromhex(data)
            data=data.decode('utf-8')
            checkEncrypt=1
        except:
            data=data
        if data == 'check_invitation':
            #print(username + " invitation = " + str(len(listAccount[user_index].invitationBox)))
            if (len(listAccount[user_index].invitationBox) != 0):
                invitation = listAccount[user_index].popInvitation()
                connection.send(str.encode(invitation + ' invite you to join a game. Do you want to join? (Y/N)'))
                if (connection.recv(2048)).decode('utf-8') == 'Y':
                    for i in range(len(listOfClients)):
                        if invitation in listOfClients[i]:
                            listOfClients[i][0].send(str.encode('Y'))
                    #joinGame(connection, listOfClients, listAccount, user_index, listRooms)
                else:
                    for i in range(len(listOfClients)):
                        if invitation in listOfClients[i]:
                            listOfClients[i][0].send(str.encode('N'))
                    connection.send(str.encode('decline'))
            else:
                connection.send(str.encode('no invite'))
        elif data == 'start_game':
            print(str(listOfClients))
            startGame(connection=connection, listofUser=listOfClients)
        elif data == 'logout':
            for i in range(len(listOfClients)):
                if connection in listOfClients[i]:
                    client = (connection,)
                    listOfClients.remove(listOfClients[i])
                    listOfClients.append(client)
            break
        #elif data == 'start_game':
            startGame(connection, listOfClients, listAccount, user_index, listRooms)
        else:
            option,value = parseRequest(data)
            if option == 'change_password':
                changePassword(checkEncrypt,connection,value,index,listAccount)
            elif option == 'setup_info':
                setupInfo(connection,value,listAccount,index)
            elif option == 'check_user':
                checkUser(connection,value,listAccount, listOfClients)
            else:
                connection.send(str.encode('Invalid syntax. Please try again.'))

def Login(connection,username,password,listAccount):
    #Check username and password
    index = checkName(listAccount,username)
    if password != listAccount[index].password:
        index = -1

    if index!=-1:
        announce='1'
    else: 
        announce='-1'

    connection.send(str.encode(announce))
    return index, username, password
    #Annouce
        #connection.send(str.encode('1'))
        #data = connection.recv(2048)
      
def Register(connection,username,password,listAccount):
    mark=0
    #Check username
    index=checkName(listAccount,username)
    if username==' ' or index!=-1: mark=-1
    while mark==-1:
        connection.send(str.encode('-1'))
        data=(connection.recv(2048)).decode('utf-8')
        
        data=data.split(' ')
        username=data[0]
        password=data[1]
        index=checkName(listAccount,username)
        if username!=' ' and index==-1: mark=1
    #Save new account into file
    listAccount.append(classAccount.Account(username,'',password,'','','0',[]))
    writeAll('Account.txt',listAccount)
    #Annouce
    connection.send(str.encode('1'))
    data=connection.recv(2048)
    announce='Register successfully. Please login.'
    connection.send(str.encode(announce))

def changePassword(connection,password,index,listAccount):
    mark=0
    oldpassword=listAccount[index].password
    if password!=oldpassword:
        mark=-1
    while mark==-1:
        connection.send(str.encode('-1'))
        data=encryptRecv(connection, 0)
        
        if data==oldpassword:
            mark=0
    
    #Send '1' when Password is correct
    connection.send(str.encode('1'))

    #Receive new password

    data=encryptRecv(connection, 0)
    newpassword=data

    #Update
    listAccount[index].password=newpassword
    writeAll('Account.txt',listAccount)

    #Annouce
    announce='change password successfully.'
    connection.send(str.encode(announce))

def setupInfo(connection,data,listAccount,index):
    #data=[option,value], value: fullname/date/note
    option=data[0]

    #Date
    if option=='d':
        temp=data.split()
        #temp=[option,value]

        if len(temp)<2:
            connection.send(str.encode('Invalid syntax. Please try again'))
            return
        date=temp[1]
        listAccount[index].dob=date
        writeAll('Account.txt',listAccount)
        message='>>Birthday of '+listAccount[index].username+' is '+ date
        connection.send(str.encode(message))
    #Fullname and Note
    elif option=='f' or option=='n':
        temp=data.split('"')
        #temp=[option,value]
        if len(temp)<2:
            connection.send(str.encode('Invalid syntax. Please try again'))
            return
        else: 
            option=temp[0].strip()
            if option=='fullname':
                name=temp[1]
                listAccount[index].name=name
                writeAll('Account.txt',listAccount)
                message=">>"+listAccount[index].username+'\'s fullname is '+'"'+name+'"'
                connection.send(str.encode(message))

            elif option=='note':
                note=temp[1]
                listAccount[index].note=note
                writeAll('Account.txt',listAccount)
                message='>>'+listAccount[index].username+'\'s note: '+note
                connection.send(str.encode(message))

            else: connection.send(str.encode('Invalid syntax. Please try again'))

def checkUser(connection, data, listAccount, onliner):
    #Data=[option,username]
    data=data.split()
    if len(data) < 2:
        connection.send(str.encode('Invalid syntax. Please try again.'))
        return
    #Remove white space
    option=data[0].strip()
    username=data[1].strip()
    index = checkName(listAccount,username)
    if index == -1:
        connection.send(str.encode('>>User does not exist'))
    elif option=='find':
        connection.send(str.encode('>>User exists'))
    elif option=='online':
        #find in listAccount of connection
        check = False
        for user in onliner:
            if username == user[1]:
                check = True
        if check == True:
            connection.send(str.encode('>>User is online'))
        else:
            connection.send(str.encode('>>User is offline'))
    elif option=='show_date':
        date=listAccount[index].dob
        message='>>Birthday of '+username +' is '+date
        connection.send(str.encode(message))
    
    elif option=='show_fullname':
        message=">>"+username +'\'s fullname is "'+listAccount[index].name+'"'
        connection.send(str.encode(message))
    
    elif option=='show_note':
        message=">>"+username+'\'s note: '+listAccount[index].note
        connection.send(str.encode(message))

    elif option=='show_point':
        message=">>"+username+'\'s point: '+listAccount[index].point
        connection.send(str.encode(message))
    
    elif option=='show_all':
        message='\nUser name: '+username
        message+='\nFullname: '+listAccount[index].name
        message+='\nDate of birth: '+listAccount[index].dob
        message+='\nNote: '+listAccount[index].note
        message+='\nPoint: '+listAccount[index].point + '\n'
        connection.send(str.encode(message))
    else: 
        message='Invalid!'
        connection.send(str.encode(message))


def startGame(connection, listofUser):
    for user in listofUser:
        print(user)
        connection.send(str.encode(user))