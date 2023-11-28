#LAB4
#0036517187
import argparse
import sys
import os
import numpy as np
import random
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def errorCalc(expected, given):
    N = expected.size
    suma = 0
    for j in range(expected.size):
        diff = expected[j]-given[j]
        s = math.pow(diff, 2)
        suma += s
    return suma/N

def fitProSelection(population):
    #populacija je lista jedinski uzlazno sortirana po erroru, zadnji element ima najveci error
    
    maximum = sum([net.fitness for net in population])
    selection_prob = [net.fitness/maximum for net in population]
    
    return population[np.random.choice(len(population), p=selection_prob)]    #vraca neku jedinku/neku mrezu


def mutate(net, p, K):
    #mutiraj tezine
    
    for i in range(len(net.weights1)): 
        for j in range(len(net.weights1[i])):
            px = np.random.uniform(0, 1)
            if px <= p: #mutira
                #print("mutated w1")
                gau = np.random.normal(0, K)
                value=net.weights1[i][j]
                value += gau
                net.weights1[i][j]=value
    for i in range(len(net.weights2)): 
        for j in range(len(net.weights2[i])):
            px = np.random.uniform(0, 1)
            if px <= p: #mutira
                #print("mutated w2")
                gau = np.random.normal(0, K)
                value=net.weights2[i][j]
                value += gau
                net.weights2[i][j]=value
                
    for i in range(len(net.bias1)): 
        for j in range(len(net.bias1[i])):
            px = np.random.uniform(0, 1)
            if px <= p: #mutira
                #print("mutated b1")
                gau = np.random.normal(0, K)
                value=net.bias1[i][j]
                value += gau
                net.bias1[i][j]=value
    for i in range(len(net.bias2)): 
        for j in range(len(net.bias2[i])):
            px = np.random.uniform(0, 1)
            if px <= p: #mutira
                #print("mutated b2")
                gau = np.random.normal(0, K)
                value=net.bias2[i][j]
                value += gau
                net.bias2[i][j]=value

                
    if hasattr(net, 'weights3'):
        for i in range(len(net.weights3)): 
            for j in range(len(net.weights3[i])):
                px = np.random.uniform(0, 1)
                if px <= p: #mutira
                    #print("mutated w3")
                    gau = np.random.normal(0, K)
                    value=net.weights3[i][j]
                    value += gau
                    net.weights3[i][j]=value
        for i in range(len(net.bias3)):
            for j in range(len(net.bias3[i])):
                px = np.random.uniform(0, 1)
                if px <= p: #mutira
                    #print("mutated b3")
                    gau = np.random.normal(0, K)
                    value=net.bias3[i][j]
                    value += gau
                    net.bias3[i][j]=value
   
        
                    
    #mutiraj pragove
    
##                


def geneticAlg(x_train, y_train, x_test, y_test, config, popsize, elitism, p, K, iternum):
    population =[]
    if config != "5s5s":
        num = config[:-1] #makni s
        num=int(num)
    #print(num)
        for i in range(popsize):
            mreza = NeuralNetwork1L(x_train, y_train, num)
            population.append(mreza)
    else:
        for i in range(popsize):
            mreza = NeuralNetwork2L(x_train, y_train)
            population.append(mreza)

 
    for i in range(iternum): #idemo od 0 do 1999 za prvi krug
        
        #eval-odredi fitness na kraju petlje kada dobijes nove weights
        #sort po fitnessu
        population.sort(key=lambda x: x.err, reverse=False) #radi, prvi clan je najmanje error - najbolji fitness
        m = math.ceil(population[-1].err)
       # print(len(population))
        fitness_list=[]
        for k in range(popsize):
            fit = m - population[k].err
            fitness_list.append(fit) #radi
            population[k].fitness = fit
##        fitness_list = [math.ceil(population[-1].err) - population[k].err for k in range(popsize)]
##        for r in range(len(fitness_list)):
##            population[r].fitness=fitness_list[r]
        it = i
        if ((it+1)%2000 == 0):
            print("[Train error @"+str(it+1)+"]: "+str(population[0].err)) #+najbolji fitness u gen
        new_gen = []
        if elitism != 0:
            for i in range(elitism):
                new_gen.append(population[i])
        for i in range(popsize-elitism):
            #odaberi 2 roditelja
            r1 = fitProSelection(population)
            r2 = fitProSelection(population)
            while r1.fitness == r2.fitness: #ako su dva ista roditelja, izaberi novog
                r2 = fitProSelection(population)
            #krizaj roditelje kao aritm sredinu i napravi dijete
            if config != "5s5s":
                num = config[:-1] #makni s
                num=int(num)
                child = NeuralNetwork1L(x_train, y_train, num)
                #roditelji imaju 2 weights i 2 biasa
                child.weights1 = (r1.weights1+r2.weights1)/2
                child.weights2 = (r1.weights2+r2.weights2)/2
                child.bias1 = (r1.bias1+r2.bias1)/2
                child.bias2 = (r1.bias2+r2.bias2)/2
                child.weights = [child.weights1, child.weights2]
                child.bias = [child.bias1, child.bias2]
                
            else:
                child = NeuralNetwork2L(x_train, y_train)
                child.weights1 = (r1.weights1+r2.weights1)/2
                child.weights2 = (r1.weights2+r2.weights2)/2
                child.weights3 = (r1.weights3+r2.weights3)/2
                child.bias1 = (r1.bias1+r2.bias1)/2
                child.bias2 = (r1.bias2+r2.bias2)/2
                child.bias3 = (r1.bias3+r2.bias3)/2
                child.weights = [child.weights1, child.weights2, child.weights3]
                child.bias = [child.bias1, child.bias2, child.bias3]

            if p != 0:
                mutate(child, p, K)

            child.forwardFeed()
            child.err = errorCalc(child.y, child.output)
            new_gen.append(child)
            
            #ubaci dijete u novu generaciju
       
        population = new_gen
