import sys

brojacRedaka = 1;
prijelazi = dict()

#LAB1 UTR

#procitaj podatke po retcima i spremi ih
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
        #ucitaj prihvatljiva stanja
        prihvStanja = line.split(",")
    elif brojacRedaka == 5:
        #ucitaj pocetno stanje
        pocetnoStanje = str(line)
    else:
        #ucitavanje funkcije prijelaza u rjecnik
        #trenutnoSt,simbol->skupIducihStanja
        temp1 = line.split('->')
        temp2 = temp1[0].split(',')
        kljuc = (temp2[0], temp2[1]) #kljuc je tuple koji se sastoji od stanja i simbola
        prijelazi[kljuc] = temp1[1].split(',') #vrijednost je lista stanja

    brojacRedaka += 1


for niz1 in nizovi:
    niz = niz1.split(',')
    trenutnaStanja = []
    trenutnaStanja.append(pocetnoStanje)
    sljedecaStanja = []
    vecIspisanaTrenutna = False
    prazanSkup = False
    
    for i in range(len(niz)+1): #citanje simbola po nizu
        
        dodanoStanje = True
        while dodanoStanje: #dodavanje stanja dobivena eta prijelazima u listu trenutnih stanja
            dodanoStanje = False
            for stanje in trenutnaStanja:
                if (stanje, "$") in prijelazi and not (set(prijelazi[(stanje, "$")]).issubset(set(trenutnaStanja))) and not prazanSkup:
                    for stanje1 in prijelazi[(stanje, "$")]:
                        if stanje1 not in trenutnaStanja and stanje1 != '#':
                            trenutnaStanja.append(stanje1)
                            dodanoStanje = True
       
        for stanje in trenutnaStanja:
            if i < len(niz) and not prazanSkup:    
                if (stanje, niz[i]) in prijelazi and not (set(prijelazi[(stanje, niz[i])]).issubset(set(sljedecaStanja))):
                        for stanje1 in prijelazi[(stanje, niz[i])]:
                            if stanje1 not in sljedecaStanja and stanje1 != '#':
                               sljedecaStanja.append(stanje1) #radimo listu sljedecih stanja preko prijelaza u iduca na temelju ulaznog simbola
        
        if not vecIspisanaTrenutna and not prazanSkup: #ako nismo jos ispisali trenutna stanja
                izlaznaLista = sorted(trenutnaStanja) #sortiramo trenutna stanja
                izlaz = ",".join(izlaznaLista) 
                print(izlaz, end="") #ispis
                if i < len(niz):
                        print("|", end="") #ako nije zadnji 

        
        if not sljedecaStanja and i != len(niz): #ako nema sljedeceg stanja a nije zadnji loop ispisujemo #
                print("#", end="")
                if i < len(niz)-1:
                        print("|", end="")
                vecIspisanaTrenutna = True
                prazanSkup = True #ne azuriramo trenutna stanja sljedecim jer nemamo sljedecih, trenutna su vec ispisana
        else:
                trenutnaStanja = sljedecaStanja.copy()
                sljedecaStanja.clear()
                vecIspisanaTrenutna = False  #ako imamo sljedeca stanja ona za iduci znak postaju trenutna a sljedeca se brisu jer cese generirati na temelju trenutnih
        

    print() #novi red nakon svakog niza
   
    
