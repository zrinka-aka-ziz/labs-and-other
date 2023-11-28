#LAB2 KUHARICA
#0036517187 iz 2021. god (prolazi autograder 2022 - dakle ostavljam nepromijenjenim)
#===============
import os
import sys


def resolve(c1, c2):
    #c1 i c2 su 2 tuplea
    c1_list=list(c1)
    c2_list=list(c2)
     
    for lit in c1_list:
        if lit[0]=="~":
            if lit[1:] in c2_list:
                c1_list.remove(lit)
                c2_list.remove(lit[1:])
                c = c1_list+c2_list
                return(tuple(set(c)))
        else:
            if "~"+lit in c2_list:
                c1_list.remove(lit)
                c2_list.remove("~"+lit)
                c = c1_list+c2_list
                return(tuple(set(c)))
    return 0

def priprema(start): #start je set
    clauses = set(start)
    removed = set()
    for clause in start:
        clauselist = list(clause)
       
        for lit in clauselist:
            if len(clauselist) > 1: #provjeri da nema tautologije
                if lit[0]=='~':
                    opp=lit[1:]
                    if opp in clauselist and lit in clauselist:
                        removed.add(clause)

                        
                else:
                    opp="~"+lit
                    if opp in clauselist and lit in clauselist:
                        removed.add(clause)

    clauses=clauses.difference(removed)            

        #ovo sve radi
            #provjera da c1 nije podskup od c2, tada maknemo c2
    
    clauselist=list(clauses)
    editlist=list(clauselist)
    clauses_final=set()
  #radi, vraca skup tupleova nakon provjere da je c1 podskup c2 i makne c2
    if len(clauses)>1:
        for c1 in clauselist:
            temp = list(clauselist)
            temp.remove(c1) # bez c1
            #print(temp)
            for c2 in temp:
                if set(c1).issubset(c2) and c2 in editlist and c1 in editlist:
                    editlist.remove(c2)
                    
        if editlist:
            for el in editlist:
                clauses_final.add(el) 
        return(clauses_final)
##        clauses_ret=set(clauses_final)
##        for clause in clauses_final:
##           
##            temp2 = set(clauses_final)
##            temp2.remove(clause)
##            if len(clause)==1:
##                used = False
##                #print(str(temp2))
##                for clause2 in temp2:
##                    
##                    if clause[0][0] == "~":
##                        #print(str(clause))
##                        
##                        if clause[0] in clause2 or clause[0][1:] in clause2:
##                            used = True
##                    else:
##                        if clause[0] in clause2 or "~"+clause[0] in clause2:
##                            used = True
##                    
##                if not used:
##                    clauses_ret.remove(clause)
##                    #print(str(clause))
##        return clauses_ret
    return clauses
    
def res_func(start, goal):
    #sos skup je negirani cilj i rezolvente
    #na pocetku makni sto mozes - podskupove i tautologije   
                            
    #nova rezolventa ide iz start skupa i sosa
    clauses = priprema(start)
    #print(str(start))
    sos = set()
    goal_real = set()
    goal_real.add(goal)
  
    goal_real=priprema(goal_real)

    goal=list(goal_real)[0]

    #negacija cilja
   
    for lit in goal:
        if lit[0]=='~':
            sos.add((lit[1:],))
        else:
            sos.add(("~"+lit,))

