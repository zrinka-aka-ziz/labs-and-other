import sys

def program():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                izlaz.append("<program>")
        #if index >= len(ulaz): return
                if ulaz[i][0] != "IDN" and ulaz[i][0] != "KR_ZA" and ulaz[i] != "zavrsni_znak":
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                else:
                        lista_naredbi()

def lista_naredbi():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<lista_naredbi>")
                if ulaz[i][0] == "IDN" or ulaz[i][0] == "KR_ZA":
                        naredba()
                        lista_naredbi()
                elif ulaz[i][0] == "KR_AZ" or ulaz[i] == "zavrsni_znak":
                        izlaz.append(" "*level + " $")
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                           
                level -= 1
        
def naredba():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<naredba>")
                if ulaz[i][0] == "IDN" :
                        naredba_pridruzivanja()
                        
                elif ulaz[i][0] == "KR_ZA":
                        za_petlja()
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                            
                level -= 1
def naredba_pridruzivanja():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<naredba_pridruzivanja>")
                if ulaz[i][0] == "IDN" :
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1 #prijedi na sljedeci redak na ulazu
                        if ulaz[i][0] == "OP_PRIDRUZI":
                                izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                                i+=1 #sljedeci redak na ulazu
                                E()
                        else:
                                if not err:
                                        err = True
                                        if ulaz[i] == "zavrsni_znak":
                                                print("err kraj")
                                        else:
                                                print("err", " ".join(ulaz[i]))
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
                
def za_petlja():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<za_petlja>")
                if ulaz[i][0] == "KR_ZA" :
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1 #prijedi na sljedeci redak na ulazu
                        if ulaz[i][0] == "IDN":
                                izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                                i+=1 #sljedeci redak na ulazu
                                if ulaz[i][0] == "KR_OD":
                                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                                        i+=1 #sljedeci redak na ulazu
                                        E()
                                        if ulaz[i][0] == "KR_DO":
                                                izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                                                i+=1 #sljedeci redak na ulazu
                                                E()
                                                lista_naredbi()
                                                if ulaz[i][0] == "KR_AZ":
                                                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                                                        i+=1 #sljedeci redak na ulazu
                                                else:
                                                        if not err: #ako zastavica jos nije postavljena, postavi ju
                                                                err = True
                                                                if ulaz[i] == "zavrsni_znak":
                                                                        print("err kraj")
                                                                else:
                                                                        print("err", " ".join(ulaz[i]))
                                        else:
                                                if not err:
                                                        err = True
                                                        if ulaz[i] == "zavrsni_znak":
                                                                print("err kraj")
                                                        else:
                                                                print("err", " ".join(ulaz[i]))
                                        
                                
                                else:
                                        if not err:
                                                err = True
                                                if ulaz[i] == "zavrsni_znak":
                                                        print("err kraj")
                                                else:
                                                        print("err", " ".join(ulaz[i]))
                        else:
                                if not err:
                                        err = True
                                        if ulaz[i] == "zavrsni_znak":
                                                print("err kraj")
                                        else:
                                                print("err", " ".join(ulaz[i]))
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
def E():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<E>")
                if ulaz[i][0] == "IDN" or ulaz[i][0] == "BROJ"  or ulaz[i][0] == "OP_PLUS"  or ulaz[i][0] == "OP_MINUS"  or ulaz[i][0] == "L_ZAGRADA":
                        T()
                        E_lista()
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
        
def E_lista():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<E_lista>")
                if ulaz[i][0] == "OP_PLUS" or ulaz[i][0] == "OP_MINUS":
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1
                        E()
                elif ulaz[i][0] == "IDN" or ulaz[i][0] == "KR_ZA" or ulaz[i][0] == "KR_DO" or ulaz[i][0] == "KR_AZ" or ulaz[i][0] == "D_ZAGRADA" or ulaz[i] == "zavrsni_znak":
                        izlaz.append(" "*level + " " + "$")
                        #i+=1
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
def T():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<T>")
                if ulaz[i][0] == "IDN" or ulaz[i][0] == "BROJ"  or ulaz[i][0] == "OP_PLUS"  or ulaz[i][0] == "OP_MINUS"  or ulaz[i][0] == "L_ZAGRADA":
                        P()
                        T_lista()
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
def T_lista():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<T_lista>")
                if ulaz[i][0] == "OP_PUTA" or ulaz[i][0] == "OP_DIJELI":
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1
                        T()
                elif ulaz[i][0] == "IDN" or ulaz[i][0] == "KR_ZA" or ulaz[i][0] == "KR_DO" or ulaz[i][0] == "KR_AZ" or ulaz[i][0] == "D_ZAGRADA" or ulaz[i][0] == "OP_PLUS"  or ulaz[i][0] == "OP_MINUS" or ulaz[i] == "zavrsni_znak":
                        izlaz.append(" "*level + " " + "$")
                        #i+=1
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
def P():
        global i
        global level
        global ulaz
        global izlaz
        global err
        if not err:
                level += 1
                izlaz.append(" "*level + "<P>")
                if ulaz[i][0] == "OP_PLUS" or ulaz[i][0] == "OP_MINUS":
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1
                        P()
                elif ulaz[i][0] == "L_ZAGRADA":
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1
                        E()
                        if ulaz[i][0] == "D_ZAGRADA":
                                izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                                i+=1
                        else:
                                if not err:
                                        err = True
                                        if ulaz[i] == "zavrsni_znak":
                                                print("err kraj")
                                        else:
                                                print("err", " ".join(ulaz[i]))
                elif ulaz[i][0] == "IDN" or ulaz[i][0] == "BROJ":
                        izlaz.append(" "*level + " " + " ".join(ulaz[i]))
                        i+=1
                else:
                        if not err:
                                err = True
                                if ulaz[i] == "zavrsni_znak":
                                        print("err kraj")
                                else:
                                        print("err", " ".join(ulaz[i]))
                level -= 1
        






#main
i = 0
#operatori = ['+','-', '*', '/', '=']
#zagrade = ['(',')']
#kljucneRijeci = ['za', 'az', 'od', 'do']
ulaz = []
izlaz = []
level = 0

err = False #zastavica za error

for line in sys.stdin:
        line = line.rstrip()
        line = line.rstrip('\n') #makni spaces na pocetku i na kraju i oznaku za kraj retka
                    #citanje
        ulaz.append(line.split(" ")) #lista s clanovima tipa ['IDN', '1', 'a']

ulaz.append("zavrsni_znak")
#print(ulaz)

program() #pocetak
if not err:
        for redak in izlaz:
                print(redak)

                            
                                

                        
                
           









        
