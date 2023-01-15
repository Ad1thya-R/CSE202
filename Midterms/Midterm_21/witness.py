import random
import math
import numpy as np
#######################################################################################################################################
#Functions split, merge, add_matrix and sub_matrix are given
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

###################################################################################################################
a1= [[1,1], [1,0]]
b1= [[0,1], [1,0]]
def compute_witness_trivial(A,B):
    n=len(A)
    res = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if A[i][k] == 1 and B[k][j] == 1:
                    res[i][j] = k+1
    return res

#complexity is O(n^3) due to the 3 nested for loops

#print(compute_witness_trivial(a1,b1))
def expose_column(A):
    n = len(A)
    W = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            W[i][j] = (j + 1) * A[i][j]
    return W
#print(expose_column(a1))

def compute_witness_unique(A,B):
    A_hat = expose_column(A)
    return mult_matrix(A_hat,B)
#print(compute_witness_unique(a1,b1))
#complexity is O(n^3) due to the 3 nested for loops in matrix mult


nul_col = [[1,1,1],[1,1,0],[0,1,1]]
r_test = {1,2}

def nullify_columns(A, R):
    n=len(A)
    res = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for k in range(n):
            if (k+1) in R:
                res[i][k] = A[i][k]
            else:
                continue
    return res
#print(nullify_columns(nul_col, r_test))

def nullify_rows(B,R):
    n=len(B)
    res = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for k in range(n):
            if (k+1) in R:
                res[k] = B[k]
            else:
                continue
    return res
#print(nullify_rows(nul_col, r_test))

a2=[[1,1,1],
    [1,1,0],
    [0,1,1]]

b2=[[1,0,1],
    [0,1,0],
    [0,1,1]]
def compute_witness_restricted(A,B,R):
    ar = nullify_columns(A,R)
    br = nullify_rows(B, R)
    return compute_witness_unique(ar,br)
#complexity is again O(n^3) due to the matrix mult with nullification only being O(n^2)
#print(compute_witness_restricted(a2,b2,[1,2]))
'''
The probability that R contains exactly one witness is higher than 1/2e
Thus the probability of R being wrong the first time is (1-1/2e)

Then if we repeat the independent randomisation 2e*log(n) times,
The probability of failure is (1-1/(2e))^{2e*log(n)), which tends to 0 as n gets large
'''
def sample(r,n):
    X = [i+1 for i in range(n)]
    for i in range(n):
        j = random.randint(i,n-1)
        X[i], X[j] = X[j], X[i]
    return X[:r]
'''
ten_occur = 0
for i in range(10000):
    if 10 in sample(3,10):
        ten_occur+=1
print(ten_occur)
'''
def neg_mat(A):
    n=len(A)
    res = [[0 for i in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
                    res[i][j] = -A[i][j]
    return res


def compute_witness_random(A,B):
    n = len(A)
    log = math.log(n)
    W = neg_mat(mult_matrix(A,B))
    for t in range(int(log)+1):
        r=2**t
        for _ in range(int(2*math.e*log)):
            R = sample(r,n)
            WR = compute_witness_restricted(A,B,R)
            for i in range(n):
                for j in range(n):
                    k = WR[i][j] - 1
                    if W[i][j] < 0 and A[i][k] * B[k][j] == 1:
                        W[i][j] = WR[i][j]
    for i in range(n):
        for j in range(n):
            if W[i][j] < 0:
                for k in range(n):
                    if A[i][k] * B[k][j] == 1:
                        W[i][j] = k + 1
    return W

#print(compute_witness_random(a2,b2))