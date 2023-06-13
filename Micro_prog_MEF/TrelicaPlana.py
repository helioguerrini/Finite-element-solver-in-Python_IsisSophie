# -*- coding: utf-8 -*-
"""
Criado em 14 de Jan quinta-feira 20:04:20 2016
Atualizado em 06 de Mar terça-feira 01:03:40 2018
Programa para análise de treliças planas Versão 1.1
@autor: Msc Hélio Guerrini Filho
"""
from numpy import array,zeros
import function_Elementos
import function_Givens
###############################################################################
############################## ENTRADA DE DADOS ###############################
###############################################################################

########################### Matriz de conectividade ###########################
# formato: matrizconect = array([[Elemento1,nó_inicial,nó_final],[Elemento2,
# nó_inicial,nó_final],...,[ElementoN,nó_inicial,nó_final]])
#matrizconect = array([[1,1,2],[2,2,3],[3,1,3],[4,3,4]],int)
matrizconect = [[1,1,2],[2,2,3],[3,1,3],[4,3,4]]

######################## Matriz de coordenadas nodais (malha) #################
# tabCoordNod = array([[x1,y1],...,[xN,yN]) - A posicao corresponde ao node
#tabCoordNod = array([[0.0,0.0],[1000,0.0],[1000,750],[0.0,750]],float)
tabCoordNod = [[0.0,0.0],[1000,0.0],[1000,750],[0.0,750]]

############################# Tabela de dados #################################
#tabDados = [[[Area1, modulo de young1], [elem1, elem3, elem7...]],[[Area2, modulo de young],[elem2, elem5, elem4...]]]
tabDados = [[[645.0, 200.0e3],[1,2]],[[645.0, 200.0e3],[3,4]]]

############################## Condições de contorno ##########################
#CondCont = array([graus de liberdade fixos])
#CondCont = array([1,2,4,7,8], int)
CondCont = [1,2,4,7,8]

######################## Definicao do carregamento ###########################
#cargaF = [[Forca, GDL1], ..., [ForcaN, GDLN]]
cargaF = [[90000.0, 3], [-110000.0, 6]]

#################### Montagem da matriz global de rigidez #####################
#Declaração da matriz de zeros
Nglobal = 2*len(tabCoordNod)
K = zeros([Nglobal,Nglobal],float)
for ps in range(len(matrizconect)):
    #Obtém elementos e nós correntes    
    el = matrizconect[ps][0] #Elemento corrente
    no1, no2 = matrizconect[ps][1], matrizconect[ps][2] #Nós do elemento
    
    #Obtem as propriedades do elemento - área de secao e modulo de elasticidade
    for jh in range(len(tabDados)):
        for hj in range(len(tabDados[jh][1])):
            if tabDados[jh][1][hj] == el:
                A, E = tabDados[jh][0][0], tabDados[jh][0][1]
            
    #Obtém coordenadas dos nós
    x1, y1 = tabCoordNod[no1-1][0], tabCoordNod[no1-1][1]
    x2, y2 = tabCoordNod[no2-1][0], tabCoordNod[no2-1][1]
    #Obtém a matriz de rigidez do elemento corrente
    k = function_Elementos.ElemTrel(E,A,x1,y1,x2,y2)
    ## Montagem da matriz global
    for i in range(4):
        if i<=1:
            ig = (2*no1 - 2) + i
        else:
            ig = (2*no2 - 4) + i
        for j in range(4):
            if j<=1:
                jg = (2*no1 - 2) + j
            else:
                jg = (2*no2 - 4) + j
            #print i, ig, j, jg
            K[ig][jg] = K[ig][jg] + k[i][j]
#print ('Matriz de Rigidez Global:')
#print ('[K] = ', K)
############# Determinação da matriz global de rigidez parcial ################
##################### segundo as condições de contorno ########################
Nparcial = Nglobal - len(CondCont)
Kparcial = zeros([Nparcial,Nparcial],float) #matriz parcial
Gdllivres = zeros([Nparcial,1],float) #matriz parcial
iii = 0 # Contador auxiliar
for i in range(Nglobal):
    VarLogic = 0
    for j in range(len(CondCont)):
        CC = CondCont[j]
        if i+1 == CC:
            VarLogic = 1
    if VarLogic == 0:
        Gdllivres[iii] = Gdllivres[iii] + (i+1)
        iii = iii + 1
            
for i in range(Nparcial):
    Gdli = int(Gdllivres[i])
    for j in range(Nparcial):
        Gdlj = int(Gdllivres[j])
        Kparcial[i][j] = Kparcial[i][j] + K[(Gdli-1)][(Gdlj-1)]
        
        
############################# Vetor de Forca Aplicado #########################
VetForca = zeros((Nparcial,1), float)
for i in range(len(cargaF)):
    gdlF = cargaF[i][1]
    for j in range(Nparcial):
        if (gdlF) == Gdllivres[j][0]:
            VetForca[j][0] =  cargaF[i][0]
            
##################### Determinação dos deslocamentos nodais ####################
deslocnod = function_Givens.sl(Kparcial,VetForca)
VetDeslcGlogal = zeros([Nglobal,1],float)
p, Pos = 0, 0
for i in range(len(VetDeslcGlogal)):
    Pos = Gdllivres[p]
    if i+1 == Pos:
        VetDeslcGlogal[i] = VetDeslcGlogal[i] + deslocnod[p]
        if p<=len(Gdllivres)-1:
            p = p + 1
        if p>len(Gdllivres)-1:
            p=len(Gdllivres)-1
print 
print ('Vetor de deslocamentos nodais:')
print ('{q} = ', VetDeslcGlogal)

'''
######################### Abre o arquivo de resultados ######################
res = open('Resultados_treliças.txt', 'w')

res.close()

import os
os.system('Resultados.txt')


######################### Determinação das forças nodais #######################
VetFocaGlogal = zeros([Nglobal,1],float)

for i in range(len(VetFocaGlogal)):
    for j in range(len(VetFocaGlogal)):
        VetFocaGlogal[i] = VetFocaGlogal[i] + K[i][j]*VetDeslcGlogal[j]

print 
print ('Vetor de forcas nodais:')
print ('{F} = ', VetFocaGlogal)            
'''
            
            
            
            
            
            
            
            
            
            
            
            
            
            

