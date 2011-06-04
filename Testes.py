# -*- coding: utf-8 -*-

from Brachistochrone import *
import sys
from time import strftime

pontos = [[0,100,30,50], [0,10,3,5], [10,100,20,10], [0,20,100,10]]
ngeracoes = [20, 50, 100, 250]
nindividuos = [50, 100, 200, 500]
ngenes = [15, 30]
tamanho_torneio = [0, 2, 5, 10]
nrecombinacao = [1, 3, 5]
prob_recombinacao = [0.1, 0.25, 0.5]
prob_mutacao = [0.05, 0.1, 0.15]
tamanho_elite = [0.0, 0.1, 0.3]
output = []
c = configuracoes(False)
ok = True

sys.stdout.write("\nQual a representação desejada (fixas/dinâmicas)? ")
texto = sys.stdin.readline().strip()
if texto == "fixas" or texto == "Fixas":
	c[-1] = False
	print "fixas"
else:
	c[-1] = True
	print "dinâmicas"

sys.stdout.write("\nQual o teste desejado?\n")
sys.stdout.write("1 - Nº de gerações + nº de indivíduos + nº de genes\n")
sys.stdout.write("2 - Método de selecção + tamanho de sorteio + probabilidades de recombinação e mutação\n")
teste = int(sys.stdin.readline())

melhores = []
piores = []
media = []
dp = []

if teste == 1:
	for ponto in pontos:
		output.append("\nPontos A(%d,%d) B(%d,%d)\n" % (ponto[0], ponto[1], ponto[2], ponto[3]))
		melhores.append(output[-1])
		piores.append(output[-1])
		media.append(output[-1])
		dp.append(output[-1])
		sys.stdout.write(output[-1])
		output.append("-----------------------------------------\n")
		sys.stdout.write(output[-1])
		for i in xrange(4):
			c[i] = ponto[i]
		for gene in ngenes:
			c[6] = gene
			for individuo in nindividuos:
				c[5] = individuo
				for geracao in ngeracoes:
					c[4] = geracao
					output.append("\nA(%d,%d) B(%d,%d)\n" % (ponto[0], ponto[1], ponto[2], ponto[3]))
					sys.stdout.write(output[-1])
					output.append("Número de genes: %d\n" % (gene))
					sys.stdout.write(output[-1])
					output.append("Número de indivíduos: %d\n" % (individuo))
					sys.stdout.write(output[-1])
					output.append("Número de gerações: %d\n" % (geracao))
					sys.stdout.write(output[-1])
					resultados = brachistochrone(1, False, c)
					output.append("Melhor indivíduo: %.5f    " % (resultados[0]))
					output.append("Pior indivíduo: %.5f    " % (resultados[1]))
					output.append("Aptidão média: %.5f    " % (resultados[2]))
					output.append("Desvio padrão: %.5f\n" % (resultados[3]))
					# facilitar passar para excel
					melhores.append("%.5f\n" % (resultados[0]))
					piores.append("%.5f\n" % (resultados[1]))
					media.append("%.5f\n" % (resultados[2]))
					dp.append("%.5f\n" % (resultados[3]))
		output.append("-----------------------------------------\n")
		sys.stdout.write(output[-1])

elif teste == 2:
	for ponto in pontos:
		output.append("\nPontos A(%d,%d) B(%d,%d)\n" % (ponto[0], ponto[1], ponto[2], ponto[3]))
		melhores.append(output[-1])
		piores.append(output[-1])
		media.append(output[-1])
		dp.append(output[-1])
		sys.stdout.write(output[-1])
		output.append("-----------------------------------------\n")
		sys.stdout.write(output[-1])
		for i in xrange(4):
			c[i] = ponto[i]
		for mutacao in prob_mutacao:
			c[10] = mutacao
			for recombinacao in prob_recombinacao:
				c[9] = recombinacao
				for tamanho in tamanho_torneio:
					c[7] = tamanho
					output.append("\nA(%d,%d) B(%d,%d)\n" % (ponto[0], ponto[1], ponto[2], ponto[3]))
					sys.stdout.write(output[-1])
					if tamanho > 0:
						output.append("Tamanho do torneio: %d\n" % (tamanho))
					else:
						output.append("Método de selecção: Roleta\n")
					sys.stdout.write(output[-1])
					output.append("Probabilidade de recombinação: %d\n" % (recombinacao))
					sys.stdout.write(output[-1])
					output.append("Probabilidade de mutação: %d\n" % (mutacao))
					sys.stdout.write(output[-1])
					resultados = brachistochrone(1, False, c)
					output.append("Melhor indivíduo: %.5f    " % (resultados[0]))
					output.append("Pior indivíduo: %.5f    " % (resultados[1]))
					output.append("Aptidão média: %.5f    " % (resultados[2]))
					output.append("Desvio padrão: %.5f\n" % (resultados[3]))
					# facilitar passar para excel
					melhores.append("%.5f\n" % (resultados[0]))
					piores.append("%.5f\n" % (resultados[1]))
					media.append("%.5f\n" % (resultados[2]))
					dp.append("%.5f\n" % (resultados[3]))
		output.append("-----------------------------------------\n")
		sys.stdout.write(output[-1])

else:
	ok = False

if ok:
	rep = "y"
	if c[-1]:
		rep = "xy"
	url = ("resultados/teste%d representacao %s " % (teste, rep))
	data = strftime("%d-%m-%Y - %Hh %Mm %Ss")
	# relatorio geral
	f = open(url+data+".txt", "w")
	f.writelines(output)
	f.close()
	# melhores
	f = open(url+"melhores "+data+".txt", "w")
	f.writelines(melhores)
	f.close()
	# piores
	f = open(url+"piores "+data+".txt", "w")
	f.writelines(piores)
	f.close()
	# media
	f = open(url+"media "+data+".txt", "w")
	f.writelines(media)
	f.close()
	# dp
	f = open(url+"dp "+data+".txt", "w")
	f.writelines(dp)
	f.close()
