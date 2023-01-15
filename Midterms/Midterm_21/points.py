#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import math

#Q1

def min_max(A):# This function returns both the minimum and the maximum of A
    n = len(A)
    if n == 1:
        return (A[0],A[0])
    elif n == 2:
        if A[1]>=A[0]:
            return (A[0],A[1])
        else:
            return (A[1],A[0])
    else:
        front = min_max(A[:n//2])
        back = min_max(A[n//2:])
        el1 = 0
        el2 = 0
        if front[0]<=back[0]:
            el1 = front[0]
        else:
            el1 = back[0]
        if front[1]>=back[1]:
            el2 = front[1]
        else:
            el2 = back[1]
        return (el1, el2)

#T(n) = 2T(n//2) + 2
#T(1) = 1
#T(2) = 2
#n+n/2+n/4+n/8+... = 3n/2 comparisons
#O(n) algorithm

#Q2
# This function returns the coordinates of both the top-left and bottom-right corners.
def bounding_box(S):
    x_list = [k[0] for k in S]
    y_list = [k[1] for k in S]
    m1, n1 = min_max(x_list)
    m2, n2 = min_max(y_list)
    return [[m1,n2],[n1,m2]]
#Q3
def lexicographic(p1,p2):
    if (p1[0] < p2[0]):
        return True
    elif (p1[0] == p2[0] ):
        return p1[1] <= p2[1]
    return False

def maxima_set(S):
    n=len(S)
    if n <= 1:
        return S

    k = n // 2
    h1 = maxima_set(S[:k])
    h2 = maxima_set(S[k:])
    q = h2[0]

    for h in h1:
        if q[1]>=h[1]:
            h1.remove(h)
    return h1+h2


def dominate_bs(C, y, left, right):
    if left == right-1:
        if y>=C[0][1]:
            return 1
        else:
            return 0
    mid = (left+right)// 2  # using `(right + left)//2` can lead to an integer overflow
    if y >= C[mid][1]:
        return mid + dominate_bs(C, y, mid, right)
    else:
        return dominate_bs(C, y, left, mid)

def my_y_coordinate(A):
    return A[1]

def dominance_counting(S):
    n = len(S)
    if n == 0:
        return []
    if n == 1:
        return [[S[0], 0]]

    k = n // 2
    s1 = dominance_counting(S[:k])
    s2 = dominance_counting(S[k:])

    C = S[:k]
    C.sort(key=my_y_coordinate)
    R=[]
    for s in s2:
        pt, ct = s
        x, y = pt
        R += [[pt, ct + dominate_bs(C,y,0,len(C))]]

    return s1 + R














