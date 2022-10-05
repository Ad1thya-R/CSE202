# -*- coding: utf-8 -*-

import math
from PowerTree import *

## Q1 ##
def bin_pow(x,n):
    y=1
    if n==0:
        return 1
    if n==1:
        return x
    else:
        if n%2==0:
            y=(bin_pow(x,n//2))**2
        else:
            y=x*(bin_pow(x,n//2))**2
    return y

## Q2 ##
def cost_bin_pow(n):
    if n==0 or n==1:
        return 0
    else:
        if n%2==0:
            return 1 + cost_bin_pow(n//2)
        else:
            return 2 + cost_bin_pow(n//2)

## Q3 ##
def smallest_factor(n):
    for i in range(2,int(n**(1/2))+1):
        if n/i-int(n/i)==0:
            return i
    return -1
## Q4 ##
def factor_pow(x,n):
    if n == 0:
        return 1
    if n == 1:
        return x
    prime=smallest_factor(n)
    if prime==-1:
        return x*factor_pow(x,n-1)
    else:
        return factor_pow(factor_pow(x,prime),n/prime)

## Q5 ##
def cost_factor_pow(n):
    prime=smallest_factor(n)
    if n==0 or n==1:
        return 0
    else:
        if prime==-1:
            return 1 + cost_factor_pow(n-1)
        else:
            return cost_factor_pow(prime)+cost_factor_pow(n/prime)

## Q6 ##
def power_from_chain(x,chain):
    l=len(chain)
    powers={1:x}
    for m in range(1,l):
        k=chain[m]
        j=chain[m-1]
        i=k-j
        powers[k]=powers[j]*powers[i]
    return powers[chain[-1]]

## Q8 ##

def power_tree_chain(n):
    tree = PowerTree()
    while n not in tree.parent:
        tree.add_layer()
    return tree.path_from_root(n)

def power_tree_pow(x,n):
    if n == 0:
        return 1
    return power_from_chain(x,power_tree_chain(n))
    	   
def cost_power_tree_pow(n):
    if n == 0:
        return 0
    chain = power_tree_chain(n)
    return len(chain) - 1

## Q9 ##  
def compare_costs(m):
    return f"Cost bin pow: {cost_bin_pow(m)}, Cost factor pow: {cost_factor_pow(m)}, Cost power tree pow: {cost_power_tree_pow(m)}"

for i in range(22,30):
    print(compare_costs(i))
