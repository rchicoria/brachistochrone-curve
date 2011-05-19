# -*- coding: utf-8 -*-

from BrachFitness import *
import sys
from matplotlib.pyplot import plot, show
from random import uniform

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

def grafico(curva):
	x = []
	y = []
	
	for i in xrange(0, len(curva), 2):
		x.append(curva[i])
		y.append(curva[i+1])
	
	plot(x, y)
	show()

def cria_individuo(x1, y1, x2, y2, ngenes):
	individuo = [x1, y1]
	for i in xrange(ngenes-2):
		individuo.append((x1+((x2-x1)*(float(i+1)/(ngenes-1)))))
		individuo.append(uniform(0, y1))
	individuo.append(x2)
	individuo.append(y2)
	return [individuo, 0]

def cria_populacao(x1, y1, x2, y2, nindividuos, ngenes):
	return [cria_individuo(x1, y1, x2, y2, ngenes) for i in xrange(nindividuos)]

def cria_eixo_x(x1, x2, ngenes):
	return [(x1+((x2-x1)*(float(i)/(ngenes-1)))) for i in xrange(ngenes)]

def sga(x1, y1, x2, y2, ngeracoes, nindividuos, ngenes, seleccao_pais, fitness, mutacao,
		seleccao_sobreviventes, tamanho_torneio, prob_mutacao, tamanho_elite, tamanho_mutacao):
		
	# cria a população
	populacao = cria_populacao(x1, y1, x2, y2, nindividuos, ngenes)
	# avalia a população
	populacao = [[individuo[0], calcBrachTime(individuo[0])] for individuo in populacao]
	# continua...
	
	# só merda a partir daqui
	grafico(populacao[0][0])
	return True

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
	# faz os cálculos
	sga(x1, y1, x2, y2, ngeracoes, nindividuos, ngenes,0,0,0,0,0,0,0,0)
