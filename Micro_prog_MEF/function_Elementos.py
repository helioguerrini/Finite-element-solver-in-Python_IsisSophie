# -*- coding: utf-8 -*-
"""
Criado em Jan 19 terça-feira 02:20:23 2016
Programa que fornece as matrizes de rigidez dos elememtos finitos
@autor: Msc Hélio Guerrini Filho
"""
# Matriz do Elemento de Treliça Plana
from numpy import array
def ElemTrel(E,A,x1,y1,x2,y2):
    l = ((x2-x1)**2 + (y2-y1)**2)**0.5
    CS, S = (x2-x1)/l , (y2-y1)/l
    MatrizRig = (E*A/l)*array([[CS**2,CS*S,-CS**2,-CS*S],[CS*S,S**2,-CS*S,-S**2],[-CS**2,-CS*S,CS**2,CS*S],[-CS*S,-S**2,CS*S,S**2]])
    return MatrizRig

# Matriz do Elemento de Portico Plano
"""
Elemento implementado por
@autor: Bruno Massao
"""
def ElemPort2D(E,A,I,x1,y1,x2,y2):
    l = ((x2-x1)**2 + (y2-y1)**2)**0.5
    C, S = (x2-x1)/l , (y2-y1)/l
    #print C, S
    MatrizPort2D = (E/l)*(array([[(A*C**2)+((12*I/l**2)*S**2),(A-(12*I/l**2))*C*S,(-6*I/l)*S,-((A*C**2)+((12*I/l**2)*S**2)),-((A-(12*I/l**2))*C*S),-((6*I/l)*S)],
                              [(A-(12*I/l**2))*C*S,((A*S**2)+((12*I/l**2)*C**2)),(6*I/l)*C,-((A-(12*I/l**2))*C*S),-((A*S**2)+((12*I/l**2)*C**2)),(6*I/l)*C],
                              [(-6*I/l)*S,(6*I/l)*C,4*I,(6*I/l)*S,(-6*I/l)*C,2*I],
                              [-((A*C**2)+((12*I/l**2)*S**2)),-((A-(12*I/l**2))*C*S),(6*I/l)*S,(A*C**2)+((12*I/l**2)*S**2),(A-(12*I/l**2))*C*S,(6*I/l)*S],
                              [-((A-(12*I/l**2))*C*S),-((A*S**2)+((12*I/l**2)*C**2)),-((6*I/l)*C),((A-(12*I/l**2))*C*S),((A*S**2)+((12*I/l**2)*C**2)),-(6*I/l)*C],
                              [-((6*I/l)*S),(6*I/l)*C,2*I,(6*I/l)*S,-(6*I/l)*C,4*I]]))
    return MatrizPort2D

