import random
import math
from UF import *

nr_calls=0

class WG:
    def __init__(self, L): # L is the list of edges
        L.sort(key= lambda e: e[2])
        self.edges=L
        self.adj={}
        for x in L:
            if x[0] not in self.adj:
                self.adj[x[0]]={x[1]:x[2]}
            else:
                self.adj[x[0]][x[1]]=x[2]
            if x[1] not in self.adj:
                self.adj[x[1]]={x[0]:x[2]}
            else:
                self.adj[x[1]][x[0]]=x[2]

    def min_cycle_aux(self,w,L,S):
        global nr_calls
        nr_calls=nr_calls+1
        a=L[0]; b=L[-1]
        if len(S)==0:
            if a not in self.adj[b]:
                return (math.inf,[])
            else:
                Lc=L[:]
                Lc.append(a)
                return (w+self.adj[b][a],Lc)
        res=(math.inf,[])
        for x in self.adj[b]:
            if x in S:
                L.append(x); S.remove(x)
                outx=self.min_cycle_aux(w+self.adj[b][x],L,S)
                L.pop(); S.add(x)
                if outx[0]<res[0]:
                    res=outx
        return res

    def min_cycle(self):
        global nr_calls
        nr_calls=0
        S=self.vertex_set()
        a=S.pop()
        res = self.min_cycle_aux(0,[a],S)
        print("number of calls to min_cycle_aux: "+str(nr_calls))
        return res

    def vertex_set(self): # returns the set with all vertices of the graph
        return set(self.adj.keys())

    def lower_bound(self,w,L,S):
        # returns low(L), with w the cost of L, and S the set of vertices not in L
        a, b = L[0], L[-1]
        min_a, min_b = math.inf, math.inf
        for x in self.adj[a]:
            if x in S and self.adj[a][x]<min_a:
                min_a=self.adj[a][x]
        for x in self.adj[b]:
            if x in S and self.adj[b][x]<min_b:
                min_b=self.adj[b][x]
        return w+min_a+min_b+self.weight_min_tree(S)

    def min_cycle_aux_using_bound(self,bestsofar,w,L,S):
        a, b = L[0], L[-1]
        if len(S)==0:
            if a not in self.adj[b]:
                return (math.inf,[])
            elif w+self.adj[b][a]>=bestsofar:
                return (math.inf,[])
            else:
                Lc=L[:]
                Lc.append(a)
                return (w+self.adj[b][a],Lc)

        if self.lower_bound(w,L,S)>=bestsofar:
            return (math.inf,[])

        res=(math.inf,[])
        for x in self.adj[b]:
            if x in S:
                L.append(x); S.remove(x)
                outx=self.min_cycle_aux_using_bound(bestsofar,w+self.adj[b][x],L,S)
                L.pop()
                S.add(x)
                if outx[0]<res[0]:
                    res=outx
                if outx[0]<bestsofar:
                    bestsofar=outx[0]
        return res

    def min_cycle_using_bound(self):
        S=self.vertex_set()
        a=S.pop()
        res = self.min_cycle_aux_using_bound(math.inf,0,[a],S)
        return res

    def weight_min_tree(self,S): # mincost among all trees whose spanned vertices are those in S
        if len(S)==1:
            return 0
        if len(S)==2:
            L=list(S)
            if L[0] in self.adj[L[1]]:
                return self.adj[L[0]][L[1]]
            else: return math.inf
        uf=UF(S)
        nr_components=len(S)
        weight=0
        for e in self.edges:
            if e[0] in S and e[1] in S:
                if uf.find(e[0])!=uf.find(e[1]):
                    weight=weight+e[2]
                    uf.union(e[0],e[1])
                    nr_components=nr_components-1
                    if nr_components==1:
                        return weight
        return math.inf

    def induce_by_subset(self,S): # reduces self.adj to keep only the edges with both ends in S
        new_adj={}
        for x in self.adj:
            for y in self.adj[x]:
                if x in S and y in S:
                    if x not in new_adj:
                        new_adj[x]={y:self.adj[x][y]}
                    else:
                        new_adj[x][y]=self.adj[x][y]
                    if y not in new_adj:
                        new_adj[y]={x:self.adj[y][x]}
                    else:
                        new_adj[y][x]=self.adj[y][x]
        self.adj=new_adj

    def display(self):
        print("Graph has "+str(len(self.adj))+" vertices")
        print()
        for x,y in self.adj.items():
            print("Neighbours of "+str(x)+":")
            for t,u in y.items():
                print(str(t)+" with weight "+str(u))
            print()



