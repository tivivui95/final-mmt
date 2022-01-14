class Account:
  def __init__(account,username, name, password,dob,note,point, invitationBox):
    account.username=username
    account.name = name
    account.password = password
    account.dob=dob
    account.note=note
    account.point=point
    account.invitationBox = invitationBox

  def username(account):
    return account.username
  def name(account):
    return account.name
  def password(account):
    return account.password
  def dob(account):
    return account.dob
  def note(account):
    return account.note
  def point(account):
    return account.point
  def invitationBox(account):
    return account.invitationBox

  def addInvitation(account, playername):
    account.invitationBox.append(playername)
  def popInvitation(account):
    return account.invitationBox.pop(0)
  def addPoint(account):
    newPoint = int(account.point) + 1
    account.point = str(newPoint)
    
  def toString(account):
    print("Name: ",end='')
    print(account.name)
    print("Dob: ",end='')
    print(account.dob)
    print("point: ",end='')
    print(account.point)