import sys

def provjera_def(izlaz: list, var: str) -> int:
        #vraca index u listi na kojoj je trazena varijabla, ako varijable nema vraca -1
        #global izlaz
        found = -1
        for j in range(len(izlaz)):
               
                if izlaz[j][0] == var:
                        if found == -1: #ako jos nije nadena nijedna varijabla s tim imenom
                                found = j
                        else:
                                if izlaz[j][2] > izlaz[found][2]: #ako je nadena varijabla s tim imenom, gledaj je li sakrivena (postoji li jos jedna definicija te varijable s vecim br bloka)
                                        found = j
        #  vraca index
        return found
                
                

        
#main
dubina_bloka = 0 #o kojem bloku je rijec
operatori = ['+','-', '*', '/']
zagrade = ['(',')']
kljucneRijeci = ['za', 'az', 'od', 'do']
ulaz = []
izlaz = [] #lista s definiranim varijablama [var, redak def, dubina bloka]

makni =['<E>', '<T>', '<P>', '<T_lista>', '$', '<E_lista>', '<program>', '<lista_naredbi>', '<naredba>']
prethodni = ''
err = False #zastavica za error
error = 'err ' #string koji ce se ispisati ako dode do errora
for line in sys.stdin:
        line = line.rstrip()
        line = line.rstrip('\n') #makni spaces na pocetku i na kraju i oznaku za kraj retka
                    #citanje
        line = line.lstrip() #makni leading whitespaces
        if line not in makni:
                ulaz.append(line.split(" ")) #lista
                #ovo radi, listi su clanovi liste tipa ['IDN', '1', 'x'] bez E T P E_lista T_lista i tih


#print(ulaz)
i = 0
for i in range(len(ulaz)):
        
        #print(ulaz[i])
        if i>len(ulaz):
                break
        if err:
                break
        if ulaz[i][0] == '<za_petlja>': #obradi ZA OD DO
                dubina_bloka += 1
                i+=2 #skoci na IDN
                redak = ulaz[i][1]
                var = ulaz[i][2] 
                izlaz.append([var, redak, dubina_bloka]) #ovo je automatska inicijalizacija varijable u ZA dijelu
                #print(izlaz)
                i+=2 #preskoci KROD i citaj expression

                while i < len(ulaz):
                        #obrada E-ova
                        if len(ulaz[i]) > 1:
                                if ulaz[i][0] == 'IDN': #npr varijabla z
                                        index = provjera_def(izlaz, ulaz[i][2]) #gledaj je li varijabla definirana
                                        if index == -1 or izlaz[index][0] == var: #ako se koristi nedefinirana varijabla ili varijabla definirana nakon ZA onda error
                                                #print("err")
                                                dobra_def = False
                                                err = True
                                                error += ulaz[i][1] + " " + ulaz[i][2]
                                                print(error)
                                                break
                                        else: 
                                                print(redak + " "+izlaz[index][1]+" "+izlaz[index][0]) #inace koristi se neka varijabla i to s ispisuje

                        if ulaz[i+1][0] == '<naredba_pridruzivanja>' or ulaz[i+1][0] == '<za_petlja>':
                                break
                        else:
                                i += 1
                
                
                
        elif ulaz[i][0] == '<naredba_pridruzivanja>': #obradi pridruzivanje
                #pridruzi, na ulazu IDN i =
                i+=1 #na IDN
                var = ulaz[i][2] #potencijalno nova varijabla
                redak = ulaz[i][1]
                #nova = [var, redak_def, dubina_bloka]
                postoji = False
                index = provjera_def(izlaz, var)
                if index != -1:
                        postoji = True
                                
                if not postoji: #dodavanje, ne treba provjeravati dubinu
                        #provjeri da definicija nije u stilu x=x+3 ili s nedef. varijablom
                        #redak = ulaz[i][1] #gledaj sve sto je u tom retku
                        dobra_def = True
                        i+=2 #preskoci = i gledaj sto je s desne strane
                        
                        while (i < len(ulaz) and len(ulaz[i]) != 1 and ulaz[i][1] == redak and dobra_def):
                                
                                if ulaz[i][0] == 'IDN': #npr varijabla z
                                        index = provjera_def(izlaz, ulaz[i][2]) #gledaj je li varijabla definirana
                                      
                                        if index == -1:
                                                #print("err")
                                                dobra_def = False
                                                err = True
                                                error += ulaz[i][1] + " " + ulaz[i][2]
                                                print(error)
                                                break
                                        else:
                                                print(redak + " "+izlaz[index][1]+" "+izlaz[index][0]) #inace koristi se neka varijabla i to s ispisuje
                                                
                                
                                i += 1
                        if dobra_def:      
                                izlaz.append([var, redak, dubina_bloka]) #dodaj u izlaz
                else: #ako varijabla vec postoji (a koristi se, ispisi ju)
                        i+=2 #preskoci = , gledaj desnu stranu
                        redak = ulaz[i][1]
                        dobra_def = True
                        
                        while (i < len(ulaz) and len(ulaz[i]) != 1 and ulaz[i][1] == redak and dobra_def):
                                if ulaz[i][0] == 'IDN':
                                        
                                        index = provjera_def(izlaz, ulaz[i][2]) #gledaj je li varijabla definirana
                                        
                                        if index == -1:
                                                dobra_def = False
                                                err = True
                                                error += ulaz[i][1] + " " + ulaz[i][2]
                                                print(error)
                                                break
                                        else:
                                                print(redak + " "+izlaz[index][1]+" "+izlaz[index][0])
                                i+=1
                                                

        elif ulaz[i][0] == 'KR_AZ': #smanji blok
               
                dubina_bloka -= 1
                
                #makni sve varijable koje vise ne postoje
                k = 0
                broj = len(izlaz)
                pomocna = []
                while k < broj:
                       
                        if izlaz[k][2] <= dubina_bloka and k <len(izlaz):
                                var =izlaz[k]
                                pomocna.append(var)
                        k+=1
                izlaz = pomocna

                        
                
           









        
