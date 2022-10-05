# -*- coding: utf-8 -*-
import math
# Q1

def poly_mult(P,Q):
    p=len(P)
    q=len(Q)
    final=[0]*(p+q-1)
    for i in range(p):
        for j in range(q):
            final[i+j]+=P[i]*Q[j]
    return final



def cost_poly_mult(n): 
    return 2*n**2-2*n+1

# Q2

def poly_add(P,Q):
    p=len(P)
    q=len(Q)
    minpq=min(p, q)
    final = [0] * minpq
    if p>q:
         final+=P[q:]
    if p<q:
        final+=Q[p:]
    for i in range(minpq):
        final[i]=P[i]+Q[i]

    return final

         
def neg(P):
    return [-p for p in P]
   
def shift(P,k):
   return [0]*k+P
  
# Q3  
  
def poly_kara_mult(P,Q):
    n=len(P)+len(Q)-2
    if n<=2:
        return poly_mult(P,Q)
    else:
        k=int(math.ceil(n/2))
        A0=P[:k]
        A1=P[k:]
        B0 = Q[:k]
        B1 = Q[k:]
        H0=poly_kara_mult(A0,B0)
        H2=poly_kara_mult(A1,B1)
        add_A=poly_add(A0,A1)
        add_B=poly_add(B0,B1)
        H1=poly_kara_mult(add_A,add_B)

        xk=shift(poly_add(poly_add(H1,neg(H0)),neg(H2)),k)
        x2k = shift(H2,2*k)
        return poly_add(poly_add(H0,xk),x2k)

    
def cost_poly_kara_mult(n):
    if n==1:
        return 1
    if n>=2:
        return 3*cost_poly_kara_mult(math.ceil(n/2))+4*n

# Q4 

def cost_poly_tc3_mult(n):
    if n==1:
        return 1
    if n==2:
        return 3
    else:
        return 5*cost_poly_tc3_mult(math.ceil(n/3))+30*n

# Q5 hybrid
   
def poly_switch_mult(d,P,Q):
    n=len(P)+len(Q)-2
    if n<=d:
        return poly_mult(P,Q)
    else:
        k=int(math.ceil(n/2))
        A0=P[:k]
        A1=P[k:]
        B0 = Q[:k]
        B1 = Q[k:]
        H0=poly_switch_mult(d, A0,B0)
        H2=poly_switch_mult(d, A1,B1)
        add_A=poly_add(A0,A1)
        add_B=poly_add(B0,B1)
        H1=poly_switch_mult(d, add_A,add_B)

        xk=shift(poly_add(poly_add(H1,neg(H0)),neg(H2)),k)
        x2k = shift(H2,2*k)
        return poly_add(poly_add(H0,xk),x2k)

def cost_switch_mult(d,n):
    if n<=d:
        return 2*n**2-2*n+1
    else:
        return 3*cost_switch_mult(d,math.ceil(n/2))+4*n

   
