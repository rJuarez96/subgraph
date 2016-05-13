import networkx as nx
import itertools

G=nx.Graph()

def getfor(formula):
    formula = formula[1:-1]
    clauses = formula.split("),(")
    tuplas = []
    for clause in clauses:
        clause = tuple(map(int,clause.split(",")))
        tuplas.append(clause)
    return tuplas
        
def connected(tup):
    unconnected = list(tup)
    flag = True
    for vertex in tup:
        for test in unconnected:
            if vertex == test:
                continue
            if not G.has_edge(vertex,test):
                flag = False
    return flag
        
def create(formula):
    g = getfor(formula)
    G.add_edges_from(g)
    max_len_clique = 0;
    max_clique = []
    tuples = []
    for i in xrange(3,len(G.nodes())):
         tuples.extend(list(itertools.combinations(G.nodes(),i)))
    for tup in tuples:
        if connected(tup):
            if(len(tup)>max_len_clique):
                max_clique = tup;
                max_len_clique = len(tup)
    return max_clique
