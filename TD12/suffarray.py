# -*- coding: utf-8 -*-

def str_compare(a, b):
    N = min(len(a),len(b))
    for i in range(N):
        if a[i] < b[i]:
            return -1
        elif a[i] > b[i]:
            return 1

    return len(a)-len(b)

def str_compare_m(a,b, m):
    if len(a) >= m and len(b) >= m:
        # len(a) >= m and len(b) >= m
        return str_compare(a[:m], b[:m])
    else:
        # len(a) < m or len(b) > m
        return str_compare(a,b)

def longest_common_prefix(a, b):
    N = min(len(a),len(b))
    for i in range(N):
        if a[i] != b[i]:
            return i
    return N


class suffix_array:
    # Question 1
    def __init__(self, t):
        self.T = t
        self.N = len(t)
        self.suffId = [i for i in range(self.N)]

        # TODO: order suffId by lexicographic order of suffixes
        order = [i for i in range(self.N)]
        order.sort(key=lambda i: self.suffix(i))
        self.suffId = order

    def suffix(self, i):
        return self.T[self.suffId[i]:]

    # Question 2
    def findL(self, S):
        '''
        Find the leftmost suffix of T that starts with S
        :param S: string to search
        :return: index of leftmost suffix of T that starts with S or N if empty
        '''
        L=0
        R=self.N
        while L<R:
            M=(L+R)//2
            if str_compare_m(self.suffix(M),S,len(S))<0:
                L=M+1
            else:
                R=M
        return L

    # Question 2
    def findR(self,S):
        '''
        Find the rightmost suffix of T that starts with S
        :param S: string to search
        :return: index of rightmost suffix of T that starts with S or N if empty
        '''
        L=0
        R=self.N
        while L<R:
            M=(L+R)//2
            if str_compare_m(self.suffix(M),S,len(S))<=0:
                L=M+1
            else:
                R=M
        return R

    def findLR(self,S):
        return (self.findL(S),self.findR(S))

# Question 4
def KWIC(sa, S, c = 15):
    '''
    Find all occurrences of S in T and return them as a list of context strings
    :param sa: suffix array
    :param S: string to search
    :param c: context size
    :return: list of context strings
    '''
    L, R = sa.findLR(S)
    if L==R:
        return []
    return [sa.T[max(0,sa.suffId[i]-c):sa.suffId[i]+c+len(S)] for i in range(L,R)]

# Question 5
def longest_repeated_substring(sa):
    '''
    Find the longest repeated substring in T
    :param sa: suffix array
    :return: longest repeated substring
    '''
    LRS = ""
    for i in range(1,sa.N):
        lcp = longest_common_prefix(sa.suffix(i-1), sa.suffix(i))
        if lcp > len(LRS):
            LRS = sa.suffix(i)[:lcp]
    return LRS