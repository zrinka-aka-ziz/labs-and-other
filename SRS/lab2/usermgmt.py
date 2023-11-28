#ADMIN
#0036517187

#ass, passwd, forcepass, del

import bcrypt
import sys
import os
import json
import getpass
import base64


filename = 'stored.txt'
def check_pass(pwd):
    if (any(x.isupper() for x in pwd) and any(x.islower() for x in pwd) and any(x.isdigit() for x in pwd) and len(pwd) >= 8):
        return True
    else:
        print("Password must be at least 8 characters long, must contain at least 1 number, one capital letter and one lower letter. Password example: Pass1234")
        print("Please enter a new password or exit.")
        return False
    
def add(user, d):
    if user in d.keys():
                print("Name already in use. Exiting.")
                return
    try:
        pwd_og = getpass.getpass(prompt="Password: ")
        try:
            pwd_rep = getpass.getpass(prompt="Repeat password: ")
        except Exception as err:
            print('Error occured: ', err)
    except Exception as err:
       print('Error occured: ', err)
    if pwd_og != pwd_rep:
        print('Password mismatch. Failed to add user.')
        exit()
    else:
        if not check_pass(pwd_og):
            add(user, d)
        else:
            
        #hash za pass
            b=pwd_og.encode(encoding='utf-8')
            pwdh=base64.b64encode(b)
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(pwdh, salt)
            #print(hashed)
           # pwdh=base64.b64encode(hashed)
        #dodaj u rjecnik - zastavica i hash za pwd
            l=list()
            l.append(0)
            l.append(hashed.decode())
            #l.append(salt)
            d[user]=l
        #upisi u file
            file=open(filename, 'w')
            #json.dump(d)
            json.dump(d, file)#
            #json.dump(d, file)
            file.close()
            print('User added successfully.')
        

def passwd(user, d):
    if user not in d.keys():
        print("User does not exist. Exiting.")
        return
    try:
        pwd_og = getpass.getpass(prompt="Password: ")
        try:
            pwd_rep = getpass.getpass(prompt="Repeat password: ")
        except Exception as err:
            print('Error occured: ', err)
    except Exception as err:
       print('Error occured: ', err)
    if pwd_og != pwd_rep:
        print('Password mismatch. Failed to change password.')
        exit()
    else:
        if not check_pass(pwd_og):
           passwd(user)
        else:
            b=pwd_og.encode(encoding='utf-8')
            pwdh=base64.b64encode(b)
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(pwdh, salt)
           
        #dodaj u rjecnik - zastavica i hash za pwd
            l=[]
            l.append(0)
            l.append(hashed.decode())
            #l.append(salt)
            d[user]=l
        #upisi u file
            file=open(filename, 'w')
            #json.dump(d)
            json.dump(d, file)#
            #json.dump(d, file)
            file.close()
            print('User password changed successfully.')
        
        
    
def force(user, d):
    if user not in d.keys():
        print("Username does not exist. Exiting.")
        exit()
        #dodaj u rjecnik - zastavica 
    d[user][0]=1
        #upisi u file
    file=open(filename, 'w')
            #json.dump(d)
    json.dump(d, file)#
            #json.dump(d, file)
    file.close()
    print('User will be requested to change password on next login.')
    
def delete(user, d):
    if user not in d.keys():
        print("Username does not exist. Exiting.")
        exit()
      
        #brisi kljuc
    del d[user]
        #upisi u file
    file=open(filename, 'w')
            #json.dump(d)
    json.dump(d, file)#
            #json.dump(d, file)
    file.close()
    print('User deleted successfully.')
    
#main
    #napravi file i u njega stavi prazan rjecnik kao json object/text
if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
    file = open(filename, 'w') #otvara ili stvara file
    d={}
    json.dump(d, file)
    #file.write(line)
    file.close()
else:
    file=open(filename, 'r')
    d=json.load(file)
    file.close()
    #print(type(d))
if len(sys.argv) > 1:
    if str(sys.argv[1])=='add':
        add(sys.argv[2], d)
##    elif not os.path.isfile(filename):
##        print('User management not initialized.')
##        exit()
    elif str(sys.argv[1])=='passwd':
       passwd(sys.argv[2], d)   
    elif str(sys.argv[1])=='forcepass':
        force(sys.argv[2], d)
    elif str(sys.argv[1])=='del':
        delete(sys.argv[2],d)
    else:
        print("Wrong command. Use one of the following: add [username], passwd [username], forcepass [username], del [username]")
else:
    print("Wrong command. Use one of the following: add [username], passwd [username], forcepass [username], del [username]")
