import networkx as nx
import itertools

G=nx.Graph()
import time
start_time=time.time()
steps=0
def countVertexDegree(matrix): #Crea una lista con los grados de cada vrtice en el grafo que recibe
    global steps
    degree=[]
    deg=0
    for row in matrix:
        for bit in row:
            if bit==1:
                deg+=1
                steps+=1
        degree.append(deg)
        deg=0
    return degree
    
def buildM(h,g): #Crea una matriz M0 comparando los grados de cada vrtice de los grafos H y G
    m0=[]
    for n in range(len(g)):
        m0.append([])
    for i in range(len(g)):
        for j in range(len(h)):
            m0[i].append((h[j]>=g[i]).real) #1 si el grado del vrtice Vhj >= grado del vrtice Vgi
    return m0

def prune(m,i,j,ag,ah):
    global steps
    #print(i,j,m)
    #print("\n")
    for x in range(len(ag)):
        if(ag[i][x]):
            for y in range(len(ah)):
                steps+=1
                if(m[x][y]*ah[y][j]):
                    return True
    
def permute(m0,row,h,g): #Crea todas las permutaciones de la matriz padre M0 posibles y prueba si son isomrficas
    global steps
    if(row==len(m0)):
        n=0
        for i in range(len(m0[0])):
            for j in range(len(m0)):
                n+=m0[j][i]
                steps+=1
            if(n>1):
                return
            n=0
        
        res=[[sum(a*b for a,b in zip(m0_row,h_col)) for h_col in zip(*h)] for m0_row in m0]
        steps+=((2*len(h)-1)*(len(res)*len(res[0])))
        resTr=[[res[j][i] for j in range(len(res))] for i in range(len(res[0]))]
        arr=[[sum(a*b for a,b in zip(m0_row,resTr_col)) for resTr_col in zip(*resTr)] for m0_row in m0]
        steps+=((2*len(resTr)-1)*(len(arr)*len(arr[0])))
        if(g==arr): #<= para subgrafos inducidos
            for ro in m0:
                print(ro)
            print("\n")
            return True
    else:
        arr1=m0[row][:] #Guarda copia de m0[row]
        arr2=[i for i, x in enumerate(arr1) if x] #Crea una lista con los ndices donde hay 1 en arr1
        for n in range(len(arr2)): #Cambia todos los 1 a 0 excepto el n-simo
            for i in arr2:
                if i!=arr2[n]:
                    m0[row][i]=0
            
            if(prune(m0,row,m0[row].index(1),g,h)):
                if permute(m0,row+1,h,g):
                    return True    
                else:
                    m0[row]=arr1[:]
            else:
                m0[row]=arr1[:]
        return False
def create(formula):
    global steps
    mat = getfor(formula) 
    ah=mat[0]
    ag=mat[1]
    degh=countVertexDegree(ah)
    degg=countVertexDegree(ag)
    m0=buildM(degh,degg)
    
    if (permute(m0,0,ah,ag)):
        pasos=str(steps)
        steps=0
        return("YES!  "+pasos)
    else:
        return("No")
    

            
def getfor(formula):
    
    
   
    retCla=[]
    clauses=formula.split("/")
    
    
    clause1=hacMa(clauses[0][2:-2])
    clause2=hacMa(clauses[1][2:-2])
    retCla.append(clause1)
    retCla.append(clause2)

    
    return retCla

def hacMa(algo):
    
    clauses=algo.split("],[")
    
    tuplas = []
    arr=[]
    for clause in clauses:
        clause = map(int,clause.split(","))
        tuplas.append(clause)
    length=len(tuplas)
    for n in range(length):
        arr.append([])
        for m in range(length):
            arr[n].append(0)
    for v in range(len(tuplas)):
        for ve in tuplas[v]:
            arr[v][ve-1]=1
    return arr 

  
'''def main():
    #ah=[[0,1,0,0],[1,0,1,1],[0,1,0,0],[0,1,0,0]] #Matriz de adyacencia del grafo H
    #ag=[[0,0,1],[0,0,1],[1,1,0]] #Matriz de adyacencia del grafo G
    #ah=[[0,1,0,1,1],[1,0,1,0,1],[0,1,0,1,1],[1,0,1,0,1],[1,1,1,1,0]]
    #ag=[[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]]
    #ah=[[0,1,0,1,1],[1,0,1,0,1],[0,1,0,1,1],[1,0,1,0,1],[1,1,1,1,0]]
    #ag=[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
    #ah=[[0,1,1,0,1],[1,0,1,1,1],[1,1,0,1,1],[0,1,1,0,1],[1,1,1,1,0]]
    #ag=[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
    ah=[[0,1,0,0,0,0,0,0,0,0,0,0,0],[1,0,1,0,0,0,0,0,0,0,0,1,0],[0,1,0,1,0,0,0,0,0,0,0,0,0],[0,0,1,0,1,0,0,0,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0,0,0,1],[0,0,0,0,1,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,1,0,1,0,0,0,0],[0,0,0,0,0,0,0,1,0,1,1,0,0],[0,0,0,0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,1,0,0,0,0],[0,1,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,0,0,1,0]]
    ag=[[0,1,0,0,0,0,0,0],[1,0,0,1,0,0,0,0],[0,0,0,1,0,0,0,0],[0,1,1,0,1,0,0,0],[0,0,0,1,0,1,0,0],[0,0,0,0,1,0,1,1],[0,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0]]
    #Hamiltonian Path
    #ah=[[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0]]
    #ag=[[0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]]
    #Hamiltonian Circuit
    #ah=[[0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 1], [0, 0, 1, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0], [1, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 0, 0, 1, 0]]
    #ag=[[0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 0, 1, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0, 1, 0]]
    #ah=[[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0]]
    #ag=[[0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]]
    degh=countVertexDegree(ah)
    degg=countVertexDegree(ag)
    m0=buildM(degh,degg)
    #for row in m0:
    #    print(row)
    #print("\n")
    if (permute(m0,0,ah,ag)):
        print("YES!")
    else:
        print("No")
    print("--- %s seconds ---" % (time.time() - start_time))
main()'''