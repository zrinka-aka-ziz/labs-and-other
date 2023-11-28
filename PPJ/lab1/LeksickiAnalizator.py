import sys

brojacRedaka = 0
operatori =['+','-', '*', '/', '=']
zagrade=['(',')']
kljucneRijeci=['za', 'az', 'od', 'do']


for l in sys.stdin:
    brojacRedaka += 1 #na pocetku uvijek uvecaj broj redaka
    l = l.lstrip()
    l = l.rstrip('\n') #makni spaces na pocetku i na kraju i oznaku za kraj retka
                    #citanje
    line = l
    endLine = False
                
    while not endLine:
                      
            if not line:
                    endLine = True 
            elif line[0] == " ": #preskoci space
                                
                    line = line.lstrip()#line[:0] + line[1:]
                               
            elif line[0] == '\t': #preskoci tab
                    line = line[1:]       
            elif line[:1].isdigit():
                    stopBr = False
                    broj = line[:1]
                    line = line[1:]
                    while not stopBr: #dok god vidiš brojeve spremaj ih u string
                            if line[:1].isdigit():
                                    broj += line[:1]
                                    line = line[1:] #iduci znak
                            else:
                                    stopBr = True #gotovo citanje broja
                                                
                    print('BROJ ', end="")
                    print(brojacRedaka, end=" ")
                    print(broj)     
                                        
                        

            elif line[:1].isalpha(): #ako je slovo
                   if len(line)>=3 and not line[:3].isalpha() and line[:2] in kljucneRijeci and not line[:3][2].isdigit() or len(line)== 2 and line[:2] in kljucneRijeci: #ako je kljucna rijec
                            if line[:2] =='za':
                                    print('KR_ZA ', end="")
                                    print(brojacRedaka, end=" ")
                                    print(line[:2])
                                    line = line[2:]
                            elif line[:2] =='az':
                                    print('KR_AZ ', end="")
                                    print(brojacRedaka, end=" ")
                                    print(line[:2])
                                    line = line[2:]
                            elif line[:2] =='od':
                                    print('KR_OD ', end="")
                                    print(brojacRedaka, end=" ")
                                    print(line[:2])
                                    line = line[2:]
                            else:
                                    print('KR_DO ', end="")
                                    print(brojacRedaka, end=" ")
                                    print(line[:2])
                                    line = line[2:]

                   else: #ako nije kljucna rijec a pocinje slovom, onda je idn
                            stopLoad = False
                            idn =  line[:1]
                            line = line[1:]
                            while not stopLoad:
                                    if line[:1].isdigit() or line[:1].isalpha(): #ako je iduci znak broj ili slovo onda jos uvijek spada u idn
                                            idn += line[:1]
                                            line = line[1:] #iduci znak
                                    else:
                                            stopLoad = True #gotovo citanje idn-a
                                                        
                            print('IDN ', end="")
                            print(brojacRedaka, end=" ")
                            print(idn)
                                        
                                        
                                

            else:
                    if line[:2] == "//": #ako naides na komentar prijedi na iducu liniju
                            endLine = True
                                        
                    else: #moze biti operator ili zagrada
                                       
                            if line[:1] in operatori:
                                              
                                    if line[:1] == '=':
                                            print('OP_PRIDRUZI ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                                    elif line[:1] == '-':
                                            print('OP_MINUS ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                                    elif line[:1] == '+':
                                            print('OP_PLUS ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                                    elif line[:1] == '/':
                                            print('OP_DIJELI ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                                    else:
                                            print('OP_PUTA ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                                                
                            if line[:1] in zagrade:
                                    if line[:1] == '(':
                                            print('L_ZAGRADA ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                                    else:
                                            print('D_ZAGRADA ', end="")
                                            print(brojacRedaka, end=" ")
                                            print(line[:1])
                                            line = line[1:]
                            
                                
