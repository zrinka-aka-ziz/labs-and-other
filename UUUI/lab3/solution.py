#0036517187
#lab3 UUUI
#ID3 decision tree

import os
import sys
import math

#global checked

##class Node: #klasa cvorova, prvi je prazan root, nakon toga cvorovi su oblika feature=value npr weather=sunny 
##    def __init__(self, name, parent): #cvor ima ili djecu ili value
##        self.children = []
##        self.name = name
##        self.parent = parent
##        self.val = None
##    #def PrintTree(self):
##        #print(self.name)
##
##def printing(node, lvl): #kao node uvijek predati root, kao lvl nula
##   # print("usao u cvor: ")
##   # print(node.name)
##    if len(node.children) != 0:
##        
##        for child in node.children:
##            printing(child, lvl+1)
##    else:
##        branch = []
##        branch.append(node.val)
##        node1 = node
##        while node1.name != 'root':
##            branch.append(str(lvl)+":"+node1.name)
##            lvl -= 1
##            node1=node1.parent
##        #branches.append(branch)
##        #print(branch[::-1])
##        
##        for elem in branch[::-1]:
##            print(elem, end=" ")
##        print("")

def D_xv(v, input_list): ##broji koliko ih ima vrijednost v u atributu x, v je npr sunny
    #print("XVXVXVXV")
    #print(v)
    #print(input_list)
    
    y_v = dict() #rjecnik koji sadrzi koliko ima yes koliko no koliko maybe itd.
    y_num = 0  #ukupni br npr dana kad je suncano
    for row in input_list:
        y_val = row[-1]
        #print("!!!!!!!!")
        #print(y_val)
        if y_val not in y_v.keys():
            #print("prvi if")
            y_v[y_val] = 0 #postavi npr no na nula
        if v in row: #moze biti yes, no, maybe, nesto trece
            #print("USAO U +1 ZA NUM")
            y_num += 1 #broji pojavu npr sunny, ako red sadrzi sunny dodaje 1
            if y_val not in y_v.keys():
                y_v[y_val] = 1
            else:
                current = y_v.get(y_val)
                current += 1
                y_v[y_val] = current
    #print(y_v)
    return y_v, y_num #radi
##
def E_D(y, y_num): #trazena znacajka npr sunny, (lista inputova,) dictionary s pobrojenim ishodima, uk br ishoda
    E_d = float(0) ##paziti na rubne slucajeve - ako su svi isti, E je 1, ako su svi 0 onda 0, ako samo jedan ima ishod onda 0
    #if v != None: #ako je v None, onda se radi entropija za cijelu tablicu
        
        #for key in y:
            
        #math.log2()

    #else:
    value_list = list(y.values())
    same = all(element == value_list[0] for element in value_list)
    if (same) and value_list[0] != 0: #rubni slucajevi
        E_d = float(1) #svi ishodi jednaki
    elif (same) and value_list[0] == 0:
        E_d = float(0) #svi ishodi 0
    else:
        for key in y:
            if y[key] != 0: #ako je vrijednost nula onda log2(0)=0 pa preskacemo
                p = float(y[key])/float(y_num)
                E_d += -1*(p * math.log2(p))
    return E_d

            
        
##
def D_count(input_list): 
    y = dict() #rjecnik koji sadrzi koliko ima yes koliko no koliko maybe itd.
    for row in input_list:
        y_val = row[-1] #moze biti yes, no, maybe, nesto trece
        if y_val not in y.keys():
            y[y_val] = 1
        else:
            current = y.get(y_val)
            current += 1
            y[y_val] = current
    y_num = len(input_list) #ukupni broj promatranih dana
    return y, y_num

def attr_check(header, input_list): #vraca dictionary sa setovima npr weather: {sunny, rainy, cloudy}
    attr=dict()
    for i in range(len(header)):
        vals = set()
        for row in input_list:
            vals.add(row[i])
##            if row[i] not in attr[header[i]]:
##                attr[header[i]].append(row[i])
        attr[header[i]]=vals
    return attr
                

