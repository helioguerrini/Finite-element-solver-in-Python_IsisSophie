# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 19:06:38 2021
PROGRAMA DE ANALISE DE VIGAS POR ELEMENTOS FINITOS - ELEMENTOS 1D
@author: Helio Guerrini Filho
Atualizado 06/07/2021
"""
############################## Modulos #######################################
import numpy as np
from numpy.linalg import solve
from ELEMENTOS import elemViga

######################### Parametros da malha ################################
# Tabela de conectividade
tabConect = np.array([[1, 1, 2],[2, 2, 3]],int)

# Tabela de coord nodais = array([[x1, y1],...,[xN, yN]])
tabCoordNod = np.array([[0, 0], [1.25, 0], [2.5, 0]],float)

############################# Tabela de dados ################################
tabDados = np.array([[1.25, 8.5e-6, 200e9],[1.25, 8.5e-6, 200e9]])

################# Definicao das condicoes de contorno CC #####################
#condCont = [numero gdl restringido 1, ..., numero gdl restringido N]
condCont = [3,5,6]

######################## Definicao do carregamento ###########################
#cargaFM = [[Forca ou Momento1, GDL1], ..., [Forca ou MomentoN, GDLN]]
cargaFM = [[-5000.0, 1]]

######################### Matriz de zeros Global #############################
# Numero de graus de liberdade da estrutura.
Ngdl = 2*len(tabCoordNod)
K = np.zeros((Ngdl, Ngdl),float)

##################### Montagem da Matriz de Rigidez ##########################
for i in range(len(tabConect)):
    # Separa o elemento corrente
    elemento = tabConect[i][0]
    E, I, L = tabDados[elemento-1][2], tabDados[elemento-1][1], tabDados[elemento-1][0]
    # Matriz de rigidez do elemento finito  de viga
    k = elemViga(E, I, L)
    # Primeiro e segundo no 
    primNo,segunNo = tabConect[i][1], tabConect[i][2]
    # Primeiro grau de liberdade
    gdlf1 = 1 + (primNo -1)*2
    # Terceiro grau de liberdade
    gdlf3 = 1 + (segunNo -1)*2
    # Segundo grau de liberdade
    gdlf2, gdlf4 = (gdlf1 + 1), (gdlf3 + 1)
    # Vetor de Graus de liberdade
    vetorGDL = np.array([gdlf1, gdlf2, gdlf3, gdlf4],int)
    # Terceiro
    for ii in range(4):
        for jj in range(4):
            K[vetorGDL[ii]-1][vetorGDL[jj]-1] = K[vetorGDL[ii]-1][vetorGDL[jj]-1] + k[ii][jj]
'''
print ('Matriz Global de Rigidez:')
print ('[K] = ', K)
'''

######### Matriz de rigidez cortada nos graus de liberdade da CC #############
# Numero de graus de liberdade nao restrigidos
NgdlnR = len(K) - len(condCont)
# Matriz de rigidez de zeros
kp = np.zeros((NgdlnR, NgdlnR),float)

# Lista de graus de liberdade não restringidos
listGDLnR = list(range(Ngdl))
for i in range(len(condCont)):
    NN = condCont[i]
    listGDLnR.remove(NN-1)

# Matriz de rigidez cortada
for i in range(NgdlnR):
    for j in range(NgdlnR):
        kp[i][j] = kp[i][j] + K[listGDLnR[i]][listGDLnR[j]]

########################## *Vetor de Forca/Momento Aplicado ####################
vetorFM = np.zeros((NgdlnR), float)
for i in range(len(cargaFM)):
    gdlFM = cargaFM[i][1]
    for j in range(NgdlnR):
        if (gdlFM-1) == listGDLnR[j]:
            vetorFM[j] =  cargaFM[i][0]

######################### Gera matrizes de resultados ########################
# Numero de nos
numNodes = len(tabCoordNod)
#resultDesloc = [[GDL1, Desloc1, Rotacao1], ...,[GDLN, DeslocN, RotacaoN]]]
resultDesloc = np.zeros((numNodes, 2),float)
#resultForca = [[GDL1, Forca1, Momento1], ...,[GDLN, ForcaN, MomentoN]]]
resultForca = np.zeros((numNodes, 2),float)

 
######################### Abre o arquivo de resultados ######################
res = open('Resultados.txt', 'w')
#res = open('Resultados.csv', 'w')

            
########################### Deslocamentos nodais #############################
deslocq = solve(kp, vetorFM)
print ('########### Deslocamentos nodais: ###########')

for i in range(NgdlnR):
    print ('Grau de liberdade = ', listGDLnR[i]+1)

    if (listGDLnR[i]+1)%2 == 0:
        print ('Rotacao = ', deslocq[i])
        posdeC = int((listGDLnR[i] + 1)/2) - 1
        resultDesloc[posdeC][1] = resultDesloc[posdeC][1] + deslocq[i]
        
    else:
        print ('Deslocamento = ', deslocq[i])
        posdeC = int((listGDLnR[i] + 2)/2) - 1
        resultDesloc[posdeC][0] = resultDesloc[posdeC][0] + deslocq[i]

    print ()

############################# Reacoes de apoio ##############################
print ('############# Reacoes de apoio: #############')

# Cicla os graus de liberdade restringidos
for i in range(len(condCont)):
    # Inicia a variável de reação de apoio
    FM = 0.0
    # Cicla todos os graus de liberdade da estrutura
    for j in range(Ngdl):
        # Inicia o valor do deslocamento para o grau de liberdade corrente
        qq = 0
        # Cicla os graus de liberdade não restringidos
        for ij in range(NgdlnR):
            if j == listGDLnR[ij]:
                qq = deslocq[ij]
        # Calcula as componentes de reação de apoio
        FM = FM + K[condCont[i]-1][j]*qq
    print ('Grau de liberdade = ', condCont[i])
    
    if (condCont[i])%2 == 0:
        print ('Momento = ', FM)
        posdeC = int((condCont[i])/2) - 1
        resultForca[posdeC][1] = resultForca[posdeC][1] + FM

    else:
        print ('Forca = ', FM)
        posdeC = int((condCont[i] + 1)/2) - 1
        resultForca[posdeC][0] = resultForca[posdeC][0] + FM

    print ()


######################### Escreve arquivo de resultados ######################
res.write('########### Deslocamentos e rotacoes nodais: ###########\n')
# Escreve o nome das colunas #
tamNodes = len(str(numNodes))
res.write('No')
for i in range(tamNodes + 2):
    res.write(' ')
res.write('Deslocamento  Rotacao\n')
#############################

# Escreve os valores das colunas #
for i in range(numNodes):
    res.write('{:1d}'.format(i+1))
    for j in range(2):
        res.write('{:14.4e}'.format(resultDesloc[i][j]))
    res.write('\n')
res.write('\n')
#############################

res.write('################### Reacoes de apoio: ##################\n')
# Escreve o nome das colunas #
tamNodes = len(str(numNodes))
res.write('No')
for i in range(tamNodes + 2):
    res.write(' ')
res.write('Forca         Momento\n')
#############################

for i in range(numNodes):
    res.write('{:1d}'.format(i+1))
    for j in range(2):
        res.write('{:14.4e}'.format(resultForca[i][j]))
    res.write('\n')
res.write('\n')

res.write('############## Matriz Global de Rigidez: ###############\n')
for i in range(Ngdl):
    for j in range(Ngdl):
        #res.write('{:12.4e}'.format(K[i][j]) + ',')
        res.write('{:12.4e}'.format(K[i][j]))
    res.write('\n')

res.close()


import os
os.system('Resultados.txt')











