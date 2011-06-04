"""
Made by:

Gustavo Fernandes
Joao Duro
Joao Lopes
"""

from BrachFitness import *
from plotLib import *
from random import randrange, sample, randint, random, choice
from operator import itemgetter
from math import sqrt
import os;

def test_curve():
    solucao_A= [1,2,2,1,3,0,4,1.5]
    solucao_B = [1,1,2,2,3,1,4,1.5]
    
    addCurve(solucao_A)
    addCurve(solucao_B)
    
    showCurves()


def createIndiv(begin_end_points, size, fitnessFunc):
    x1 = begin_end_points[0]
    y1 = begin_end_points[1]
    x2 = begin_end_points[2]
    y2 = begin_end_points[3]
    
    fit = -1
    while fit == -1:
	indiv = [[x1, y1]]
	x = []
	for i in range(1, size-1):
	    x_temp = randrange(x1, x2)
	    while (x_temp in x):
		x_temp = randrange(x1, x2)
	    x.append(x_temp)
	    indiv.append([x_temp, randrange(0, y1)])
	
	indiv.append([x2, y2])
	indiv.sort(key=itemgetter(0))
	indiv_final = []
	for i in indiv:
	    indiv_final.append(i[0])
	    indiv_final.append(i[1])
	#print 'len',len(indiv)
	fit = fitnessFunc(indiv_final)
    return [indiv_final, fit]


def createPop(begin_end_points, sizeIndiv, sizePop, fitnessFunc):
    pop = [createIndiv(begin_end_points, sizeIndiv, fitnessFunc) for i in range(sizePop)]
    return pop


"""
Tournament Selection Function
fucntion Args: [tournamentSize]
"""
def tournamentSelection(population, size, functionArgs):
    selection = []
    #print functionArgs
    for i in range(size):
        tournament = sample(population, functionArgs[0])
        tournament.sort(key=itemgetter(1))
        selection.append(tournament[0])
        
    return selection

"""
Roulette Selection Function
fucntion Args: []
"""
def rouletteSelection(population, size, functionArgs):
    total=0.0
    for i in population:
	total+=1.0/i[1]
    portion=[]
    for i in range(len(population)):
	if(i!=0):
	    portion.append((1.0/population[i][1])/total+portion[i-1])
	else:
	    portion.append((1.0/population[i][1])/total)
    selection=[]
    for i in range(0,size):
	rand=random()
	for p in range(len(portion)):
	    if(portion[p]>rand):
		selection.append(population[p])
		break
    return selection

def elitismSelection(parents, offspring, size_elite):
    size = int(len(parents) * size_elite)
    new_pop = parents[:size] + offspring[:len(parents) - size]
    new_pop.sort(key=itemgetter(1))
    return new_pop


def n_point_crossover(parent_1,parent_2,n):
    cross_points = [choice(range(1, (len(parent_1[0])/2-1))) for i in range(n)]
    cross_points.append(0)
    cross_points.append(len(parent_1[0])/2)
    cross_points.sort()
    
    #print cross_points
    
    offspring_1 = []
    offspring_2 = []
    for i in range((n+2)-1):
	
	if (i % 2) == 0:	    
	    offspring_1.extend(parent_1[0][cross_points[i]*2:cross_points[i+1]*2])
	    offspring_2.extend(parent_2[0][cross_points[i]*2:cross_points[i+1]*2])
	else:
	    offspring_1.extend(parent_2[0][cross_points[i]*2:cross_points[i+1]*2])
	    offspring_2.extend(parent_1[0][cross_points[i]*2:cross_points[i+1]*2])

    """
    print "##################################"
    print parent_1
    print parent_2
    print [offspring_1,0]
    print [offspring_2,0]
    print "##################################"
    """
	
    return [[offspring_1,0],[offspring_2, 0]]