##############################
## Approximation algorithms ##
##############################

### Provided

    def random_cycle(self):
        # construct a random cycle
        T = [x for x in self.adj]
        random.shuffle(T)
        return (T, self.eval_cycle(T))

    def eval_cycle(self, T):
        # evaluate a cycle
        w = 0
        for i in range(1,len(self.adj)):
            w += self.adj[T[i - 1]][T[i]]

        w += self.adj[T[len(self.adj) - 1]][T[0]]
        return w

    def get(self, T, i):
        # returns the node at L[i] (cyclic: Safe if i < 0 or i > len(L))
        return T[i % len(self.adj)]

#########################
## Greedy construction ##
#########################

    ## Question 1
    def greedily_select_edges(self):
        deg = dict().fromkeys(self.adj.keys(), 0)
        uf = UF(self.adj.keys())
        C = set()
        for (u, v, w) in self.edges:
            if deg[u] <= 1 and deg[v] <= 1:
                if not uf.is_connected(u, v) or len(C) == len(self.adj) - 1:
                    C.add((u, v, w))
                    uf.union(u, v)
                    deg[u] += 1
                    deg[v] += 1
        return C

    ## Question 2
    def build_cycle_from_edges(self, edges):
        T = []
        W = 0
        neighborhood = dict()
        for (u, v, w) in edges:
            neighborhood[v] = neighborhood.get(v, set()).union({u})
            neighborhood[u] = neighborhood.get(u, set()).union({v})
            W += w
        for (u, v, w) in edges:
            T+= [u]
            T+= [v]
            neighborhood[u]-={v}
            neighborhood[v]-={u}
            break
        while len(T) < len(edges):
            T += [neighborhood[T[-1]].pop()]
            neighborhood[T[-1]] -= {T[-2]}
        return (W, T)

    ## Greedy approximation algorithm
    def greedy_min(self):
        select_edges = self.greedily_select_edges()
        return self.build_cycle_from_edges(select_edges)

###########
## 2-opt ##
###########

    ## Question 3
    def evaluate_flip(self, T, i, j):
        return self.adj[self.get(T, i - 1)][self.get(T, i)] + self.adj[self.get(T, j)][self.get(T, j + 1)] - \
               self.adj[self.get(T, i - 1)][self.get(T, j)] - self.adj[self.get(T, i)][self.get(T, j + 1)]


    ## Question 4
    def find_best_opt2(self, T):
        two_nodes = None
        g = 0
        for i in range(len(T)):
            for j in range(1, len(T) - 1):
                temp = self.evaluate_flip(T, i, i + j)
                if temp > g:
                    g = temp
                    two_nodes = (self.get(T, i), self.get(T, i + j))
        return (two_nodes, g)

    ## Question 5
    def opt_2(self, W, T):
        two_nodes, g = self.find_best_opt2(T)
        if g:
            W -= g
            self.flip(T, T.index(two_nodes[0]), T.index(two_nodes[1]))
        return (W, T)

    ## Perform a flip in the list of nodes
    def flip(self, T, i, j):
        k = j + 1
        #reverse T[i:k]
        while i < k:
            T[i], T[k] = T[k], T[i]
            i += 1
            k -= 1

    ## Question 6
    def neighborhood_search_opt2(self, W, T):
        while self.find_best_opt2(T)[0]:
            W, T = self.opt_2(W, T)
        return (W, T)
