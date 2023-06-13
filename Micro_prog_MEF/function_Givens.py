# -*- coding: cp1252 -*-
# Resolução de um sistema linear ([K]{U}={R}) pelo método de fatorização de Givens
from numpy import *
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
