import math
import random

## Question 5 ##
def random_element(dict):
    Num = 0
    for x in dict:
        Num += dict[x]
    i = random.randint(1, Num)
    for x in dict:
        if i <= dict[x]:
            return x
        else:
            i = i - dict[x]

## Question 7 ##
def random_cut(m):
    n = len(m.adj)
    par = {}
    for x in m.adj:
        par[x] = []
    for _ in range(n - 2):
        (i, j) = m.random_edge()
        m.contract(i, j)
        par[i] = par[i] + [j] + par[j]
        del (par[j])
    x = next(iter(par))
    return [m.deg[x], [x] + par[x]]

def mincut_karger(L, p): # p is the desired error bound
    n = L[0]
    i = 2 / n / (n - 1)  # proba success at each trial is at least p
    k = math.ceil(math.log(p) / math.log(1 - i))
    best = math.inf
    best_cut = []
    for _ in range(k):
        m = MultiGraph(L)
        res_trial = random_cut(m)
        if res_trial[0] < best:
            best = res_trial[0]
            best_cut = res_trial[1]
    return [best, best_cut]

## Contains Questions 4 and 6 ##
class MultiGraph:
    def __init__(self, L):
        self.adj = {}
        self.deg = {}
        for x in L[1]:
            if x[0] not in self.adj:
                self.adj[x[0]] = {x[1]: x[2]}
                self.deg[x[0]] = x[2]
            else:
                self.adj[x[0]][x[1]] = x[2]
                self.deg[x[0]] += x[2]
            if x[1] not in self.adj:
                self.adj[x[1]] = {x[0]: x[2]}
                self.deg[x[1]] = x[2]
            else:
                self.adj[x[1]][x[0]] = x[2]
                self.deg[x[1]] += x[2]

    def subset_from_integer(self, i):# i is an integer between 1 and 2^n - 2, with n the number of vertices
        subset = {}
        for x in self.adj:
            if i % 2 == 1:
                subset[x] = True
            i = i >> 1
        return subset

    def cutsize(self, i):# i is an integer between 1 and 2^n - 2, with n the number of vertices
        subset = self.subset_from_integer(i)
        res = 0
        for x, y in self.adj.items():
            for t, u in y.items():
                if x in subset and not t in subset:
                    res += u
        return [res, [x for x in subset]] 

    def display(self):
        for x, y in self.adj.items():
            print("Neighbors of " + str(x) + ", which has degree " + str(self.deg[x]))	
            for t, u in y.items(): 
                print(str(t) + " with multiplicity " + str(u))
    
    ## Question 4 ##
    def contract(self, i, j):# contracts edge i, j (i absorbs j)
        mult_edge = self.adj[i][j]
        del self.adj[j][i]
        del self.adj[i][j]
        self.deg[i] -= mult_edge
        for x, y in self.adj[j].items():
            if x in self.adj[i]:
                self.adj[i][x] += y
                self.adj[x][i] += y
            else:
                self.adj[i][x] = y
                self.adj[x][i] = y
            del self.adj[x][j]
            self.deg[i] += y
        del self.adj[j]
        del self.deg[j]

        ## Question 6.1 ##
    def random_vertex(self):
        return random_element(self.deg)

    ## Question 6.2 ##
    def random_edge(self):
        i = self.random_vertex()
        j = random_element(self.adj[i])
        return (i, j)
