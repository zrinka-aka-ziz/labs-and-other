import sys

brojacRedaka = 1
prijelazi = dict()



for line in sys.stdin:
    line = line.rstrip('\n')
    if brojacRedaka == 1:
                #ucitaj ulazne nizove
                nizovi = line.split("|")
    elif brojacRedaka == 2:
                #ucitaj moguca stanja
                stanja = line.split(",")
    elif brojacRedaka == 3:
                #ucitaj moguce simbole na ulazu
                simboli = line.split(",")
    elif brojacRedaka == 4:
                #ucitaj znakove stoga
                stogZn = line.split(",")
    elif brojacRedaka == 5:
                #ucitaj prihvatljiva stanja
                prihvStanja = line.split(",")
    elif brojacRedaka == 6:
                #ucitaj pocetno stanje
                pocetnoStanje = str(line)
    elif brojacRedaka == 7:
                #ucitaj pocetni znak stoga
                pocStog = str(line)
        
    else:
                #ucitavanje funkcije prijelaza u rjecnik
                #trenutnoSt,simbol,znakStoga->novoStanje,nizZnakvaStoga
                    
                temp1 = line.split('->')
                temp2 = temp1[0].split(',')
                kljuc = (temp2[0], temp2[1], temp2[2]) #kljuc je tuple koji se sastoji od stanja, simbola i znaka stoga
                prijelazi[kljuc] = temp1[1].split(',') #vrijednost je lista koja se sastoji od novog stanja i niza znakova stoga

    brojacRedaka += 1


#print(nizovi)
#print(stanja)
#print(simboli)
#print(stogZn)
#print(prihvStanja)
#print(pocetnoStanje)
#print(pocStog)
#print(prijelazi)
#print()

            # ovo radi ne diraj!!!!

       
       
      
for niz1 in nizovi: #za svaki niz znakova u nizu
        niz = niz1.split(',') #lista simbola na ulazu
        #izlaznaStanja = [] #kolekcija podataka za ispis
        #izlazniStog = []
        trenutnoStanje = pocetnoStanje
        trenutniStog = pocStog
        fail = False
        
        #izlaznaStanja.append(trenutnoStanje) #koristit ce se za ispis
        #izlazniStog.append(trenutniStog)
        prazanStog = False #zastavica je li stog prazan
        print(str(trenutnoStanje) + '#' + str(trenutniStog) + '|', end="")
        
        for i in range(len(niz)+1): #citanje simbola po nizu

                if not trenutniStog:
                        prazanStog = True
                
                
                if i != len(niz):
                        if not prazanStog:
                                vrh = list(trenutniStog) #nadi vrh stoga
                                vrhStoga = vrh[0]
                                
                        else:
                                vrhStoga = '$'
                                      
                        
                        while (trenutnoStanje, "$", vrhStoga) in prijelazi and not prazanStog:

                                trenutniStog = trenutniStog[:0] + trenutniStog[1:] # skini element s vrha stoga

                                
                                sljedeceStanje = prijelazi[(trenutnoStanje, "$", vrhStoga)][0]
                                sljStog = prijelazi[(trenutnoStanje, "$", vrhStoga)][1]
                                
                                if sljStog != '$': #ako se ne skida sa stoga
                                        sljedeciStog = sljStog + trenutniStog
                                        
                                else: #ako se skida sa stoga
                                        sljedeciStog = trenutniStog
                                        
                                trenutnoStanje = sljedeceStanje
                                trenutniStog = sljedeciStog

                                if not trenutniStog:
                                        prazanStog = True
                                        vrhStoga = '$'
                                        print(str(trenutnoStanje) + '#$|', end="")
                                else:
                                        vrh = list(trenutniStog)
                                        vrhStoga = vrh[0]
                                        print(str(trenutnoStanje) + '#' + str(trenutniStog) + '|', end="")
                                       
                                        
                        ## nadi prijelaze
                        if (trenutnoStanje, niz[i], vrhStoga) in prijelazi:

                                trenutniStog = trenutniStog[:0] + trenutniStog[1:] # skini element s vrha stoga
                                
                                sljedeceStanje = prijelazi[(trenutnoStanje, niz[i], vrhStoga)][0]
                                sljStog = prijelazi[(trenutnoStanje, niz[i], vrhStoga)][1]
                                
                                if sljStog != '$': #ako se ne skida sa stoga
                                        sljedeciStog = sljStog + trenutniStog
                                        
                                else: #ako se skida sa stoga
                                        sljedeciStog = trenutniStog
                                        
                                trenutnoStanje = sljedeceStanje
                                trenutniStog = sljedeciStog
                                
                                if not trenutniStog:
                                        prazanStog = True
                                        vrhStoga = '$'
                                        print(str(trenutnoStanje) + '#$|', end="")
                                else:
                                        vrh = list(trenutniStog)
                                        vrhStoga = vrh[0]
                                        print(str(trenutnoStanje) + '#' + str(trenutniStog) + '|', end="")
                                       

                        else: #ako nema takvog prijelaza onda fail
                                fail = True
                                break
                        
                                #nema prijelaza, fail
                elif i == len(niz): #extra iteracija na kraju
                        if prazanStog: # sa praznim stogom se ne moze nista
                                break
                        
                        vrh = list(trenutniStog) #nadi vrh stoga
                        vrhStoga = vrh[0]
                        
                                
                        while trenutnoStanje not in prihvStanja and (trenutnoStanje, "$", vrhStoga) in prijelazi and not prazanStog:
                                
                                trenutniStog = trenutniStog[:0] + trenutniStog[1:] # skini element s vrha stoga

                                sljedeceStanje = prijelazi[(trenutnoStanje, "$", vrhStoga)][0]
                                sljStog = prijelazi[(trenutnoStanje, "$", vrhStoga)][1]
                                
                                if sljStog != '$': #ako se ne skida sa stoga
                                        sljedeciStog = sljStog + trenutniStog
                                        
                                else: #ako se skida sa stoga
                                        sljedeciStog = trenutniStog
                                        
                                trenutnoStanje = sljedeceStanje
                                trenutniStog = sljedeciStog

                                if not trenutniStog:
                                        prazanStog = True
                                        vrhStoga = '$'
                                        print(str(trenutnoStanje) + '#$|', end="")
                                else:
                                        vrh = list(trenutniStog)
                                        vrhStoga = vrh[0]
                                        print(str(trenutnoStanje) + '#' + str(trenutniStog) + '|', end="")
                                       
 
                        
                


                
        
        if fail: #fail poseban ispis
                print("fail|0", end="")
        elif not fail:
                if trenutnoStanje in prihvStanja: #ispis prihvatljivosti
                        print("1", end="")
                else:
                        print("0", end="")                    
                
        print() #novi red nakon svakog niza







