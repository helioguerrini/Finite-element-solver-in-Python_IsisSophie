# -*- coding: utf-8 -*-
"""
Programa para análise de treliças planas 
@autor: Msc Hélio Guerrini Filho
"""
###################################### Módulos #########################################
from pandas import DataFrame
from numpy import array, zeros, arange
from math import pi, sin, cos
import win32com.client
acad = win32com.client.Dispatch("AutoCAD.Application")

print('#########################################################################')
print('#########################################################################')
print('########################### ISIS SOPHIE CAE #############################')
print('########### EXECUTÁVEL DE ANÁLISE ESTÁTICA PARA TRELIÇAS 2D #############')
print('#########################################################################')
print('#########################################################################')

Seletor = ''
while Seletor != 'Sair':
    Seletor = input('>>>')
    
    if Seletor == '@#$Executar_analise$#@':
        try:    
            ###############################################################################
            ############################## ENTRADA DE DADOS ###############################
            ###############################################################################
            
            ############################# Inicia as matrizes ##############################
            tabCoordNod = {}
            matrizconect, listconect = [], []
            cargaF, listF = [], []
            tabDados, listmatsec = [], []
            listelemprov, listpropelem = [], []
            CondCont = []
            #contkk = 0
            ################## Obtencao dos dados de entrada pelo modelo CAD ##############
            print('Obtendo dados do arquivo CAD')
            for entity in acad.ActiveDocument.ModelSpace:
                name = entity.EntityName
                if name == 'AcDbBlockReference':
                    HasAttributes = entity.HasAttributes
                    #nome do bloco
                    NomeBl = entity.Name
                    #Ponto de inserção
                    pto = entity.InsertionPoint
                    
            #################### Matriz de coordenadas nodais (malha) ####################
                    if NomeBl == 'NOD_2D':
                        for attrib in entity.GetAttributes():
                            tabCoordNod[attrib.TextString] = (pto[0],pto[1])
            ########################### Matriz de conectividade ###########################
            # formato: matrizconect = array([[Elemento1,nó_inicial,nó_final],[Elemento2,
            # nó_inicial,nó_final],...,[ElementoN,nó_inicial,nó_final]])
                    elif NomeBl == 'ELEM_BAR_2D':
                        for attrib in entity.GetAttributes():
                            if attrib.TagString ==  'BAR_2D':
                                listconect.append(int(attrib.TextString))
                            elif attrib.TagString ==  'NOD_I_2D':
                                listconect.append(int(attrib.TextString))
                            elif attrib.TagString ==  'NOD_F_2D':
                                listconect.append(int(attrib.TextString))
            ############################# Tabela de dados #################################
            #tabDados = [[[Area1, modulo de young1], [elem1, elem3, elem7...]],[[Area2, modulo de young],[elem2, elem5, elem4...]]]
            #tabDados = [[[645.0, 200.0e3],[1,2]],[[645.0, 200.0e3],[3,4]]]
                            elif attrib.TagString ==  'SEC':
                                listmatsec.append(float(attrib.TextString))
                            elif attrib.TagString ==  'MAT':
                                listmatsec.append(float(attrib.TextString))
                           
                       
                        #Preenche a matriz de conectividade       
                        matrizconect.append(listconect)
                        #Preenche a tabela de dados
                        listpropelem.append(listmatsec)
                        listelemprov.append(listconect[0])
                        listpropelem.append(listelemprov)
                        tabDados.append(listpropelem)
                        
                        listconect, listmatsec, listelemprov, listpropelem = [], [], [], []
                        #contkk = contkk + 1
            ######################## Definição do carregamento ###########################
            #cargaF = [[Forca, GDL1], ..., [ForcaN, GDLN]] 
                    elif NomeBl == 'F_NOD_2D':
                        angtheta = float(entity.rotation)
                        for attrib in entity.GetAttributes():
                            if attrib.TagString ==  'F_2D':
                                ForcaPrinc = float(attrib.TextString)
                                CompFx = ForcaPrinc*cos(angtheta)
                                CompFy = ForcaPrinc*sin(angtheta)
                            elif attrib.TagString ==  'INF_NO_2D':
                                Gdlx = 2*int(attrib.TextString) - 1
                                Gdly = 2*int(attrib.TextString)
                        if CompFx != 0.0:         
                            cargaF.append([CompFx,Gdlx])
                        if CompFy != 0.0:
                            cargaF.append([CompFy,Gdly])
                        ForcaPrinc, CompFx, CompFy, Gdlx, Gdly = 0.0, 0.0, 0.0, 0, 0
            
            ############################## Condições de contorno ##########################
            #CondCont = array([1,2,4,7,8], int)
                    elif NomeBl == 'AP_MV_2D':
                        angtheta = float(entity.rotation)
                        for attrib in entity.GetAttributes():
                            if attrib.TagString ==  'INF_NO_2D':
                                Gdlx = 2*int(attrib.TextString) - 1
                                Gdly = 2*int(attrib.TextString)
                                #Por enquanto só funciona com restrições com angulos 0 e 90 (Rever)
                                if int(abs(Gdlx*cos(angtheta))) != Gdlx:
                                    CondCont.append(Gdlx)
                                if int(abs(Gdly*sin(angtheta))) != Gdly:
                                    CondCont.append(Gdly)
                        Gdlx, Gdly = 0.0, 0.0
                    elif NomeBl == 'AP_FIX_2D':
                        angtheta = float(entity.rotation)
                        for attrib in entity.GetAttributes():
                            if attrib.TagString ==  'INF_NO_2D':
                                Gdlx = 2*int(attrib.TextString) - 1
                                Gdly = 2*int(attrib.TextString)
                                CondCont.append(Gdlx)
                                CondCont.append(Gdly)
                        Gdlx, Gdly = 0.0, 0.0
                                    
            ################### Matriz do Elemento de Treliça Plana #######################
            def ElemTrel(E,A,x1,y1,x2,y2):
                l = ((x2-x1)**2 + (y2-y1)**2)**0.5
                CS, S = (x2-x1)/l , (y2-y1)/l
                MatrizRig = (E*A/l)*array([[CS**2,CS*S,-CS**2,-CS*S],[CS*S,S**2,-CS*S,-S**2],[-CS**2,-CS*S,CS**2,CS*S],[-CS*S,-S**2,CS*S,S**2]])
                return MatrizRig
            ###############################################################################
            
            ################### Tensão normal nas barras (elementos) ######################
            def TenDefDeslBar(E,A,x1,y1,x2,y2,qel):
                l = ((x2-x1)**2 + (y2-y1)**2)**0.5
                CS, S = (x2-x1)/l , (y2-y1)/l
                TensaoBar = (E/l)*(-qel[0]*CS - qel[1]*S + qel[2]*CS + qel[3]*S)
                NormalBar = A*TensaoBar
                DeformacaoBar = TensaoBar/E
                DeslocamentoBar = DeformacaoBar * l
                
                return NormalBar, TensaoBar, DeformacaoBar, DeslocamentoBar
            
            #### Resolução de um sistema linear ([K]{U}={R}) pelo método de fatorização de Givens ####
            def sl(Kparcial,VetForca):
                # Ordem da matriz
                n=len(Kparcial) # conta o número de colunas da matriz [Kparcial]
            
                # Inicia variáveis
                k1, k2 = 0, 0
            
                # Fatorização de Givens
                for i in range(n-1):
                    for h in range(i+1,n):
                        if (Kparcial[i][i])**2+(Kparcial[h][i])**2==0:
                            cs=1
                            sn=0
                        else:            
                            # Determina cossenos e senos
                            cs=(Kparcial[i][i])/((Kparcial[i][i])**2+(Kparcial[h][i])**2)**0.5
                            sn=(Kparcial[h][i])/((Kparcial[i][i])**2+(Kparcial[h][i])**2)**0.5
                        for j in range(n):
                            k1,k2 = 0, 0
                            k1,k2 = Kparcial[i][j], Kparcial[h][j]
                            # Cálculo da matriz ~Kparcial ( vai transformando Kparcial em Sg)
                            Kparcial[i][j] = k1*cs + k2*sn
                            Kparcial[h][j] = -k1*sn + k2*cs
                        # Vai transformando VetForca em V  
                        v1, v2 = VetForca[i][0], VetForca[h][0]
                        VetForca[i][0] = v1*cs + v2*sn
                        VetForca[h][0] = -v1*sn + v2*cs
                # Resolução do sistema linear ( obtém U )
                U=zeros([n,1],float)
                for i in range(n):
                    SS=0
                    for j in range(n):
                        SS=SS+(Kparcial[n-1-i][n-1-j]*U[n-1-j])
                    U[n-1-i]=(VetForca[n-1-i][0]-SS)/Kparcial[n-1-i][n-1-i]
            
                return U
            
            ###############################################################################
            
            
            #################### Montagem da matriz global de rigidez #####################
            #Declaração da matriz de zeros
            #print(CondCont)
            print('Solução numérica')
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
                            E, A = tabDados[jh][0][0], tabDados[jh][0][1]
                        
                #Obtém coordenadas dos nós
                #x1, y1 = tabCoordNod[no1-1][0], tabCoordNod[no1-1][1]
                x1, y1 = tabCoordNod[str(no1)][0], tabCoordNod[str(no1)][1]
                #x2, y2 = tabCoordNod[no2-1][0], tabCoordNod[no2-1][1]
                x2, y2 = tabCoordNod[str(no2)][0], tabCoordNod[str(no2)][1]
                #Obtém a matriz de rigidez do elemento corrente
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
                    
            print(Kparcial)        
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
            
            ######################### Determinação das forças nodais #######################
            VetFocaGlogal = zeros([Nglobal,1],float)
            
            for i in range(len(VetFocaGlogal)):
                for j in range(len(VetFocaGlogal)):
                    VetFocaGlogal[i] = VetFocaGlogal[i] + K[i][j]*VetDeslcGlogal[j]
            print('Análise terminada com sucesso')      
            ############################ Pós-processamento ################################
            colunGDLT = (arange(1,Nglobal+1))
            infonode = []
            infodirt = []
            
            for i in range(Nglobal):
                if colunGDLT[i]%2 == 0:
                    infodirt.append('Y')
                    infonode.append(0.5*colunGDLT[i])
                else:
                    infodirt.append('X')
                    infonode.append(0.5*(colunGDLT[i]+1))
            '''        
            respdfdesloc = pd.DataFrame(VetDeslcGlogal, columns = ['Desloc. nodais'] )
            respdfforca = pd.DataFrame(VetFocaGlogal, columns = ['Forcas nodais'])
            
            respdf1 = respdfdesloc.join(respdfforca)
            respdf2 = pd.DataFrame(colunGDLT, columns = ['GDLs'] ).join(respdf1)
            respdf3 = pd.DataFrame(infodirt, columns = ['Direcao'] ).join(respdf2)
            respdf = pd.DataFrame(infonode, columns = ['NO'] ).join(respdf3)
            '''
            respdfdesloc = DataFrame(VetDeslcGlogal, columns = ['Desloc. nodais'] )
            respdfforca = DataFrame(VetFocaGlogal, columns = ['Forcas nodais'])
            
            respdf1 = respdfdesloc.join(respdfforca)
            respdf2 = DataFrame(colunGDLT, columns = ['GDLs'] ).join(respdf1)
            respdf3 = DataFrame(infodirt, columns = ['Direcao'] ).join(respdf2)
            respdf = DataFrame(infonode, columns = ['NO'] ).join(respdf3)
            
            # Limpa as variaveis
            colunGDLT, infonode, infodirt, respdfdesloc, respdfforca = 0,0,0,0,0
            respdf1,respdf2,respdf3 = 0,0,0
            
            print(respdf)
            
            
            ## Tensões, deformações e deslocamentos normais das barras (elementos)
            
            linhaElem, linhaNormal, linhaTensao, linhaDeformacao, linhaDeslocamento, qel = [],[],[],[],[],[]
            for ps in range(len(matrizconect)):
                #Obtém elementos e nós correntes    
                el = matrizconect[ps][0] #Elemento corrente
                no1, no2 = matrizconect[ps][1], matrizconect[ps][2] #Nós do elemento
                
                #Obtem as propriedades do elemento - área de secao e modulo de elasticidade
                for jh in range(len(tabDados)):
                    for hj in range(len(tabDados[jh][1])):
                        if tabDados[jh][1][hj] == el:
                            E, A = tabDados[jh][0][0], tabDados[jh][0][1]
                        
                #Obtém coordenadas dos nós
                x1, y1 = tabCoordNod[str(no1)][0], tabCoordNod[str(no1)][1]
                x2, y2 = tabCoordNod[str(no2)][0], tabCoordNod[str(no2)][1]
                
                qel = [VetDeslcGlogal[2*no1 - 2], VetDeslcGlogal[2*no1 - 1], VetDeslcGlogal[2*no2 - 2], VetDeslcGlogal[2*no2 - 1]]
                
                # Função de Normal, tensão, deformação e deslocamento
                respNTDD = TenDefDeslBar(E,A,x1,y1,x2,y2,qel)
            
                # Preenchendo as respostas dos elementos
                linhaElem.append(el)
                linhaNormal.append(respNTDD[0][0])
                linhaTensao.append(respNTDD[1][0])
                linhaDeformacao.append(respNTDD[2][0])
                linhaDeslocamento.append(respNTDD[3][0])
                        
            dicionarioNTDD = {'Elementos': linhaElem, 'Forca normal': linhaNormal, 'Tensao normal': linhaTensao, 'Deform. normal': linhaDeformacao, 'Desloc. normal': linhaDeslocamento}        
                        
            
            #respdfNTDD = pd.DataFrame.from_dict(dicionarioNTDD)
            respdfNTDD = DataFrame.from_dict(dicionarioNTDD)
            print()
            print(respdfNTDD)       
            
            # Gravando os resultados em um arquivo de saída de dados
            print('Gravando resultados')
            respdf.to_csv('C:/ISTemp/Nodal.csv')
            respdfNTDD.to_csv('C:/ISTemp/Elemento.csv')
            print('Concluído')
        except:
            print('ERRO!')
            print('Análise interrompida.')
            print()
            print('Possíveis erros:')
            print(' 1.Erros de leitura do modelo.')
            print(' 2.Erros de inconsistência do modelo.')
