import sys
brojacRedaka = 1;
prijelazi = dict()

#LAB2 UTR

for line in sys.stdin:
        line = line.rstrip('\n')
        if brojacRedaka == 1: #ucitaj moguca stanja
                stanja = line.split(",")
        elif brojacRedaka == 2:
                #ucitaj moguce simbole na ulazu
                simboli = line.split(",")
        elif brojacRedaka == 3:
                #ucitaj prihvatljiva stanja
                prihvStanja = line.split(",")
        elif brojacRedaka == 4:
                #ucitaj pocetno stanje
                pocetnoStanje = str(line)
        else:
                #ucitavanje funkcije prijelaza u rjecnik
                #trenutnoSt,simbol->skupIducihStanja
                temp1 = line.split('->')
                temp2 = temp1[0].split(',')
                kljuc = (temp2[0], temp2[1]) #kljuc je tuple koji se sastoji od stanja i simbola
                prijelazi[kljuc] = temp1[1] #vrijednost je stanje u koje se prelazi

        brojacRedaka += 1
            
# trazenje nedohvatljivih stanja

dohvStanja = [] #lista dohvatljivih stanja
nedohvStanja = []
dohvStanja.append(pocetnoStanje)
dodanoStanje = True

while dodanoStanje:  #ponavljaj ako je u listu dohvatljivih nesto dodano
    dodanoStanje = False
    for stanje in dohvStanja:
        for simbol in simboli:
            if (stanje, simbol) in prijelazi and prijelazi[(stanje, simbol)] not in dohvStanja: #za svako stanje i svaki njegov prijelaz provjeri je li stanje u koje prijelazi vec u listi
                dohvStanja.append(prijelazi[(stanje, simbol)])
                #ako nije u listi, dodaj ga, zastavica za dodano stanje je True
                dodanoStanje = True


dohvStanja.sort()

for stanje in stanja:
    if stanje not in dohvStanja:
        nedohvStanja.append(stanje)
        
stanja = dohvStanja #updateamo listu stanja koja se sad sastoji samo od dohvatljivih


for stanje in nedohvStanja:
    if stanje in prihvStanja:
        prihvStanja.remove(stanje)
    for simbol in simboli:
        del prijelazi[(stanje, simbol)] #iz prijelaza izbacimo nedohvatljiva stanja


# minimizacija, izbacivanje duplikata stanja


#prve dvije grupe
G11 = prihvStanja
G12 = []
#prva podjela i nova podjela
podjela = []
podjelaNova=[]
for stanje in stanja:
        if stanje not in prihvStanja:
                G12.append(stanje) #lista neprihvatljivih stanja
#podjela je lista koja se sastoji od lista             
podjelaNova.append(G11)
podjelaNova.append(G12)



prijelazi2 = prijelazi.copy() 


while (True):
      
        podjela = podjelaNova
        podjelaNova =[]
        
        for stanje in stanja:
                for simbol in simboli:
                        for grupa in podjela:
                                if prijelazi[(stanje, simbol)] in grupa:
                                        prijelazi2[(stanje, simbol)] = grupa
                                        #novi rjecnik prijelaza u koji ce ici grupe a ne sljedeca stanja
   
        for grupa in podjela:
                #podijeli na nove grupe ako imaju iste prijelaze
                for stanje in grupa:
                        for i in range(len(grupa)):
                                if grupa[i] != stanje: #medusobno usporeduj svako stanje sa svakim osim stanja koja su istu
                                        odgSimboli = 0 #za koliko simbola imaju iste prijelaze
                                        for simbol in simboli:
                                                if prijelazi2[(stanje, simbol)] == prijelazi2[(grupa[i], simbol)]:
                                                        odgSimboli +=1
                                        if odgSimboli == len(simboli): #ako imaju sve iste prijelaze
                                                 # nadi ili grupu s istim prijelazima ili napravi novu
                                                if not podjelaNova: #ako nema nista u novoj podjeli
                                                        temp = []
                                                        temp.append(stanje)
                                                        temp.append(grupa[i])
                                                        temp.sort()
                                                        podjelaNova.append(temp)
                                                elif not (any(grupa[i] in sublist for sublist in podjelaNova)):
                                                        #ako grupa[i] nije uopce sadrzana u novoj podjeli, pretrazi novu podjelu i nadi joj mjesto 
                                                        #tako da u novoj podjeli nades grupu u kojoj je stanje ili stvori novu grupu u podjeli
                                                        if any(stanje in sublist for sublist in podjelaNova): #ako postoji grupa koja sadrzi stanje onda grupa[i] ide u tu grupu
                                                                for grupaNova in podjelaNova:
                                                                        for stanjePoc in grupaNova:
                                                                                if stanjePoc == stanje:
                                                                                        grupaNova.append(grupa[i]) #nasli smo joj grupu
                                                        else:
                                                                temp = []
                                                                temp.append(stanje)
                                                                temp.append(grupa[i])
                                                                temp.sort()
                                                                podjelaNova.append(temp)

                                                                #to su potencijalna ekvivalentna stanja
                                                                #ako neko stanje nije pripalo nijednoj grupi onda je ono grupa za sebe
        
        
        for stanje1 in stanja:
                if not (any(stanje1 in sublist for sublist in podjelaNova)):
                        temp = []
                        temp.append(stanje1)
                        podjelaNova.append(temp)
        podjelaNova.sort()
       
        if podjela == podjelaNova:
                break

#ako smo izasli iz while petlje to znaci da su podjela i podjelaNova iste
#treba ukloniti istovjetna stanja
stanjaMin = []
prihvStanjaMin = []
prijelaziMin = dict()

for grupa in podjela:
        for stanje in grupa:
                if len(grupa) !=1:
                        grupa.sort()
                        if grupa[0] not in stanjaMin:
                                if pocetnoStanje in grupa and grupa[0] != pocetnoStanje:
                                        pocetnoStanje = grupa[0]
                                stanjaMin.append(grupa[0])
                else:
                        stanjaMin.append(grupa[0]) #azuriraj stanja
stanjaMin.sort()
for stanje in stanjaMin:
        if stanje in prihvStanja:
                prihvStanjaMin.append(stanje) #azuriraj prihvatljiva stanja

prihvStanjaMin.sort()

for stanje in stanjaMin:
        for simbol in simboli:
                prijelaziMin[(stanje, simbol)] = prijelazi2[(stanje, simbol)] #azuriraj prijelaze pt1
                
for kljuc in prijelaziMin:
        for stanje in prijelaziMin[kljuc]:
                if stanje in stanjaMin:
                        prijelaziMin[kljuc] = stanje  #azuriraj prijelaze pt1

redak1 = ",".join(stanjaMin)
redak2 = ",".join(simboli)
redak3 = ",".join(prihvStanjaMin)
temp = []
for kljuc in prijelaziMin:
        x = ",".join(kljuc)
        x = x + "->" + prijelaziMin[kljuc]
        temp.append(x)

print(redak1)
print(redak2)
print(redak3)
print(pocetnoStanje)
for x in temp:
        print(x)


       
                
                


                                                                        
                                                
                                                        
                                                        
                
                                
                                
                               
                                        
                                        
                        




