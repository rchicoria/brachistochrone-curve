# -*- coding: utf-8 -*-

from BrachFitness import *
import sys
from matplotlib.pyplot import plot, show, ylabel, xlabel, title, savefig, close
from random import uniform, sample, random, choice
from operator import itemgetter
from math import sqrt
from time import strftime
import re

"""
Trabalho Prático Nº2: Curva Braquistócrona

Requisitos do sistema:
- módulo do Python matplotlib (em linux executar sudo apt-get install python-matplotlib)

Ficheiros/directorias necessários:
- Brachistochrone.py
- BrachFitness.py
- conf.txt
- testes (directoria)

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
	
	ylabel('y')
	xlabel('x')
	title('Melhor curva braquistocrona gerada')
	plot(x, y, 'r')
	show()

# mostra a evolução da população
def grafico_geracoes(dadosgeracoes, data):
	x = [i for i in xrange(len(dadosgeracoes))]
	melhor = [dado[0] for dado in dadosgeracoes]
	pior = [dado[1] for dado in dadosgeracoes]
	media = [dado[2] for dado in dadosgeracoes]
	dp = [dado[3] for dado in dadosgeracoes]
	close()
	plot(x, melhor, 'g', x, pior, 'r', x, media, 'b', x, dp, 'y')
	savefig("testes/"+data+".png")

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
def cria_individuo(x1, y1, x2, y2, ngenes, abcissas_aleatorias):
	individuo = [x1, y1]
	for i in xrange(ngenes-2):
		if abcissas_aleatorias:
			individuo.append(uniform(x1, x2))
		else:
			individuo.append((x1+((x2-x1)*(float(i+1)/(ngenes-1)))))
		individuo.append(uniform(0, y1))
	individuo.append(x2)
	individuo.append(y2)
	if abcissas_aleatorias and not checkIndiv(individuo):
		individuo = ordena_abcissas(individuo)
		while individuo == False:
			individuo = cria_individuo(x1, y1, x2, y2, ngenes, abcissas_aleatorias)
	return [individuo, calcBrachTime(individuo)]

# ordena as abcissas de um indivído com abcissas geradas aleatoriamente
def ordena_abcissas(individuo):
	temp = []
	for i in xrange(0, len(individuo), 2):
		temp.append([individuo[i], individuo[i+1]])
	temp.sort(key=itemgetter(0))
	aux = temp[0][0]
	for i in xrange(1, len(temp)):
		if aux == temp[i][0]:
			return False
		else:
			aux = temp[i][0]
	for i in xrange(len(temp)):
		individuo[i*2] = temp[i][0]
		individuo[i*2+1] = temp[i][1]
	return individuo

# faz a selecção dos progenitores de uma dada geração confome o método indicado
def seleccao(populacao, tamanho_torneio):
	# selecciona através do método de torneio se o tamanho de torneio não for 0
	if tamanho_torneio > 0:
		torneio = sample(populacao, tamanho_torneio)
		torneio.sort(key=itemgetter(1))
		return torneio[0]
	# selecciona através do método da roleta se o tamanho de torneio for 0
	else:
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
def recombinacao(nrecombinacao, progenitor1, progenitor2, abcissas_aleatorias):
	p1y = [progenitor1[i*2+1] for i in xrange(len(progenitor1)/2)]
	p2y = [progenitor2[i*2+1] for i in xrange(len(progenitor2)/2)]
	pontos = [choice(xrange(len(p1y))) for i in xrange(nrecombinacao)]
	pontos.sort()
	d1y = p1y[:pontos[0]]
	d2y = p2y[:pontos[0]]
	for i in xrange(len(pontos)-1):
		p1y, p2y = p2y, p1y
		d1y.extend(p1y[pontos[i]:pontos[i+1]])
		d2y.extend(p2y[pontos[i]:pontos[i+1]])
	d1y.extend(p2y[pontos[-1]:])
	d2y.extend(p1y[pontos[-1]:])
	descendente1 = progenitor1[:]
	descendente2 = progenitor2[:]
	for i in xrange(len(d1y)):
		descendente1[i*2+1] = d1y[i]
		descendente2[i*2+1] = d2y[i]
	return [[descendente1, calcBrachTime(descendente1)], [descendente2, calcBrachTime(descendente2)]]

# cria novos descendentes através do método de mutação de genes
def mutacao(individuo, y1, abcissas_aleatorias):
    cromossomas = individuo[0]
    i = 1+2+2*choice(xrange((len(cromossomas)-4)/2))
    novo_gene = uniform(0, y1)
    while novo_gene == cromossomas[i]:
        novo_gene = uniform(0, y1)
    novos_cromossomas = cromossomas[:i]
    novos_cromossomas.append(novo_gene)
    novos_cromossomas.extend(cromossomas[i+1:])
    if abcissas_aleatorias and not checkIndiv(novos_cromossomas):
    	novos_cromossomas = ordena_abcissas(novos_cromossomas)
    	while novos_cromossomas == False:
    		novos_cromossomas = mutacao(individuo, y1, abcissas_aleatorias)
    return [novos_cromossomas, calcBrachTime(novos_cromossomas)]

# escolhe os sobreviventes através de elitismo
def elitismo(populacao, descendentes, tamanho_elite):
    tamanho = int(len(populacao) * tamanho_elite)
    nova_populacao = populacao[:tamanho] + descendentes[:len(populacao) - tamanho]
    return nova_populacao

def run():
	# prepara ficheiro de output
	data = strftime("%d-%m-%Y - %Hh %Mm %Ss")
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
	output.append("Representação (abcissas fixas ou dinâmicas): ")
	if abcissas_aleatorias:
		output.append("dinâmicas\n")
	else:
		output.append("fixas\n")
	output.append("\nResultados:\n")
	
	# faz os cálculos
	nrecombinacoes = 0
	nmutacoes = 0
	dadosgeracoes = []
	
	# cria a população e avalia-a
	populacao = [cria_individuo(x1, y1, x2, y2, ngenes, abcissas_aleatorias) for i in xrange(nindividuos)]
	
	for geracao in xrange(ngeracoes):
	
		# selecciona os progenitores
		progenitores = [seleccao(populacao, tamanho_torneio) for i in xrange(nindividuos)]
		
		# cria descendentes
		descendentes = []
		
		# por recombinação
		for i in xrange(0, nindividuos, 2):
			if random() < prob_recombinacao:
				descendentes.extend(recombinacao(nrecombinacao, progenitores[i][0], progenitores[i+1][0], abcissas_aleatorias))
				nrecombinacoes += 2
			else:
				descendentes.extend([progenitores[i], progenitores[i+1]])
				
		# por mutação
		for i in xrange(nindividuos):
			if random() < prob_mutacao:
				descendentes[i] = mutacao(descendentes[i], y1, abcissas_aleatorias)
				nmutacoes += 1
				
		# selecciona sobreviventes
		descendentes.sort(key=itemgetter(1))
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
		dadosgeracoes.append([valores[0], valores[-1], media, dp])
		
	grafico_geracoes(dadosgeracoes, data)
	sys.stdout.write("Aptidão do melhor indivíduo: %f\n" % (populacao[0][1]))
	output.append( "\nNúmero de recombinações: %d\n" % (nrecombinacoes) )
	output.append( "Número de mutações: %d\n" % (nmutacoes) )
	
	# guarda os resultados num ficheiro
	f = open("testes/"+data+".txt", "w")
	f.writelines(output)
	f.close()
	
	return [valores[0], valores[-1], media, dp]

if __name__ == '__main__':

	sys.stdout.write("Número de repetições da experiência: ")
	n = int(sys.stdin.readline())
	
	# pré-definições
	x1 = 1
	y1 = 5
	x2 = 4
	y2 = 2
	ngeracoes = 100
	nindividuos = 50
	ngenes = 20
	tamanho_torneio = 3
	nrecombinacao = 5
	prob_recombinacao = 0.6
	prob_mutacao = 0.1
	tamanho_elite = 0.3
	abcissas_aleatorias = True

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
		prob_mutacao = float(linhas[11].split("=")[1].split("%")[0].strip())/100
		tamanho_elite = float(linhas[12].split("=")[1].split("%")[0].strip())/100
		texto = linhas[13].split(":")[1].strip()
		if texto == "fixas" or texto == "Fixas":
			abcissas_aleatorias = False
		else:
			abcissas_aleatorias = True
	except:
		sys.stdout.write("O ficheiro de configuração não existe ou está corrompido. Foi gerado um novo ficheiro com as configurações pré-definidas\n\n")
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
		f.write("Representação (abcissas fixas ou dinâmicas): ")
		if abcissas_aleatorias:
			f.write("dinâmicas\n")
		else:
			f.write("fixas\n")
		f.close()
		f = open("conf.txt", "r")
	
	f.seek(0)
	sys.stdout.write(f.read()+"\n")
	f.close()
	
	medias = [0.0 for i in xrange(4)]
	for i in xrange(n):
		temp = run()
		for j in xrange(4):
			medias[j] += temp[j]
	
	for i in xrange(4):
		medias[i] /= n
	print medias
