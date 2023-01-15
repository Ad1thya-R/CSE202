# -*- coding: utf-8 -*-

import random
import math
from UF import *

nr_calls = 0
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

    # QUESTION 1

    def min_cycle_aux(self,w,L,S):
        '''
        Check every hamiltonian cycle starting with L and ending with L[0] and return the one of smallest weight
        '''
        min_cyc = (math.inf, [])
        if not S:
            if L[-1] in self.adj[L[0]]:
                return (w + self.adj[L[0]][L[-1]], L + [L[0]])
            return min_cyc
        for v in S:
            if L and v not in self.adj[L[-1]]:
                continue
            S.remove(v)
            new_weight = w + (self.adj[L[-1]][v] if L else 0)
            min_cyc = min(min_cyc, self.min_cycle_aux(new_weight, L + [v], S))
            S.add(v)
        return min_cyc

    def verts(self):
        return set(self.adj.keys())
    # QUESTION 2
    def min_cycle(self):
        S = self.verts()
        return self.min_cycle_aux(0, [], S)

    '''
    Question 3
    
    Any path that contains L must be of the form 
    L[0] -> L[1] -> ... -> L[-1] -> s_1 -> ... s_k -> L[0] where S= {s_i}
    The cost of going from L[0] to L[-1] is w. Going from
    L[-1] to s_1 is at least w_end. The cost of the path s_1, ..., s_k must be at least
    w_S, as any path is also a spanning tree so its cost must be at least the minimal spanning tree cost.
    Finally, the cost of going from s_k to L[0] is at least w_start.
    Then sum the cost of all parts of the path.
    '''

    # QUESTION 4
    def lower_bound(self,w,L,S): # returns low(L), with w the cost of L, and S the set of vertices not in L
        try:
            w_start = min([self.adj[L[0]][v] for v in S if v in self.adj[L[0]]])
            w_end = min([self.adj[L[-1]][v] for v in S if v in self.adj[L[-1]]])
        except:
            w_start = math.inf
            w_end = math.inf
        wS = self.weight_min_tree(S)

        return w+w_start+w_end+wS



    # QUESTION 5
    def min_cycle_aux_using_bound(self,bestsofar,w,L,S):
        '''
        complete min cycle aux using lower bound function
        :param bestsofar:
        :param w:
        :param L:
        :param S:
        :return:
        '''
        min_weight = math.inf
        min_cycle = []
        if len(S) == 0:
            if L[0] in self.adj[L[-1]]:
                return (w + self.adj[L[0]][L[-1]], L + [L[0]])
            else:
                return (math.inf, [])
        else:
            low = self.lower_bound(w, L, S)
            if low < min_weight:
                min_weight, min_cycle = math.inf, []
                for x in S:
                    if x in self.adj[L[-1]]:
                        new_S = S - {x}
                        new_L = L + [x]
                        new_w = w + self.adj[L[-1]][x]
                        (w_1, c_1) = self.min_cycle_aux_using_bound((min_weight, min_cycle), new_w, new_L, new_S)
                        if w_1 < min_weight:
                            min_weight, min_cycle = w_1, c_1
            return (min_weight, min_cycle)


    def min_cycle_using_bound(self):
        '''
        return hamiltonian cycle of smallest weight
        :return: tuple : minimum
        use the method min_cycle_aux_using_bound
        '''
        best_so_far = (math.inf, [])
        for x in self.adj:
            (w_1, c_1) = self.min_cycle_aux_using_bound(best_so_far, 0, [x], set(self.adj) - {x})
            if w_1 < best_so_far[0]:
                best_so_far = (w_1, c_1)
        return best_so_far

#################################################################
## Auxiliary methods
#################################################################

    def weight_min_tree(self,S): # mincost among all trees whose spanned vertices are those in S
        if len(S)==1: return 0
        if len(S)==2:
            L=list(S)
            if L[0] in self.adj[L[1]]: return self.adj[L[0]][L[1]]
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
        print(self.edges)
        for x,y in self.adj.items():
            print("Neighbours of "+str(x)+":")
            for t,u in y.items():
                print(str(t)+" with weight "+str(u))
            print()
