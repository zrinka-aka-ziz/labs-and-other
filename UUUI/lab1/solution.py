import argparse
import os
import sys
from collections import deque
import heapq


## kod iz lab1 2021. Zrinka Pecanic 0036517187, prolazi sve testove za autograder 2022.
## stoga sam ga ostavila nepromijenjenog :)

def failed():
    print("[FOUND_SOLUTION]: no")
    return False
    
def path_check(elem):
    return path_check2('', elem)

def path_check2(path, elem):
    if elem[2] is not None:
        path += path_check2(path, elem[2]) + ' => ' #pozivanje rekurzivno dok se ne dode do pocetnog koji nema roditelja
    return path + elem[1] #na kraju se dodaje roditelj, vraca string


def bfs(start, goals, trans):
    
    start_state = (0.0, start, None) #pocetni tuple
    
    closed = set()
    openq = deque([start_state])
    
    while openq:
       
        n = openq.popleft()
        closed.add(n[1]) #dodavanje posjecenog elementa u closed
        if n[1] in goals:
            return n[0], len(closed), path_check(n)
        succ = trans.get(n[1])
        for s in succ: #stanja sljedbenici
            s =(n[0]+s[1], s[0], n)#(cijena, ime, roditelj) tuple
            if s[1] in closed: #ako je stanje posjeceno ne dodajemo ga na kraj reda
                continue
            openq.append(s) #dodavanje s desne strane
 
    return failed()
        
##
##
def ucs(start, goals, trans):
    
    start_state = (0.0, start, None) #pocetni tuple
    closed = set()
    openq = [start_state]
    prices = dict()
    prices[start_state[1]] = start_state[0]

    while openq:
        n = heapq.heappop(openq) #uzimanje elementa s heapa, uvijek uzima najmanji
        closed.add(n[1]) #dodavanje u closed

        if n[1] in goals:
            return n[0], len(closed), path_check(n)
        succ = trans.get(n[1])
        for s in succ:
            s =(n[0] + float(s[1]), s[0], n)
            if s[1] in closed:
                continue
            if s[1] not in prices.keys() or s[0] < prices.get(s[1]): #ako to stanje jos nije zapisano za provjeru cijene ili ako ima manju cijenu
                prices[s[1]] = s[0]
                heapq.heappush(openq, s)
    failed()
            

def astar(start, goals, trans, heur):
    start_state = (heur.get(start), start, None, 0.0) #pocetni tuple, nulti clan je procjena cijene puta
    closed = set()
    openq = [start_state]
    prices = dict()
    prices[start_state[1]] = start_state[3] #nula kao pocetna vrijednost puta

    while openq:
        n = heapq.heappop(openq) #uzimanje elementa s heapa
        closed.add(n[1]) #dodavanje u closed

        if n[1] in goals:
            return n[3], len(closed), path_check(n)
        succ = trans.get(n[1])
        
        for s in succ:
            s =(n[3] + float(s[1]) + heur.get(s[0]), s[0], n, n[3] + float(s[1])) #(procjena cijene puta, ime, roditelj, stvarna cijena dosadasnjeg puta)
            if s[1] in closed:
                continue
            if s[1] not in prices.keys() or s[3] < prices.get(s[1]): #ako to stanje jos nije zapisano za provjeru cijene ili ako ima manju cijenu
                prices[s[1]] = s[3]
                heapq.heappush(openq, (max(n[0], s[0]), s[1], n, s[3])) #f_max(f(parent), g+h))
    failed()


def optimistic(heur, trans, goals):
    print("# HEURISTIC-OPTIMISTIC {}".format(heurs))
    #checked = []
    cond = True
    for state in heur:
        #if state in checked:
            #continue
        #checked.append(state)
        result = ucs(state, goals, trans)
        if result != False:
            if heur.get(state) <= result[0]:
                print("[CONDITION]: [OK] h({}) <= h*: {} <= {}".format(state, heur.get(state), result[0]))
            else:
                cond = False
                print("[CONDITION]: [ERR] h({}) <= h*: {} <= {}".format(state, heur.get(state), result[0]))
    if cond:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")
    


