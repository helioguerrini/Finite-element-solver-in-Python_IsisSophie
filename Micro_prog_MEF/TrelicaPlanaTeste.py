# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 03:17:17 2022

@author: Helio
"""
from numpy import array,zeros
#import function_Elementos
#import function_Givens
###############################################################################
############################## ENTRADA DE DADOS ###############################
###############################################################################

import tkinter.filedialog

root = tkinter.Tk()
root.withdraw()

filtro = (("Entrada", "*.txt"), ("All files", "*"))
nomeArq = tkinter.filedialog.askopenfilename(filetypes = filtro)

root.destroy()

root.mainloop()

res = open(nomeArq)
linha = res.readlines()
seletor, ElementoTipo = '',''
listaCorrente, matrizconect, tabCoordNod = [], [], []
tabDados, tabDadosUni, cargaF = [], [], []

for i in range(len(linha)):

    if seletor == 'F':
        conectlinha = linha[i]
        
        listaCorrente = conectlinha.split(',')
        cargaElem = [float(listaCorrente[0]), int(listaCorrente[1])]
        cargaF.append(cargaElem)
        
        listaCorrente = []

    if linha[i][:-1] == '*** Carregamento ***':
        seletor = 'F'    

    if seletor == 'E':
        conectlinha = linha[i]
        
        listaCorrente = conectlinha.split(',')
        CondCont = list(map(int,listaCorrente))
        listaCorrente = []

    if linha[i][:-1] == '*** Condicoes de Contorno ***':
        seletor = 'E'    
    
    if seletor == 'D':
        conectlinha = linha[i]
        
        listaCorrente = conectlinha.split(',')
        matSec = list(map(float,listaCorrente[:2]))
        tabDadosUni.append(matSec)
        matSecElem = list(map(int,listaCorrente[2:]))
        tabDadosUni.append(matSecElem)
        tabDados.append(tabDadosUni)
        listaCorrente = []
        tabDadosUni = []
    
    if linha[i][:-1] == '*** Materiais e Secoes ***':
        seletor = 'D'

    if seletor == 'C':
        conectlinha = linha[i]
        
        listaCorrente = conectlinha.split(',')
        listaCorrente = list(map(float,listaCorrente))
        tabCoordNod.append(listaCorrente)
        
        listaCorrente = []
    
    if linha[i][:-1] == '*** Coordenadas Nodais ***':
        seletor = 'C'

    if seletor == 'B':
        conectlinha = linha[i]
        
        #Elemento, noInicial, noFinal = conectlinha.split(',')
        listaCorrente = conectlinha.split(',')
        listaCorrente = list(map(int,listaCorrente))
        matrizconect.append(listaCorrente)

        listaCorrente = []
         
    if linha[i][:-1] == '*** Matriz de Conectividade ***':
        seletor = 'B'
    
    if seletor == 'A':
        ElementoTipo = linha[i]
        
    if linha[i][:-1] == '*** Elemento ***':
        seletor = 'A'
        
###############################################################################
# Funcao que retorna amatriz de rigidez do Elemento de Treliça Plana

def ElemTrel(E,A,x1,y1,x2,y2):
    l = ((x2-x1)**2 + (y2-y1)**2)**0.5
    CS, S = (x2-x1)/l , (y2-y1)/l
    MatrizRig = (E*A/l)*array([[CS**2,CS*S,-CS**2,-CS*S],[CS*S,S**2,-CS*S,-S**2],[-CS**2,-CS*S,CS**2,CS*S],[-CS*S,-S**2,CS*S,S**2]])
    return MatrizRig
###############################################################################
# Resolução de um sistema linear ([K]{U}={R}) pelo método de fatorização de Givens
def sl(K,R):
    # Ordem da matriz
    n=len(K) # conta o número de colunas da matriz [K]

    # Inicia variáveis
    k1, k2 = 0, 0

    # Fatorização de Givens
    for i in range(n-1):
        for h in range(i+1,n):
            if (K[i][i])**2+(K[h][i])**2==0:
                cs=1
                sn=0
            else:            
                # Determina cossenos e senos
                cs=(K[i][i])/((K[i][i])**2+(K[h][i])**2)**0.5
                sn=(K[h][i])/((K[i][i])**2+(K[h][i])**2)**0.5
            for j in range(n):
                k1,k2 = 0, 0
                k1,k2 = K[i][j], K[h][j]
                # Cálculo da matriz ~K ( vai transformando K em Sg)
                K[i][j] = k1*cs + k2*sn
                K[h][j] = -k1*sn + k2*cs
            # Vai transformando R em V  
            v1, v2 = R[i][0], R[h][0]
            R[i][0] = v1*cs + v2*sn
            R[h][0] = -v1*sn + v2*cs
    # Resolução do sistema linear ( obtém U )
    U=zeros([n,1],float)
    for i in range(n):
        SS=0
        for j in range(n):
            SS=SS+(K[n-1-i][n-1-j]*U[n-1-j])
        U[n-1-i]=(R[n-1-i][0]-SS)/K[n-1-i][n-1-i]

    return U

###############################################################################
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
    #k = function_Elementos.ElemTrel(E,A,x1,y1,x2,y2)
    k = ElemTrel(E,A,x1,y1,x2,y2)
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
deslocnod = sl(Kparcial,VetForca)
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
input('Pressione enter para cotinuar...')