##    #napravi test
    for jedinka in population:
        jedinka.input = np.array(x_test)
        jedinka.y = np.array(y_test)
        jedinka.forwardFeed()
        jedinka.err = errorCalc(jedinka.y, jedinka.output)
    population.sort(key=lambda x: x.err, reverse=False)
    print("[Test error]: "+str(population[0].err))

  
    

class NeuralNetwork1L():
    def __init__(self, x, y, num): #num je 5 ili 20 ili sto vec
        self.input = np.array(x) #lista od listi x-eva
        self.input_size = len(x[0]) #koliko imamo x-eva
        self.weights1 = np.random.normal(0, 0.01, size=(self.input_size, num))
        self.weights2 = np.random.normal(0, 0.01, size=(num, 1))
        self.bias1 = np.random.normal(0, 0.01, size=(1, num)) #vektor, treba bit dim 5/20 itd.
        self.bias2 = np.random.normal(0, 0.01, size=(1, 1)) #bias na izlazu je samo jedan
        self.y = np.array(y)
        
        self.output = np.zeros(self.y.shape) #lista y koja ce se koristiti za err racun
        
        
        self.weights = [self.weights1, self.weights2]
        self.bias = [self.bias1, self.bias2]
        
        self.fitness = None
        self.forwardFeed()
        self.err = errorCalc(self.y, self.output)
        
    def forwardFeed(self):
        
        sigmoid_vectorized = np.vectorize(sigmoid)
       
        for i in range(self.output.size):
            layer1 = sigmoid_vectorized(np.dot(self.input[i], self.weights1) + self.bias1) #pozovi sigmoidu nad svakim izlazom neurona
            
            self.output[i] = np.dot(layer1, self.weights2) + self.bias2
        
        


class NeuralNetwork2L():
    def __init__(self, x, y): #5s5s
        self.input = np.array(x) #lista od listi x-eva
        self.input_size = len(x[0]) #koliko imamo x-eva
        self.weights1 = np.random.normal(0, 0.01, size=(self.input_size, 5))
        self.weights2 = np.random.normal(0, 0.01, size=(5, 5))
        self.weights3 = np.random.normal(0, 0.01, size=(5, 1))
        self.bias1 = np.random.normal(0, 0.01, size=(1, 5)) #vektor, treba bit dim 5 
        self.bias2 = np.random.normal(0, 0.01, size=(1, 5)) 
        self.bias3 = np.random.normal(0, 0.01, size=(1, 1))#bias na izlazu je samo jedan
        self.y = np.array(y)
        
        self.output = np.zeros(self.y.shape) #lista y koja ce se koristiti za err racun
        
    
        self.weights = [self.weights1, self.weights2, self.weights3]
        self.bias = [self.bias1, self.bias2, self.bias3]
        self.fitness = None
        self.forwardFeed()
        self.err = errorCalc(self.y, self.output)
        

    def forwardFeed(self):
        #print("num =" + str(self.num))
        sigmoid_vectorized = np.vectorize(sigmoid)
        for i in range(self.output.size):
            layer1 = sigmoid_vectorized(np.dot(self.input[i], self.weights1) + self.bias1) #pozovi sigmoidu nad svakim izlazom neurona, npr 12x25 matrice
            layer2 = sigmoid_vectorized(np.dot(layer1[0], self.weights2) + self.bias2) #layer 1 je atrica 1x5, spremljena kao vektor u vektoru
            #print(layer1)
            self.output[i] = np.dot(layer2, self.weights3) + self.bias3
       



#main
my_parser = argparse.ArgumentParser()

my_parser.add_argument('--train', help='path to train file')
my_parser.add_argument('--test', help='path to test file')
my_parser.add_argument('--nn', help='neural network architecture - can be in form of ns where n is a natural number or 5s5s')
my_parser.add_argument('--popsize', help='population size')
my_parser.add_argument('--elitism', help='number of elite specimens')
my_parser.add_argument('--p', help='mutation probability')
my_parser.add_argument('--K', help='stddev Gauss')
my_parser.add_argument('--iter', help='number of iterations for genetic algorithm')


args = my_parser.parse_args()
#print(vars(args))


if args.train != None:
    train_path = open(args.train, 'r', encoding="utf-8")
    train = [line.rstrip('\n') for line in train_path.readlines()]
    train_list=[]
    #train_dict=dict()
    for i in range(len(train)):
        train_list.append(train[i].split(','))
    header1 = train_list.pop(0)      #zaglavlje train dataseta
    
    x_train=[] #dvije list jedna sa x vrijednostima a druga s y vrijednostim a
    y_train=[]
    for row in train_list:
        y_train.append(float(row.pop(-1)))
        temp=[]
        for i in row:
            i=float(i)
            temp.append(i)
        x_train.append(temp)

    
if args.test != None:
    test_path = open(args.test, 'r', encoding="utf-8")
    test = [line.rstrip('\n') for line in test_path.readlines()]

    test_list=[]
    #test_dict=dict()
    for i in range(len(test)):
        test_list.append(test[i].split(','))
    header2 = test_list.pop(0)

    x_test=[] #dvije list jedna sa x vrijednostima a druga s y vrijednostim a
    y_test=[]
    for row in test_list:
        y_test.append(float(row.pop(-1)))
        temp=[]
        for i in row:
            i=float(i)
            temp.append(i)
        x_test.append(temp)

config = args.nn
geneticAlg(x_train, y_train, x_test, y_test, config, int(args.popsize), int(args.elitism), float(args.p), float(args.K), int(args.iter))
#mreza1=NeuralNetwork1L(x_train, y_train, 5)
#print(mreza1.err)
