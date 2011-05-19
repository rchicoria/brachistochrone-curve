"""
sga_b_2011.py
Simple Genetic Algorithm for the problem "Me think it is like a weasel".
Ernesto Costa, April, 2011.
"""

from random import choice, sample, randint,random
from operator import itemgetter

def create_indiv(size,alphabet):
    indiv = [choice(alphabet) for i in range(size)]
    indiv = ''.join(indiv)
    return [indiv,0]

def create_population(size_pop, size_indiv,alphabet):
    pop = [create_indiv(size_indiv, alphabet) for i in range(size_pop)]
    return pop

def sga(numb_genera,size_pop,alphabet,target,sel_parents, fit_function,
        mutation, sel_survivors, size_tournament, prob_crossover, prob_mutation, size_elite):
    # create initial population
    count_mutation = 0
    count_crossover = 0
    population = create_population(size_pop,len(target),alphabet)
    # evaluate population
    population = [[indiv[0], fitness_indiv(indiv[0], target)] for indiv in population]
    for generation in range(numb_genera):
        # Select parents
        parents = [tournament_selection(population, size_tournament) for i in range(size_pop)]
        # Produce offspring
        # a) crossover
        offspring = []
        for i in range(0,size_pop,2): # population must have an even size...
            if random() < prob_crossover:
                offspring.extend(one_point_crossover(parents[i],parents[i+1]))
                count_crossover += 2
            else:
                offspring.extend([parents[i],parents[i+1]])
        # b) mutation
        for j in range(size_pop):
            if random() < prob_mutation:
                offspring[j] = mutation(offspring[j],alphabet)
                count_mutation += 1
        # Evaluate offspring
        offspring = [[indiv[0], fitness_indiv(indiv[0], target)] for indiv in offspring] 
        offspring.sort(key = itemgetter(1))
        # Select Survivors
        population = sel_survivors(population,offspring, size_elite)
        # show best
        population.sort(key=itemgetter(1))
        print "Generation: %d\tindividual: %s\tfitness: %f" % (generation,population[0][0],population[0][1]) 
    # Choose best
    print "BEST: %s\tfitness: %f" % (population[0][0],population[0][1]) 
    print 'Crossovers:%d\tMutations:%d' % (count_crossover,count_mutation)
    return True

# Basic mechanisms and operators
def tournament_selection(population, size_tournament):
    tournament = sample(population,size_tournament)
    tournament.sort(key=itemgetter(1)) # minimization
    return tournament[0]

def elitism_selection(parents, offspring, size_elite):
    size = int(len(parents) * size_elite)
    new_pop = parents[:size] + offspring[:len(parents) - size]
    new_pop.sort(key=itemgetter(1))
    return new_pop

def fitness_indiv(indiv, target):
    indiv.upper()
    value = sum([1 for i in range(len(indiv)) if indiv[i] != target[i]])
    return value

def mutation(indiv,alphabet):
    cromo = indiv[0]
    index = choice(range(len(cromo)))
    new_gene = choice(alphabet)
    while new_gene == cromo[index]:
        new_gene = choice(alphabet)      
    new_cromo = cromo[:index] + new_gene + cromo[index + 1:]
    return [new_cromo,0]
                   
def one_point_crossover(parent_1, parent_2):
    cross_point = choice(range(len(parent_1)))
    offspring_1 = parent_1[:cross_point] + parent_2[cross_point:]
    offspring_2 = parent_2[:cross_point] + parent_1[cross_point:]  
    return [offspring_1,offspring_2]



    
if __name__ == '__main__':
    target ="GRAO A GRAO ENCHE A GALINHA O PAPO!"
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .!?:;'
    print sga(1000,50,alphabet,target, tournament_selection, fitness_indiv,mutation,elitism_selection,3,0.8,0.1,0.3)
    