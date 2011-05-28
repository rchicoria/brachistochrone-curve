# -*- coding: utf-8 -*-

from BrachFitness import *
import sys
from matplotlib.pyplot import plot, show
from random import uniform, sample, random, choice
from operator import itemgetter
from math import sqrt
from time import strftime
import re

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

# mostra uma percentagem com base num número decimal
def percentagem(numero):
	numero = numero * 100
	string = "%f" % (numero)
	novo = re.split("0+$", string)
	if novo[0][-1] == ".":
		return novo[0][:-1] + "%"
	else:
		return novo[0] + "%"

# cria um indivíduo de acordo com as regras exigidas
def cria_individuo(x1, y1, x2, y2, ngenes):
	individuo = [x1, y1]
	for i in xrange(ngenes-2):
		individuo.append((x1+((x2-x1)*(float(i+1)/(ngenes-1)))))
		individuo.append(uniform(0, y1))
	individuo.append(x2)
	individuo.append(y2)
	return [individuo, 0]

# selecciona os progenitores de uma dada geração através do método de torneio
def seleccao_torneio(populacao, tamanho_torneio):
    torneio = sample(populacao, tamanho_torneio)
    torneio.sort(key=itemgetter(1))
    return torneio[0]

# selecciona os progenitores de uma dada geração através do método da roleta
def seleccao_roleta(populacao):
	roleta = [0 for i in xrange(len(populacao))]
	total = 0
	for i in xrange(len(populacao)):
		total += populacao[i][1]
		roleta[i] = total
	resultado = uniform(0, total)
	for i in xrange(len(populacao)):
		if roleta[i] > resultado:
			return populacao[i]

