#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


#Q6
def mult_matrix (A , B ):
	"""
	:param A: matrix of size a x n
	:param B: matrix of size n x b
	:return: the product of the matrices A and B
	"""
	# we assume that A and B are non - empty matrices
	m = len ( A )
	n = len ( A [0])

	#naive matrix multiplication algorithm
	p = len ( B [0])
	C = [ None ] * m
	for i in range ( m ):
		C [ i ] = [0] * p
		for k in range ( p ):
			for j in range ( n ):
				C[i][k] += A[i][j] * B[j][k]
	return C



#Q7
def cost_mult_matrix(n):
    return 2*n**3
#Functions split, merge, add_matrix and sub_matrix are given
def split(A):
    A=np.array(A)
    row, col = A.shape
    row2, col2 = row//2, col//2
    return A[:row2, :col2].tolist(), A[:row2, col2:].tolist(), A[row2:, :col2].tolist(), A[row2:, col2:].tolist()

def merge(a,b,c,d):
    return np.vstack((np.hstack((a, b)), np.hstack((c, d)))).tolist()

#Computes the matrix A+B
def add_matrix(A,B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
                C[i][j] = A[i][j] + B[i][j]
    return C

#Computes the matrix A-B
def sub_matrix(A,B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
                C[i][j] = A[i][j] - B[i][j]
    return C

#Q8
def strassen(A,B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    else:
        a, b, c, d = split(A)
        e, f, g, h = split(B)
        p1 = strassen(a, sub_matrix(f, h))
        p2 = strassen(add_matrix(a, b), h)
        p3 = strassen(add_matrix(c, d), e)
        p4 = strassen(d, sub_matrix(g, e))
        p5 = strassen(add_matrix(a, d), add_matrix(e, h))
        p6 = strassen(sub_matrix(b, d), add_matrix(g, h))
        p7 = strassen(sub_matrix(a, c), add_matrix(e, f))
        a11 = add_matrix(sub_matrix(add_matrix(p5, p4), p2), p6)
        a12 = add_matrix(p1, p2)
        a21 = add_matrix(p3, p4)
        a22 = sub_matrix(sub_matrix(add_matrix(p5, p1), p3), p7)
        return merge(a11, a12, a21, a22)

#Q9
def cost_strassen(n):
    if n == 0:
        return 1
    else:
        return 7*cost_strassen(n-1)+18*4**(n-1)


#Q10
def convert_01(A):
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i][j] != 0:
                A[i][j] = 1
    return A

#Q11
def transitive_closure(A):
    n = len(A)
    B = [[0 for i in range(n)] for j in range(n)]
    for i in range(len(B)):
        for j in range(len(B[0])):
            if i == j:
                B[i][j] = 1
    R = add_matrix(A, B)
    R=convert_01(R)
    C=R
    for _ in range(n - 1):
        C = strassen(C, R)
    return C


def matrix_mult(A, B):
    n = len(A)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C