def mutation(indiv, size_mutation, prob_mutation):
    cromo = indiv[0]
    
    new_cromo = indiv[:]
    
    for i in range(3, len(cromo)-2):
	if (random() < prob_mutation):
	    index = i
	    gene = cromo[index]
	    mute = randint(-size_mutation, size_mutation)
	    while mute == 0:
		mute = randint(-size_mutation, size_mutation)
	    new_gene = (cromo[index]+mute) % cromo[1]
	    new_cromo = cromo[:index]
	    new_cromo.append(new_gene)
	    new_cromo.extend(cromo[index + 1:])
    
    cromo_tmp = []
    for i in range(0, len(new_cromo), 2):
	cromo_tmp.append([new_cromo[i], new_cromo[i+1]])
    cromo_tmp.sort(key=itemgetter(0))
    new_cromo = []
    for i in cromo_tmp:
	new_cromo.append(i[0])
	new_cromo.append(i[1])
    return [new_cromo,0]

def elitism_selection(parents, offspring, size_elite):
    size = int(len(parents) * size_elite)
    new_pop = parents[:size] + offspring[:len(parents) - size]
    new_pop.sort(key=itemgetter(1))
    return new_pop

def average_fitness(population):
    sum_ = 0.0
    for i in population:
	sum_ = sum_ + i[1]
    return (sum_*1.0)/len(population)

def std_dev_fitness(population, average):
    sum_ = 0.0
    for i in population:
	sum_ = sum_ + (i[1] - average)**2
    return sqrt((1.0/(len(population)-1)) * sum_)


"""
Genetic Algorithms
"""
def GA(n_generations, sizePop, sizeIndiv, fitnessFunc,
       mutation, selection_parents, functionArgs, sel_survivors,numberPoints,
       prob_crossover,prob_mutation, size_elite, size_mutation, begin_end_points,f,expnumber,testnum):
    worst_fitness = []
    best_fitness = []
    avg_fitness = []
    std_fitness = []
    # create initial population
    population = createPop(begin_end_points, sizeIndiv, sizePop, fitnessFunc)
	
    #print "### Initial Population"
    #print population
    print n_generations
    for generation in range(n_generations):

        #print "Generation: ", generation
        
        # select parents
        parents = selection_parents(population, sizePop, functionArgs)
        #print "### Parents"
        #print parents
	
	# Recombination
	offspring = []
	for i in range(0,sizePop,2):
	    #print 'i=',i
	    if random() < prob_crossover:
		offspring.extend(n_point_crossover(parents[i],parents[i+1],numberPoints))
	    else:
		offspring.extend([parents[i],parents[i+1]])
		
	#print "### Offspring after crossover",offspring
	
	# Mutation
	for j in range(sizePop):
            offspring.append(mutation(parents[j], size_mutation, prob_mutation))
	
	# Evaluate Offspring
	offspring = [[indiv[0], fitnessFunc(indiv[0])] for indiv in offspring] 
        offspring.sort(key = itemgetter(1))
	
	# Eliminate invalid candidates
	i = 0
	while (i<len(offspring)):
	    if (offspring[i][1]<0):
		offspring.pop(i)
	    else:
		i = i + 1
	
	# Offspring Selection
	population = sel_survivors(population, offspring, size_elite)	

	best_fitness.append(population[0][1])
	worst_fitness.append(population[len(population)-1][1])
	avg = average_fitness(population)
	avg_fitness.append(avg)
	std_fitness.append(std_dev_fitness(population, avg))
	"""
	best=population[0]
	worst=population[len(population)-1]
	temp="\nGeneration Number - %d\n"%(generation)
	f.write(temp)
	#PRINT ON FILE
	f.write("\nBest Indiv\n")
	tmp=" ".join(map(str,best))
	f.write(tmp)
	f.write("\nWorst Indiv\n")
	tmp=" ".join(map(str,worst))
	f.write(tmp)
	"""
    
    path="files/test"+testnum+"/indiv%d.png"%(expnumber)
    addCurve(population[0][0])
    temp="Best Individ - Fitness: %f"%(population[0][1])
    addFigure(1,temp,"x Axis","y Axis")
    saveImage(path)
    clearPlot()

    return [avg_fitness, std_fitness, best_fitness, worst_fitness]
    