# cria novos descendentes através do método de recombinação de genes
def recombinacao(nrecombinacao, progenitor1, progenitor2):
    pontos = [choice(xrange(len(progenitor1))) for i in xrange(nrecombinacao)]
    pontos.sort()
    descendente1 = progenitor1[:pontos[0]]
    descendente2 = progenitor2[:pontos[0]]
    for i in xrange(len(pontos)-1):
    	progenitor1, progenitor2 = progenitor2, progenitor1
    	descendente1.extend(progenitor1[pontos[i]:pontos[i+1]])
    	descendente2.extend(progenitor2[pontos[i]:pontos[i+1]])
    descendente1.extend(progenitor2[pontos[-1]:])
    descendente2.extend(progenitor1[pontos[-1]:])
    return [[descendente1, 0], [descendente2, 0]]

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

	# pré-definições
	x1 = 1
	y1 = 5
	x2 = 4
	y2 = 2
	ngeracoes = 10000
	nindividuos = 50
	ngenes = 50
	tamanho_torneio = 3
	nrecombinacao = 5
	prob_recombinacao = 0.6
	prob_mutacao = 0.1
	tamanho_elite = 0.3

	# carrega as configurações
	try:
		f = open("conf.txt", "r")
		linhas = f.readlines()
		x1 = int(linhas[3].split("(")[1].split(",")[0].strip())
		y1 = int(linhas[3].split(",")[1].split(")")[0].strip())
		x2 = int(linhas[4].split("(")[1].split(",")[0].strip())
		y2 = int(linhas[4].split(",")[1].split(")")[0].strip())
		ngeracoes = int(linhas[5].split("=")[1].strip())
		nindividuos = int(linhas[6].split("=")[1].strip())
		ngenes = int(linhas[7].split("=")[1].strip())
		tamanho_torneio = int(linhas[8].split("=")[1].strip())
		nrecombinacao = int(linhas[9].split("=")[1].strip())
		prob_recombinacao = float(linhas[10].split("=")[1].split("%")[0].strip())/100
		print prob_recombinacao
		prob_mutacao = float(linhas[11].split("=")[1].split("%")[0].strip())/100
		print prob_mutacao
		tamanho_elite = float(linhas[12].split("=")[1].split("%")[0].strip())/100
		print tamanho_elite
	except:
		sys.stdout.write("O ficheiro de configuração não existe ou está corrompido. Foi gerado um novo ficheiro com as configurações pré-definidas\n")
		f = open("conf.txt", "w")
		f.write("Trabalho Prático Nº2: Curva Braquistócrona\n")
		f.write("Ficheiro de configuração\n\n")
		f.write("Ponto A = (%d,%d)\n" % (x1, y1))
		f.write("Ponto B = (%d,%d)\n" % (x2, y2))
		f.write("Número de gerações = %d\n" % (ngeracoes))
		f.write("Número de indivíduos = %d\n" % (nindividuos))
		f.write("Número de genes = %d\n" % (ngenes))
		f.write("Tamanho do torneio = %d\n" % (tamanho_torneio))
		f.write("Número de pontos de recombinação = %d\n" % (nrecombinacao))
		f.write("Probabilidade de recombinação = %s\n" % (percentagem(prob_recombinacao)))
		f.write("Probabilidade de mutação = %s\n" % (percentagem(prob_mutacao)))
		f.write("Tamanho da elite = %s\n" % (percentagem(tamanho_elite)))
	
	f.close()
	
	# prepara ficheiro de output
	data = strftime("%d-%m-%Y - %H:%M:%S")
	output = ["\nResultados do teste ocorrido a %s:\n" % (data)]
	output.append("\nDados:\n")
	output.append("ponto A = (%d,%d)\n" % (x1, y1))
	output.append("ponto B = (%d,%d)\n" % (x2, y2))
	output.append("Número de gerações = %d\n" % (ngeracoes))
	output.append("Número de indivíduos = %d\n" % (nindividuos))
	output.append("Número de genes = %d\n" % (ngenes))
	output.append("Tamanho do torneio = %d\n" % (tamanho_torneio))
	output.append("Número de pontos de recombinação = %d\n" % (nrecombinacao))
	output.append("Probabilidade de recombinação = %s\n" % (percentagem(prob_recombinacao)))
	output.append("Probabilidade de mutação = %s\n" % (percentagem(prob_mutacao)))
	output.append("Tamanho da elite = %s\n" % (percentagem(tamanho_elite)))
	output.append("\nResultados:\n")
	
	# faz os cálculos
	nrecombinacoes = 0
	nmutacoes = 0
	
	# cria a população
	populacao = [cria_individuo(x1, y1, x2, y2, ngenes) for i in xrange(nindividuos)]
	
	# avalia a população
	populacao = [[individuo[0], calcBrachTime(individuo[0])] for individuo in populacao]
	
	for geracao in xrange(ngeracoes):
	
		# selecciona os progenitores
		progenitores = [seleccao_roleta(populacao) for i in xrange(nindividuos)]
		
		# cria descendentes
		descendentes = []
		
		# por recombinação
		for i in xrange(0, nindividuos, 2):
			if random() < prob_recombinacao:
				descendentes.extend(recombinacao(nrecombinacao, progenitores[i][0], progenitores[i+1][0]))
				nrecombinacoes += 2
			else:
				descendentes.extend([progenitores[i], progenitores[i+1]])
				
		# por mutação
		for i in xrange(nindividuos):
			if random() < prob_mutacao:
				descendentes[i] = mutacao(descendentes[i],y1)
				nmutacoes += 1
				
		# avalia os descendentes
		descendentes = [[individuo[0], calcBrachTime(individuo[0])] for individuo in descendentes]
		descendentes.sort(key=itemgetter(1))
		
		# selecciona sobreviventes
		populacao = elitismo(populacao, descendentes, tamanho_elite)
		populacao.sort(key=itemgetter(1))
		
		# mostra dados sobre a população na presente geração
		valores = [individuo[1] for individuo in populacao]
		media = sum(valores)/len(valores)
		valores_dp = [(valor-media)*(valor-media) for valor in valores]
		dp = sqrt(sum(valores_dp)/len(valores_dp))
		output.append( "\nGeração %d\n" % (geracao+1) )
		output.append( "Melhor descendente: %f\n" % (valores[0]) )
		output.append( "Pior descendente: %f\n" % (valores[-1]) )
		output.append( "Aptidão média: %f\n" % (media) )
		output.append( "Desvio padrão: %f\n" % (dp) )
		
	grafico(populacao[0][0])
	output.append( "\nNúmero de recombinações: %d\n" % (nrecombinacoes) )
	output.append( "Número de mutações: %d\n" % (nmutacoes) )
	
	# guarda os resultados num ficheiro
	f = open(data+".txt", "w")
	f.writelines(output)
	f.close()
