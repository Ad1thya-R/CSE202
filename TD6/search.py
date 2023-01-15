# -*- coding: utf-8 -*-

### For comparing strings

def string_compare(P,S):
    for j in range(len(P)):
        if not P[j] == S[j]:
            return False
    return True


### naive string matcher
def string_match(T, P):
    p=len(P)
    t=len(T)
    pos=[]
    for i in range(t-p+1):
        if string_compare(P,T[i:i+p]):
            pos.append(i)
    return pos

### number of characters
base = 256

### karp_rabin_sum

def hash_string_sum(S):
    return sum([ord(c) for c in S])

def hash_string_sum_update(h, Ti, Tim):
    return h - ord(Ti) + ord(Tim)

def karp_rabin_sum(T,P):
    hp = hash_string_sum(P)
    ht = hash_string_sum(T[:len(P)])
    pos = []
    spur = 0
    for i in range(len(T)-len(P)+1):
        if hp == ht:
            if string_compare(P,T[i:i+len(P)]):
                pos.append(i)
            else:
                spur += 1
        if i < len(T)-len(P):
            ht = hash_string_sum_update(ht, T[i], T[i+len(P)])
    return pos, spur


### karp_rabin_mod

def hash_string_mod(S, q):
    m = len(S)
    d = 256
    return sum([(ord(S[i])%q)*((d%q)**(m-i-1)) for i in range(m)])%q

def hash_string_mod_update(h,q, Ti, Tim, dm):
    d=256
    return (d*(h - ord(Ti)*dm) + ord(Tim))%q

def karp_rabin_mod(T,P, q):
    hp = hash_string_mod(P, q)
    ht = hash_string_mod(T[:len(P)], q)
    pos = []
    spur = 0
    for i in range(len(T)-len(P)+1):
        if hp == ht:
            if string_compare(P,T[i:i+len(P)]):
                pos.append(i)
            else:
                spur += 1
        if i < len(T)-len(P):
            ht = hash_string_mod_update(ht, q, T[i], T[i+len(P)], ((256%q)**(len(P)-1))%q)
    return pos, spur