if __name__ == '__main__':
    # begin and end points [x, y, x2, y2]
    
    f_input = open('input.csv', 'r')
    f_output = open('output.csv','w')
    line = f_input.readline()
    while (line != ""):
	split = line.split(',')
	testnum = split[0]
	if testnum == '-':
	    print 'ignoring ',testnum
	    line = f.readline()
	    continue
	print 'test#: ',str(testnum)
	numeroGeracoes = int(split[1])
	tamanhoPopulacao = int(split[2])
	tamanhoIndividuo = int(split[3])
	#split[4] = "calcBrancTime"
	fitnessFunc="calcBrancTime"
	selecao = split[5]
	if selecao == 'Tournament':
	    selecFunc = tournamentSelection
	else:
	    selecFunc = rouletteSelection
	
	numeroPontos = int(split[6][:1])
	
	probRecombinacao = int(split[7][:2])/100.0
	
	#split[8] = "Gene a Gene"
	mutacao   = "Gene a Gene"

	probMutacao = float(split[9])
	tamanhoMutacao = int(split[10])
	#split[11] = ="Elitismo"
	selecaoSobreviventes="Elitismo"
	tamanhoElite = float(split[12])
	
	begin_end_points = []
	begin_end_points.append(int(split[13][2:]))
	begin_end_points.append(int(split[14][:-2]))
	begin_end_points.append(int(split[15][2:]))
	begin_end_points.append(int(split[16][:-2]))
	
	dirname = "files/test"+testnum
	if not os.path.isdir("./" + dirname + "/"):
	    os.mkdir("./" + dirname + "/")
	    
	tmp="Numero de Geracoes: %d\nTamanho da Populacao: %d\nTamanho do Individuo: %d\nFuncao de Fitness: %s\nAlgoritmo de Mutacao: %s\nAlgoritmo de Selecao: %s\nAlgoritmo de Recombinacao: %d-Points\nSelecao de Sobreviventes: %s\nProbabilidade de Recombinacao: %f\nProbabilidade de Mutacao: %f\nTamanho da Elite: %f\nTamanho da Mutacao: %f\nPonto Inicial (%d,%d)\nPonto Final (%d,%d)\n\n" %(numeroGeracoes,tamanhoPopulacao,tamanhoIndividuo,fitnessFunc,mutacao,selecao,numeroPontos,selecaoSobreviventes,probRecombinacao,probMutacao,tamanhoElite,tamanhoMutacao,begin_end_points[0],begin_end_points[1],begin_end_points[2],begin_end_points[3])
	
	"""
	GA(n_generations, sizePop, sizeIndiv, fitnessFunc,
	   mutation, selection_parents, functionArgs, sel_survivors,numberPoints,
	   prob_crossover,prob_mutation, size_elite, size_mutation, begin_end_points)
	"""
	
	
	f=open("files/test"+testnum+"/results.txt",'w')
	f.write(tmp)
	
	best_fitness=[0 for i in range(numeroGeracoes)]
	worst_fitness=[0 for i in range(numeroGeracoes)]
	avg_fitness=[0 for i in range(numeroGeracoes)]
	std_fitness=[0 for i in range(numeroGeracoes)]
	bestAverage=0
	worstAverage=0
	numeroTestes=30
	for i in range(numeroTestes):
	    temp="\nExperiment %d \n" % (i+1)
	    [avgFitness, stdFitness, bestFitness, worstFitness]=GA(numeroGeracoes, tamanhoPopulacao, tamanhoIndividuo, calcBrachTime,
		mutation, selecFunc, [3], elitism_selection, numeroPontos,
		probRecombinacao , probMutacao, tamanhoElite, tamanhoMutacao, begin_end_points,f,i,testnum)
		
	    best_fitness = [(best_fitness[i] + bestFitness[i]) for i in range(numeroGeracoes)]
	    worst_fitness = [(worst_fitness[i] + worstFitness[i]) for i in range(numeroGeracoes)]
	    avg_fitness = [(avg_fitness[i] + avgFitness[i]) for i in range(numeroGeracoes)]
	    std_fitness = [(std_fitness[i] + stdFitness[i]) for i in range(numeroGeracoes)]
	    
	    
	best_fitness = [(best_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
	worst_fitness = [(worst_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
	avg_fitness = [(avg_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
	std_fitness = [(std_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
	
	f.write("\nFitnesses:\n")
	
	f.write("\nBest Fitness:\n")
	tmp=" ".join(map(str,best_fitness))
	f.write(tmp)
	f.write("\nWorst Fitness:\n")
	tmp=" ".join(map(str,worst_fitness))
	f.write(tmp)
	f.write("\nAverage Fitness:\n")
	tmp=" ".join(map(str,avg_fitness))
	f.write(tmp)
	f.write("\nSTD Fitness:\n")
	tmp=" ".join(map(str,std_fitness))
	f.write(tmp)
	
	f.write("\nValues to Report (end generation):\n")
	f.write("Best Worst Avg stdev\n")
	tmp="%f %f %f %f\n\n"%(best_fitness[len(best_fitness)-1],worst_fitness[len(worst_fitness)-1],avg_fitness[len(avg_fitness)-1],std_fitness[len(std_fitness)-1])
	f.write(tmp)
	tmp="%f;%f;%f;%f\n"%(best_fitness[len(best_fitness)-1],worst_fitness[len(worst_fitness)-1],avg_fitness[len(avg_fitness)-1],std_fitness[len(std_fitness)-1])
	f_output.write(tmp)
	
	#SAVE GRAPHS
	path="files/test"+testnum+"/fitnesses.png"
	
	subplot(2, 1, 1)
	defAxis([0, numeroGeracoes, 0, 30])
	addCurveWithoutX(best_fitness)
	addCurveWithoutX(worst_fitness)
	addCurveWithoutX(avg_fitness)
	#figlegend("Best","Worst","Average")
	subplot(2, 1, 2)
	defAxis([0, numeroGeracoes, 0, 5])
	addCurveWithoutX(std_fitness)
	temp = "Fitness test " + (testnum)
	addFigure(1,temp)
	saveImage(path)
	
	clearPlot()
	
	f.close()
	
	line = f_input.readline()
    f_input.close()
    f_output.close()
    """
    testnum=str(48)
    begin_end_points = [0, 100, 100, 20]
    numeroGeracoes=300
    tamanhoPopulacao=200
    tamanhoIndividuo=40
    fitnessFunc="calcBrancTime"
    mutacao="Gene a Gene"
    selecao="Roulette"
    numeroPontos=3
    selecaoSobreviventes="Elitismo"
    probRecombinacao=0.7
    probMutacao=0.01
    tamanhoElite=0.3
    tamanhoMutacao=10
    """
    """
    dirname = "files/test"+testnum
    if not os.path.isdir("./" + dirname + "/"):
	os.mkdir("./" + dirname + "/")
	
    tmp="Numero de Geracoes: %d\nTamanho da Populacao: %d\nTamanho do Individuo: %d\nFuncao de Fitness: %s\nAlgoritmo de Mutacao: %s\nAlgoritmo de Selecao: %s\nAlgoritmo de Recombinacao: %d-Points\nSelecao de Sobreviventes: %s\nProbabilidade de Recombinacao: %f\nProbabilidade de Mutacao: %f\nTamanho da Elite: %f\nTamanho da Mutacao: %f\nPonto Inicial (%d,%d)\nPonto Final (%d,%d)\n\n" %(numeroGeracoes,tamanhoPopulacao,tamanhoIndividuo,fitnessFunc,mutacao,selecao,numeroPontos,selecaoSobreviventes,probRecombinacao,probMutacao,tamanhoElite,tamanhoMutacao,begin_end_points[0],begin_end_points[1],begin_end_points[2],begin_end_points[3])
    
    ""
    GA(n_generations, sizePop, sizeIndiv, fitnessFunc,
       mutation, selection_parents, functionArgs, sel_survivors,numberPoints,
       prob_crossover,prob_mutation, size_elite, size_mutation, begin_end_points)
    ""
    
    
    f=open("files/test"+testnum+"/results.txt",'w')
    f.write(tmp)
    
    best_fitness=[0 for i in range(numeroGeracoes)]
    worst_fitness=[0 for i in range(numeroGeracoes)]
    avg_fitness=[0 for i in range(numeroGeracoes)]
    std_fitness=[0 for i in range(numeroGeracoes)]
    bestAverage=0
    worstAverage=0
    numeroTestes=30
    for i in range(numeroTestes):
	temp="\nExperiment %d \n" % (i+1)
	[avgFitness, stdFitness, bestFitness, worstFitness]=GA(numeroGeracoes, tamanhoPopulacao, tamanhoIndividuo, calcBrachTime,
	    mutation, selecFunc, [3], elitism_selection, numeroPontos,
	    probRecombinacao , probMutacao, tamanhoElite, tamanhoMutacao, begin_end_points,f,i,testnum)
	    
	best_fitness = [(best_fitness[i] + bestFitness[i]) for i in range(numeroGeracoes)]
	worst_fitness = [(worst_fitness[i] + worstFitness[i]) for i in range(numeroGeracoes)]
	avg_fitness = [(avg_fitness[i] + avgFitness[i]) for i in range(numeroGeracoes)]
	std_fitness = [(std_fitness[i] + stdFitness[i]) for i in range(numeroGeracoes)]
	
	
    best_fitness = [(best_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
    worst_fitness = [(worst_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
    avg_fitness = [(avg_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
    std_fitness = [(std_fitness[i]/numeroTestes) for i in range(numeroGeracoes)]
    
    f.write("\nFitnesses:\n")
    
    f.write("\nBest Fitness:\n")
    tmp=" ".join(map(str,best_fitness))
    f.write(tmp)
    f.write("\nWorst Fitness:\n")
    tmp=" ".join(map(str,worst_fitness))
    f.write(tmp)
    f.write("\nAverage Fitness:\n")
    tmp=" ".join(map(str,avg_fitness))
    f.write(tmp)
    f.write("\nSTD Fitness:\n")
    tmp=" ".join(map(str,std_fitness))
    f.write(tmp)
    
    f.write("\nValues to Report (end generation):\n")
    f.write("Best Worst Avg stdev\n")
    tmp="%f %f %f %f\n\n"%(best_fitness[len(best_fitness)-1],worst_fitness[len(worst_fitness)-1],avg_fitness[len(avg_fitness)-1],std_fitness[len(std_fitness)-1])
    f.write(tmp)
    
    #SAVE GRAPHS
    path="files/test"+testnum+"/fitnesses.png"
    
    subplot(2, 1, 1)
    defAxis([0, numeroGeracoes, 0, 30])
    addCurveWithoutX(best_fitness)
    addCurveWithoutX(worst_fitness)
    addCurveWithoutX(avg_fitness)
    #figlegend("Best","Worst","Average")
    subplot(2, 1, 2)
    defAxis([0, numeroGeracoes, 0, 5])
    addCurveWithoutX(std_fitness)
    temp = "Fitness test " + (testnum)
    addFigure(1,temp)
    saveImage(path)
    
    clearPlot()
    
    f.close()
    
    ""
    temp='\n Average Fitness: %f'%(average[len(average)-1])
    f.write(temp)
    temp='\n Standart Deviation: %f'%(stddev)
    f.write(temp)
    f.close()
    ""
    """
    
