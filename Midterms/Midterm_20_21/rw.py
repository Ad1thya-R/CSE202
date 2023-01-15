# -*- coding: utf-8 -*-
import random

class Graph:
    def __init__(self, L): 
    # vertices are labeled from 0 to n-1  
    # L[i] gives the list of neighbours of vertex i
        self.L=L
        self.n=len(L)

    # draws a random neighbour of vertex i
    def random_neighbour(self,i):
        return random.choice(self.L[i])
        
    # draws a random walk of length k, starting from 0    
    def random_walk(self,k):
        walk = [0]
        for i in range(k):
            walk += [self.random_neighbour(walk[i])]
        return walk
    
    # draws a random walk (starting from 0) till all vertices are visited    
    def random_walk_till_covered(self):
        walk = [0]
        visited = [k for k in range(1,self.n)]
        i=0
        while len(visited)!=0:
            rand_nb = self.random_neighbour(walk[i])
            if rand_nb in visited:
                visited.remove(rand_nb)
            walk+=[rand_nb]
            i+=1
        return walk
     
    # draws a random spanning tree
    def random_tree(self):
        walk = [0]
        visited = [k for k in range(1, self.n)]
        span = {}
        i = 0
        while len(visited) != 0:
            rand_nb = self.random_neighbour(walk[i])
            if rand_nb in visited:
                visited.remove(rand_nb)
                span[rand_nb] = walk[i]
            walk += [rand_nb]
            i += 1
        return span