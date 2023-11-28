#import pycryptodome
import sys
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
import json

## Procitati file s uputama prije koristenja, hvala!

filename = 'Pwdmanager.txt'

#velicine potrebnih elemenata u byte

TAG = 16
KEY = 32

SALT = 32
NONCE = 16

N_VAL = 2**20
R_VAL = 8
P_VAL = 1

def encrypt(master, decryptedtxt):
    file = open(filename, 'wb')
    file.seek(0)
    file.truncate()
    
    salt = get_random_bytes(SALT)
    nonce = get_random_bytes(NONCE)
    #kljuc za master
    key = scrypt(master, salt, key_len=KEY, N=N_VAL, r=R_VAL, p=P_VAL)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    #pisanje u fajl
    file.write(salt)
    file.write(nonce)
    file.write(cipher.encrypt(decryptedtxt))
    file.write(cipher.digest())
    file.close()

def decrypt(master):
    file = open(filename, 'rb+')
    key = scrypt(master, salt=file.read(SALT), key_len=KEY, N=N_VAL,r=R_VAL, p=P_VAL)
    cipher = AES.new(key, AES.MODE_GCM, nonce=file.read(NONCE))

    size = os.path.getsize(filename) - NONCE - SALT - TAG
    encrypted = file.read(size)
    decrypted = cipher.decrypt(encrypted)
    tag = file.read(TAG)
   
    try:
        cipher.verify(tag)
    except ValueError as e:
        print('Using wrong master password or password file has been compromised.')
        file.close()
        exit(1)

    file.close()
    return json.loads(decrypted.decode()) #vraca dict


def init(master):
    if os.path.isfile(filename): 
        print('Password manager already initialized, delete file Pwdmanager.txt and run init command again to initialize a new manager.')
        return
    encrypt(master, '{}'.encode())
    print('Password manager initialized.')

def put(master, user, pwd):
    decrypted = decrypt(master)
    decrypted.update({ user : pwd })
    encrypt(master, json.dumps(decrypted).encode())
    print('Stored password for ' + user)


def get(master, user):
    decrypted = decrypt(master)
    if decrypted.get(user) is not None:
        print('Password for ' + user + ' is: ' + decrypted.get(user))
    else:
        print('Username not found.')


#main
if len(sys.argv) > 1:
    if str(sys.argv[1])=='init':
        init(str(sys.argv[2]))
    elif not os.path.isfile(filename):
        print('Password manager not initialized.')
        exit()
    elif str(sys.argv[1])=='put':
        put(str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
       
    elif str(sys.argv[1])=='get':
        get(str(sys.argv[2]), str(sys.argv[3]))
    else:
        print("Wrong command. Use one of 3: init [masterpass], put [masterpass] [username] [password], get [masterpass] [username]")
else:
    print("Wrong command. Use one of 3: init [masterpass], put [masterpass] [username] [password], get [masterpass] [username]")

