# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 00:12:35 2021
Funcao Matriz de Rigidez dos Elementos Finitos
@author: Helio
"""
from numpy import array

# Matriz de rigidez do elemento de viga
def elemViga(E, I, L):
    
    k = (E*I/L**3)*array([[12, 6*L, -12, 6*L], [6*L, 4*L**2, -6*L, 2*L**2], [-12, -6*L, 12, -6*L], [6*L, 2*L**2, -6*L, 4*L**2]], float)
    
    return k
    

