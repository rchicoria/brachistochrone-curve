"""
sga_2011.py
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

def sga(numb_genera,size_pop, size_indiv, alphabet, sel_parents, fit_function,
        mutation, sel_survivors, size_tournament, prob_mutation, size_elite, size_mutation):
    # create initial population
    population = create_population(size_pop,size_indiv,alphabet)
    # evaluate population
    population = [[indiv[0], fitness_indiv(indiv[0], fit_function)] for indiv in population]
    for generation in range(numb_genera):
        # Select parents
        parents = [tournament_selection(population, size_tournament) for i in range(size_pop)]
        # Produce offspring
        offspring = []
        for j in range(size_pop):
            if random() < prob_mutation:
                offspring.append(mutation(parents[i],alphabet,size_mutation))
            else:
                offspring.append(parents[i])
        # Evaluate offspring
        offspring = [[indiv[0], fitness_indiv(indiv[0], fit_function)] for indiv in offspring] 
        offspring.sort(key = itemgetter(1))
        # Select Survivors
        population = sel_survivors(population,offspring, size_elite)
        # show best
        population.sort(key=itemgetter(1))
        print "Generation: %d\tindividual: %s\tfitness: %f" % (generation,population[0][0],population[0][1]) 
    # Choose best
    print "BEST: %s\tfitness: %f" % (population[0][0],population[0][1])  
    return True

def tournament_selection(population, size_tournament):
    tournament = sample(population,size_tournament)
    tournament.sort(key=itemgetter(1)) # minimization
    return tournament[0]

def fitness_indiv(indiv, fit_function):
    return fit_function(indiv)

def elitism_selection(parents, offspring, size_elite):
    size = int(len(parents) * size_elite)
    new_pop = parents[:size] + offspring[:len(parents) - size]
    new_pop.sort(key=itemgetter(1))
    return new_pop

def fit_weasel(indiv):
    target="ME THINK IT IS LIKE A WEASEL."
    indiv.upper()
    value = sum([1 for i in range(len(indiv)) if indiv[i] != target[i]])
    return value

def mutation(indiv,alphabet, size_mutation):
    cromo = indiv[0]
    index = choice(range(len(cromo)))
    gene = cromo[index]
    mute = randint(-size_mutation, size_mutation)
    while mute == 0:
        mute = randint(-size_mutation, size_mutation)
    index_alpha = alphabet.index(gene)
    new_index = (index_alpha + mute) % len(alphabet)
    new_gene = alphabet[new_index]
    new_cromo = cromo[:index] + new_gene + cromo[index + 1:]
    return [new_cromo,0]
                   
    
    
if __name__ == '__main__':
    size = 29
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .!?:;'
    print sga(500,50,size,alphabet,tournament_selection, fit_weasel,mutation,elitism_selection,3,0.3,0.3,15)
    