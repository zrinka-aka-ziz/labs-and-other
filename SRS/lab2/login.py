#LOGIN
#0036517187

#login i promjenu passworda ako admin to zatrazi

import bcrypt
import sys
import os
import json
import getpass
import base64
import time

filename='stored.txt'

def check_pass(pwd):
    if (any(x.isupper() for x in pwd) and any(x.islower() for x in pwd) and any(x.isdigit() for x in pwd) and len(pwd) >= 8):
        return True
    else:
        print("Password must be at least 8 characters long, must contain at least 1 number, one capital letter and one lower letter. Password example: Pass1234")
        print("Please enter a new password or exit.")
        return False

def login(user, d, br):
    
    #nema force
    try:
        pwd = getpass.getpass(prompt="Password: ")
    except Exception as err:
        print('Error occured: ', err)
    p=pwd.encode(encoding='utf-8')
    pwdh=base64.b64encode(p)
    
    #print(d[user][1].encode(encoding='utf-8'))
##    salt = bcrypt.gensalt()
##    hashed = bcrypt.hashpw(pwdh, salt)
    ##print(hashed)
    if bcrypt.checkpw(pwdh, d[user][1].encode(encoding='utf-8')):
        print("Login successful.")
        return True
    elif not bcrypt.checkpw(pwdh, d[user][1].encode(encoding='utf-8')) and br<=3:
        print("Username or password incorrect.")
        br+=1
        login(user, d, br)
    else:
        print("Username or password incorrect. 3 failed attempts - 30 seconds time out.")
        br=0
        time.sleep(30)
        login(user, d, br)
        
def force(user, d, br):
    if login(user, d, br):
        try:
            pwd_og = getpass.getpass(prompt="New password: ")
            try:
                pwd_rep = getpass.getpass(prompt="Repeat new password: ")
            except Exception as err:
                print('Error occured: ', err)
        except Exception as err:
            print('Error occured: ', err)
        if pwd_og != pwd_rep:
            print('Password mismatch. Failed to change password.')
            exit()
        else:
            if not check_pass(pwd_og):
                exit()
            else:
        #hash za pass
                p=pwd_og.encode(encoding='utf-8')
                pwdh=base64.b64encode(p)
                
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(pwdh, salt)
            
           # pwdh=base64.b64encode(hashed)
        #dodaj u rjecnik - zastavica i hash za pwd
                l=list()
                l.append(0)
                l.append(hashed.decode())
                d[user]=l
        #upisi u file
                file=open(filename, 'w')
            #json.dump(d)
                json.dump(d, file)#
            #json.dump(d, file)
                file.close()
                print('Password change successful.')
            
    
#main
    #napravi file i u njega stavi prazan rjecnik kao json object/text
if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
    print("Database is empty.")

if len(sys.argv) > 1:
    br=0
    user=sys.argv[1]
    file = open(filename, 'r')
    d=json.load(file)
    file.close()
    if user not in d.keys():
        print("Username does not exist. Exiting.")
        exit()
    if d[user][0]==0:
        login(user, d, 0)
    else:
        force(user, d, 0)