##    all_cl = sos.union(start)
##    all_cl=priprema(all_cl)
##    clauses=start.intersection(all_cl)
##    sos=sos.intersection(all_cl)
   
    br= 1
    for i in sos.union(clauses):
        iz=""
        for k in range(len(i)):
            if k < len(i)-1:
                iz=iz +i[k] + " v "
            else:
                iz=iz +i[k]
        print(str(br) +". "+iz)
        br+=1
    print("===============")
    visited=set()
    
    while (True):
        resolvents=set()
        clauses=priprema(clauses)
        sos=priprema(sos)
        
        
        for c1 in sos:
            for c2 in sos.union(clauses):
                #print(str(c1) +", " + str(c2))
                visiting1 = (c1, c2)
                visiting2 = (c2, c1)
                if visiting1 not in visited and visiting2 not in visited:
                    visited.add(visiting1)
                    c=resolve(c1, c2)
                    if c != 0 and c not in resolvents:
                        if len(c) == 0:
                            print(str(br) +". "+"NIL")
                            print("===============")
                            return True
                      
                        resolvents.add(c)
              
                        print(str(br) +". "+str(c) + " iz " +str(c1) +", " + str(c2))
                        #print(str(br) +". "+iz + " iz " +str(c1) +", " + str(c2))
                        br+=1
                        if len(c)==1:
                            
                            if c[0][0]=="~" and (c[0][1:],) in sos.union(clauses):
                                
                                print(str(br) +". "+"NIL")
                                print("===============")
                                return True
                            elif ("~"+c[0],) in sos.union(clauses):
                                print(str(br) +". "+"NIL")
                                print("===============")
                                return True
                        sos=sos.union(resolvents)
                #print(str(visited))
##            if resolvents:
##                    for res in resolvents:
##                        if len(res)==1:
##                            if res[0][0]=="~" and (res[0][1:],) in sos.union(clauses):
##                                print(str(br) +". "+"NIL")
##                                print("===============")
##                                return True
##                            elif ("~"+res[0],) in sos.union(clauses):
##                                print(str(br) +". "+"NIL")
##                                print("===============")
##                                return True
            #sos=sos.union(resolvents)
        if resolvents.issubset(clauses):
            return False
        clauses=clauses.union(resolvents)
##            
        
    #print(sos)
    

def parse_file(flag, clauses, commands):
    start = set()
    
    data = [line.rstrip('\n') for line in clauses.readlines() if not line.startswith('#')]
   #zadnji je cilj ako ne kaze drukcije
    #print(data)
    for i in range(len(data)):
        data[i]=data[i].lower()
        temp =()
        for k in data[i].split(" v "):
            temp += (k.strip(),)
        if i == len(data)-1:
            goal = temp #ciljni je zadnji
        else:
            start.add(temp)
    
    #start je set tupleova
    if flag == "res":
        
        if (res_func(start, goal)):
            print("[CONCLUSION]: {} is true".format(data[-1].lower()))
        else:
            print("[CONCLUSION]: {} is unknown".format(data[-1].lower()))
    if flag == "cook":
        start.add(goal)
        data2 = [line.rstrip('\n') for line in commands.readlines() if not line.startswith('#')]
        for j in data2: #idemo naredbu po naredbu
            j=j.lower()
            print("User's command: " + j)
            temp =()
            cmd = j[-1] #prvi clan je ?+-
            j = j[:-1] #makni ?+-
            for l in j.split(" v "):
                temp += (l.strip(),)

            if cmd== "?":

                 #cilj se dodaje u start, temp je novi goal
                
                if (res_func(start, temp)):
                    print("[CONCLUSION]: {} is true".format(j))
                else:
                    print("[CONCLUSION]: {} is unknown".format(j))
                print()
                
            elif cmd== "+":
                start.add(temp) 
                print("Added "+ j)
                print()
                
            elif cmd== "-":
                if temp in start:
                    start.remove(temp)
                    
                    print("Removed " + j)
                print()
       
        
         
#main
if len(sys.argv) > 1:
    if str(sys.argv[1])=='resolution':
        clauses = str(sys.argv[2])
        
        if not os.path.isfile(clauses):
            print('Wrong path input.')
            exit()
        clause_path = open(clauses, 'r', encoding="utf-8")
        parse_file('res', clause_path, 0)
    elif str(sys.argv[1])=='cooking':
        clauses = str(sys.argv[2])
        commands = str(sys.argv[3])
        
        if not os.path.isfile(clauses) or not os.path.isfile(commands):
            print('Wrong path input.')
            exit()
        clause_path = open(clauses, 'r', encoding="utf-8")
        command_path = open(commands, 'r', encoding="utf-8")
        parse_file('cook', clause_path, command_path)
    else:
        print("Wrong command.")
else:
    print("Wrong command.")





