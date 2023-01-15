# -*- coding: utf-8 -*-

from uf import Rank_UF
import random
import math
    
def Erdos_Renyi(N):
    '''
        TO IMPLEMENT
    '''
    uf = Rank_UF(N)
    count = 0
    while uf.count > 1:
        count += 1
        i,j = random.randint(0,N-1),random.randint(0,N-1)
        while i==j:
            j = random.randint(0,N-1)
        if not uf.is_connected(i,j):
            uf.union(i,j)
    return count


