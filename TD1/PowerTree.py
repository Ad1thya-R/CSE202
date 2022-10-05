# -*- coding: utf-8 -*-

class PowerTree:
    def __init__(self): 
        self.layers=[[1]]
        self.parent={1:1}
    
    def draw_tree(self):
        for i in range(len(self.layers)):	
            print("layer",i)
            for j in self.layers[i]: print(j,"->",self.parent[j])  
  	
    def path_from_root(self,k):
        if k not in self.parent: return -1
        res = [k]
        while (k != 1):
            k = self.parent[k]
            res = [k] + res
        return res
    
    def add_layer(self):
        tab1 = self.layers[-1]
        tab2 = []
        for j in tab1:
            for h in self.path_from_root(j):
                k = j + h
                if k not in self.parent:
                    tab2.append(k)
                    self.parent[k] = j
        self.layers.append(tab2)
