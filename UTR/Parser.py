import sys


def S():
        global nemojDalje #globalne varijable
        global izlaz
        global ulazniNiz
        global i
        if not nemojDalje:
                izlaz += 'S'
                if i >= len(ulazniNiz) or ulazniNiz[i] != 'a' and ulazniNiz[i] != 'b':
                        nemojDalje = True #na ulazu je c ili smo prosli cijeli niz pa je tu kraj citanja niza
                elif ulazniNiz[i] == 'a': #aAB
                        i += 1
                        A()
                        B()
                elif ulazniNiz[i] == 'b': #bBA
                        i += 1
                        B()
                        A()
        
   

def A():
        global nemojDalje
        global izlaz
        global ulazniNiz
        global i
        if not nemojDalje:
                izlaz += 'A'
                if i >= len(ulazniNiz) or ulazniNiz[i] != 'a' and ulazniNiz[i] != 'b':
                        nemojDalje = True #na ulazu je c ili smo prosli cijeli niz
                elif ulazniNiz[i] == 'a': #a
                        i += 1
                elif ulazniNiz[i] == 'b': #bC
                        i += 1
                        C()
                


def B():
        global nemojDalje
        global izlaz
        global ulazniNiz
        global i
        if not nemojDalje:
                izlaz += 'B'
                if i < (len(ulazniNiz)-1) and ulazniNiz[i] == 'c' and ulazniNiz[i+1] == 'c': #cc
                        i += 2
                        S() #poziv nezavrsenog znaka
                if i < (len(ulazniNiz)-1) and ulazniNiz[i] == 'b' and ulazniNiz[i+1] == 'c': #bc
                        i += 2
                #sve ostalo se moze napraviti eta prijelazom

def C():
        global izlaz #nema uvjeta
        izlaz += 'C' #AA
        A()
        A()

    


for line in sys.stdin:
    line = line.rstrip('\n')
    ulazniNiz = list(line)
 #ulazni niz
      #zastavica kad treba zaustaviti rad
nemojDalje = False
i = 0 #index na kojem citamo znak
izlaz ="" #nezavrseni znakovi
S() #zapocni
print(izlaz) #ispis nezavrsenih znakova
if i < len(ulazniNiz): #ako nisu procitani svi znakovi
        nemojDalje = True
if nemojDalje:
        print('NE') #prihvatljivo ili ne
else:
        print('DA')
