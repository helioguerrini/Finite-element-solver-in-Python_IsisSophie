# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 17:04:07 2022

@author: Helio
"""
end = 'barra.txt'
res = open(end)
linha = res.readlines()
seletor, ElementoTipo = '',''
listaCorrente = []
matrizconect = []
tabCoordNod = []
tabDados = []
tabDadosUni = []
cargaF = []

for i in range(len(linha)):

    if seletor == 'F':
        conectlinha = linha[i]
        print (conectlinha)
        
        listaCorrente = conectlinha.split(',')
        cargaElem = [float(listaCorrente[0]), int(listaCorrente[1])]
        cargaF.append(cargaElem)
        
        listaCorrente = []

    if linha[i][:-1] == '*** Carregamento ***':
        seletor = 'F'    

    if seletor == 'E':
        conectlinha = linha[i]
        print (conectlinha)
        
        listaCorrente = conectlinha.split(',')
        CondCont = list(map(int,listaCorrente))
        listaCorrente = []

    if linha[i][:-1] == '*** Condicoes de Contorno ***':
        seletor = 'E'    
    
    if seletor == 'D':
        conectlinha = linha[i]
        print (conectlinha)
        
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
        print (conectlinha)
        
        listaCorrente = conectlinha.split(',')
        listaCorrente = list(map(float,listaCorrente))
        tabCoordNod.append(listaCorrente)
        
        listaCorrente = []
    
    if linha[i][:-1] == '*** Coordenadas Nodais ***':
        seletor = 'C'

    if seletor == 'B':
        conectlinha = linha[i]
        print (conectlinha)
        
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
        
            
print (ElementoTipo)
print (matrizconect)
print(tabCoordNod)
print(tabDados)
print (CondCont)
print(cargaF)