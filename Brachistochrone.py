# -*- coding: utf-8 -*-

from BrachFitness import *
import sys
from matplotlib.pyplot import plot, show
from random import uniform, sample, random, choice
from operator import itemgetter

"""
Trabalho Prático Nº2: Curva Braquistócrona

Requisitos do sistema:
- módulo do Python matplotlib (em linux executar sudo apt-get install python-matplotlib)

Ficheiros necessários:
- Brachistochrone.py
- BrachFitness.py

Autores:
João Claro
Ricardo Lopes
Rui Chicória
"""

# recebe os pontos da curva de um indivíduo, e traça o gráfico respectivo
def grafico(curva):
	x = []
	y = []
	
	for i in xrange(0, len(curva), 2):
		x.append(curva[i])
		y.append(curva[i+1])
	
	plot(x, y)
	show()

# cria um indivíduo de acordo com as regras exigidas
def cria_individuo(x1, y1, x2, y2, ngenes):
	individuo = [x1, y1]
	for i in xrange(ngenes-2):
		individuo.append((x1+((x2-x1)*(float(i+1)/(ngenes-1)))))
		individuo.append(uniform(0, y1))
	individuo.append(x2)
	individuo.append(y2)
	return [individuo, 0]

# cria uma população com o número de indivíduos exigido
def cria_populacao(x1, y1, x2, y2, nindividuos, ngenes):
	return [cria_individuo(x1, y1, x2, y2, ngenes) for i in xrange(nindividuos)]

# selecciona os progenitores de uma dada geração através do método de torneio
def seleccao_torneio(populacao, tamanho_torneio):
    torneio = sample(populacao, tamanho_torneio)
    torneio.sort(key=itemgetter(1))
    return torneio[0]

# cria novos descendentes através do método de mutação de genes
def mutacao(individuo,y1):
    cromossomas = individuo[0]
    i = 1+2+2*choice(xrange((len(cromossomas)-4)/2))
    novo_gene = uniform(0, y1)
    while novo_gene == cromossomas[i]:
        novo_gene = uniform(0, y1)
    novos_cromossomas = cromossomas[:i]
    novos_cromossomas.append(novo_gene)
    novos_cromossomas.extend(cromossomas[i+1:])
    return [novos_cromossomas,0]

# escolhe os sobreviventes através de elitismo
def elitismo(populacao, descendentes, tamanho_elite):
    tamanho = int(len(populacao) * tamanho_elite)
    nova_populacao = populacao[:tamanho] + descendentes[:len(populacao) - tamanho]
    return nova_populacao

if __name__ == '__main__':

	# ponto 1
	sys.stdout.write("x1 y1 = ");
	x1, y1 = map(int, sys.stdin.readline().split())
	
	# ponto 2
	sys.stdout.write("x2 y2 = ");
	x2, y2 = map(int, sys.stdin.readline().split())
	
	# número de gerações
	sys.stdout.write("Número de gerações = ");
	ngeracoes = int(sys.stdin.readline())
	
	# número de indivíduos
	sys.stdout.write("Número de indivíduos = ");
	nindividuos = int(sys.stdin.readline())
	
	# número de genes
	sys.stdout.write("Número de genes = ");
	ngenes = int(sys.stdin.readline())
	
	# outras variáveis
	tamanho_torneio = 3
	prob_crossover = 0.3
	prob_mutacao = 0.5
	tamanho_elite = 0.3
	
	# faz os cálculos
	# cria a população
	populacao = cria_populacao(x1, y1, x2, y2, nindividuos, ngenes)
	# avalia a população
	populacao = [[individuo[0], calcBrachTime(individuo[0])] for individuo in populacao]
	for geracao in xrange(ngeracoes):
		# selecciona os progenitores
		progenitores = [seleccao_torneio(populacao, tamanho_torneio) for i in xrange(nindividuos)]
		# cria descendentes
		descendentes = []
		# para já, apenas permite por mutação
		for i in xrange(nindividuos):
			if random() < prob_mutacao:
				descendentes.append(mutacao(progenitores[i],y1))
			else:
				descendentes.append(progenitores[i])
		# avalia os descendentes
		descendentes = [[individuo[0], calcBrachTime(individuo[0])] for individuo in descendentes]
		descendentes.sort(key=itemgetter(1))
		# selecciona sobreviventes
		populacao = elitismo(populacao, descendentes, tamanho_elite)
		populacao.sort(key=itemgetter(1))
		sys.stdout.write( "Melhor descendente da geração %d: %f\n" % (geracao, populacao[0][1]) )
	grafico(populacao[0][0])
