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

if teste == 1:
	for ponto in pontos:
		sys.stdout.write("\nPontos A(%d,%d) B(%d,%d)\n" % (ponto[0], ponto[1], ponto[2], ponto[3]))
		sys.stdout.write("-----------------------------------------\n")
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
					brachistochrone(1, False, c)
		sys.stdout.write("-----------------------------------------\n")

elif teste == 2:
	for ponto in pontos:
		sys.stdout.write("\nPontos A(%d,%d) B(%d,%d)\n" % (ponto[0], ponto[1], ponto[2], ponto[3]))
		sys.stdout.write("-----------------------------------------\n")
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
					brachistochrone(1, False, c)
		sys.stdout.write("-----------------------------------------\n")

else:
	ok = False

if ok:
	rep = "y"
	if c[-1]:
		rep = "xy"
	f = open(("resultados/teste%d representacao %s - " % (teste, rep))+strftime("%d-%m-%Y - %Hh %Mm %Ss")+".txt", "w")
	f.writelines(output)
	f.close()