def IG(E_d, input_list, header, x): #entropija skupa, train lista, popis x-eva, x
    Ig = E_d #- suma Sv/S*E_sv
    v_num = 0 #redni broj za znacajku
    for i in range(len(header)): #nadi koju znacajku gledamo [sunny, hot, low itd.]
        if header[i] == x:
            v_num = i
            break
    s = len(input_list)
    temp=dict() #rjecnik u kojem pise koliko dana je bilo suncano, koliko kisno itd ako je x weather
    for row in input_list:
        feat = row[v_num]
        if feat not in temp.keys():
                temp[feat] = 1
        else:
            current = temp.get(feat)
            current += 1
            temp[feat] = current
        
    for key in temp.keys():
        yx, yxnum = D_xv(key, input_list)
        Ig -= (float(temp[key])/float(s)) * E_D (yx, yxnum)
    return round(Ig, 4) #ovo round mozda makni, vidjet cemo
    

def table(header, input_list, attr, var): #tablica, header i input list s pocetka, var je trazena znacajka
    if var == None:
        return header, states

    header2=header.copy()
    
#def ID3(header, input_list, node, y, y_num, attr):
    
        
            
        
        
        
        

    
    
        
        
    
    



#main
if len(sys.argv) > 1:
    
    train_data = str(sys.argv[1])   
    if not os.path.isfile(train_data):
        print('Wrong path input.')
        exit()
    train_path = open(train_data, 'r', encoding="utf-8")
    train = [line.rstrip('\n') for line in train_path.readlines()]
    train_list=[]
    #train_dict=dict()
    for i in range(len(train)):
        train_list.append(train[i].split(','))
    header1 = train_list.pop(0)      #zaglavlje train dataseta
    last=header1[-1]
    header1.remove(last)
   # print(header1)
##    for j in range len(train_list):
##        if j == 0: #prazne liste kao value za svaku znacajku
##            for k in range len(train_list[0]):
##                train_dict[train_list[0][k]]=[]
##        else:
##            for h in range len(train_list[0]):
                
#lista listi po redovima, 0. red je header
    test_data = str(sys.argv[2])    
    if not os.path.isfile(test_data):
        print('Wrong path input.')
        exit()
    test_path = open(test_data, 'r', encoding="utf-8")
    test = [line.rstrip('\n') for line in test_path.readlines()]

    test_list=[]
    #test_dict=dict()
    for i in range(len(test)):
        test_list.append(test[i].split(','))
    header2 = test_list.pop(0) #zaglavlje test dataseta
##    print("Train: ")
##    print(header1)
##    print(train_list)
##    print("Test: ")
##    print(header2)
##    print(test_list)
    if len(sys.argv) > 3:
        depth_limit = int(sys.argv[3])
        #if not isinstance(depth_limit, int):
            #print("Depth limit must be an integer.")
            #exit()
##        print(depth_limit)


    #####################################################
    y, y_num =D_count(train_list) #radi, vraca rjecnik u kojem je izbrojen broj yes/no/maybe...
    print(y)
    print(y_num)
    E_d = E_D(y, y_num)
    print(E_d)

 ##ovo sve radi
    print()
    x='weather'
    ig_we = IG(E_d, train_list, header1, x)
    print(x)
    print(ig_we)

    x='humidity'
    ig_hu = IG(E_d, train_list, header1, x)
    print(x)
    print(ig_hu)

    x='wind'
    ig_wi = IG(E_d, train_list, header1, x)
    print(x)
    print(ig_wi)

    x='temperature'
    ig_te = IG(E_d, train_list, header1, x)
    print(x)
    print(ig_te)
    #print("!!!!!!!!")
    yv, ynum = D_xv('rainy', train_list)
    print(yv)
    print(ynum)
    E_d = E_D(yv, ynum)
    print(E_d)

    
else:
    print("Wrong command.")


#init za ID3 i stable od Nodes
#root = Node('root', None) #pocetni/prazni root
y, y_num =D_count(train_list) #pocetni rjecnik s yes/no/... i brojem ukupno dana
attr = attr_check(header1, train_list)
print(attr)
#ID3(header1, train_list, root, y, y_num, attr)
#print("[BRANCHES]:")
#printing(root, 0)