def consistent(heur, trans):
    #checked = []
    #heapq.heapify(checked)
    cond = True
    print("# HEURISTIC-CONSISTENT {}".format(heurs))
    for s1 in trans:
        #if s1 in checked:
            #continue #ako smo to stanje obradili, da se ne vrtimo u krug
        for s2 in trans.get(s1):
            if not trans.get(s1).get(s2):
                break
            if heur.get(s1) <= heur.get(s2) + trans.get(s1).get(s2): #OK uvjet
                print("[CONDITION]: [OK] h({}) <= h({}) + c: {} <= {} + {}".format(s1, s2, heur.get(s1), heur.get(s2), trans.get(s1).get(s2)))
            else:
                cond = False
                print("[CONDITION]: [ERR] h({}) <= h({}) + c: {} <= {} + {}".format(s1, s2, heur.get(s1), heur.get(s2), trans.get(s1).get(s2)))
        #heapq.heappush(checked, s1)
        #checked.append(s1)
    if cond:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")
        
def h_file(file):
    data = [line.rstrip('\n') for line in file.readlines() if not line.startswith('#')]
    heur = dict()
    for j in data:
        heur[j.split(':')[0].strip()]=float(j.split(':')[1].strip()) #stavljanje u rjecnik heuristika
    return heur 

def ss_file(file):
    data = [line.rstrip('\n') for line in file.readlines() if not line.startswith('#')] #citanje cijelog fajla
    trans = dict()
    for k in data[2:]: #preskaci prve 2 stavke, pocetno stanje i ciljna stanja
        city_price = dict()
        k=k.split(':') #odvoji po dvotocki

        for i in k[1].strip().split():
            city_price.update({i.split(',')[0]: float(i.split(',')[1])})
            #dupli rjecnik
        trans.update({k[0]: city_price})
    #print(trans)
    #print(data[0].strip())
    #print(set(data[1].strip().split()))
    return data[0].strip(), set(data[1].strip().split()), trans
            

my_parser = argparse.ArgumentParser()

my_parser.add_argument('--alg', choices =['bfs', 'ucs', 'astar'], help='algorithm type')
my_parser.add_argument('--ss', help='path to state file')
my_parser.add_argument('--h', help='path to heuristics file')
my_parser.add_argument('--check-optimistic', action='store_true', help='check if heuristic is optimistic')
my_parser.add_argument('--check-consistent', action='store_true', help='check if heuristic is consistent')

args = my_parser.parse_args()
##print(vars(args))
##print(args.alg, args.ss, args.h, args.check_optimistic, args.check_consistent)

if args.ss != None:
    state_path = open(args.ss, 'r', encoding="utf-8")
    states= args.ss
    ss_tuple = ss_file(state_path)
if args.h != None:
    heur_path = open(args.h, 'r', encoding="utf-8")
    heurs=args.h
    heur = h_file(heur_path)
algtype = args.alg
opt = args.check_optimistic
cons = args.check_consistent

if ss_tuple:
    trans = ss_tuple[2]
    #print(trans)#
    #print()#




    trans_list=dict() #u trans je rjecnik unutar rjecnika, u trans list je
#rjecnik unutar kojih je lista tupleova gdje je nulti ime stanja a prvi cijena, treba nam za sortiranje za bfs

    for key in trans:
        temp = sorted(trans.get(key).items())
        trans_list[key]=temp
    #print(trans_list)#
    
if cons and ss_tuple and heur:
    consistent(heur, trans)
elif opt and ss_tuple and heur:
    optimistic(heur, trans_list, ss_tuple[1])
    
if algtype:
    if ss_tuple:
        if algtype == "bfs":
            print("# BFS")
            x=bfs(ss_tuple[0], ss_tuple[1], trans_list)
        elif algtype == "ucs":
            print("# UCS")
            x=ucs(ss_tuple[0], ss_tuple[1], trans_list)
        elif algtype == "astar" and heur:
            print("# A-STAR {}".format(heurs))
            x=astar(ss_tuple[0], ss_tuple[1], trans_list, heur)
        if x != False or x!= None:
            print("[FOUND_SOLUTION]: yes")
            print("[STATES_VISITED]: {}".format(x[1]))
            print("[PATH_LENGTH]: {}".format(len(x[2].split(' => '))))
            print("[TOTAL_COST]: {}".format(x[0]))
            print("[PATH]: {}".format(x[2]))
    


