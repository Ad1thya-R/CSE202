# -*- coding: utf-8 -*-

import math

def binary_search_rec(A,v,left,right):
    if (right >= left):
        mid = left + (right - left)//2 # using `(right + left)//2` can lead to an integer overflow
        if (v == A[mid]):
            return mid
        elif (v < A[mid]):
            return binary_search_rec(A,v,left,mid-1)
        else:
            return binary_search_rec(A,v,mid+1,right)
    
    return -1
        
## Q1 ##
def binary_search(A,v):
    """iteratively solve binary search"""

    left=0
    right=len(A)-1
    while (right >= left):
        mid = left + (right - left)//2
        if (v == A[mid]):
            return mid
        elif (v < A[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return -1

def cost_binary_search(n):
    if n==0:
        return 1
    if n==1:
        return 3
    return cost_binary_search(math.ceil(n/2)) + 3
    
## Q2 ##
def ternary_search(A,v):
    """iteratively solve ternary search"""
    left=0
    right=len(A)-1
    while (right >= left):
        mid1 = left + (right - left)//3
        mid2 = right - (right - left)//3
        if (v == A[mid1]):
            return mid1
        elif (v == A[mid2]):
            return mid2
        elif (v < A[mid1]):
            right = mid1 - 1
        elif (v > A[mid2]):
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1
    return -1


def cost_ternary_search(n):
    if n==0:
        return 1
    if n==1:
        return 5
    return cost_ternary_search(math.ceil(n/3)) + 5
    
def cost_binary_search_real(A,v):
    if len(A) == 0: return 0

    left = 0
    right = len(A) - 1
    cost =  0
    while (right >= left):
        mid = left + (right - left)//2
        if (v == A[mid]):
            return cost + 1
        elif (v < A[mid]):
            right = mid - 1
            cost+=2
        else:
            left = mid + 1
            cost += 2

    return cost

def cost_ternary_search_real(A,v):
    if len(A) == 0: return 0

    left = 0
    right = len(A) - 1
    cost =  0
    while (right >= left):
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        if (v == A[mid1]):
            return cost + 1
        elif (v == A[mid2]):
            return cost + 2
        elif (v < A[mid1]):
            right = mid1 - 1
            cost+=3
        elif (v > A[mid2]):
            left = mid2 + 1
            cost+=4
        else:
            left = mid1 + 1
            right = mid2 - 1
            cost+=4
    return cost

## Q3 ##
#helper function to carry out binary search on range [2**(k-1),2**k]
def binary_search_bounds(B,left,right,x):
    while (right >= left):
        mid = left + (right - left) // 2
        if (x == B[mid]):
            return mid
        elif (x < B[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return -1

def exponential_search(A,x):
    """iteratively solve binary search"""

    # base case
    if not A:
        return -1

    bound = 1

    # find the range in which key `x` would reside
    while bound < len(A) and A[bound] < x:
        bound *= 2  # calculate the next power of 2

    # call binary search on A[bound/2 … min(bound, n-1)]
    return binary_search_bounds(A, bound // 2, min(bound, len(A) - 1), x)


def cost_exponential_search(n):
    return math.ceil(math.log(n,2)) + cost_binary_search(2**math.ceil(math.log(n,2)))

## Q4 ##
def interpolation_search(A,v):
    """iteratively solve interpolation search"""
    if A[0] == v:
        return 0
    elif len(A)==1:
        return -1
    left=0
    right=len(A)-1
    while (right >= left):
        mid = left + ((right - left)//(A[right]-A[left]))*(v-A[left])
        if (v == A[mid]):
            return mid
        elif (v < A[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return -1

## Q6 ##
def findFirstOccurrence(A, v):
    left = 0
    right = len(A) - 1
    first = len(A) - 1
    while (right >= left):
        mid = left + (right - left) // 2
        if ((mid==0 or A[mid-1]<v) and v == A[mid]):
            first = mid
            return first
        elif (v < A[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return -1



def findLastOccurrence(A, v):
    n=len(A)
    left = 0
    right = n - 1
    last = 0
    while (right >= left):
        mid = left + (right - left) // 2
        if ((mid==n-1 or A[mid+1]>v) and v == A[mid]):
            last = mid
            return last
        elif (v < A[mid]):
            right = mid - 1
        else:
            left = mid + 1
    return -1

## Q7 ##
def findKClosestElements(A, x, k):
    l, r = 0, len(A) - k
    while l < r:
        m = (l + r) // 2
        if x - A[m] > A[m + k] - x:
            l = m + 1
        else:
            r = m
    return A[l:l + k]

## Q8 ##
def findFrequency(A):
    freq={}
    l = 0
    r = len(A) - 1
    def helper(nums,left, right, freq={}):
        if left > right:
            return

        # if every element in sublist nums[left…right] is equal,
        # then increment the element's count by `n`
        if nums[left] == nums[right]:

            count = freq.get(nums[left])
            if count is None:
                count = 0

            freq[nums[left]] = count + (right - left + 1)
            return

        mid = (left + right) // 2

        # divide the list into left and right sublist and recur
        helper(nums, left, mid, freq)
        helper(nums, mid + 1, right, freq)
    helper(A,l,r,freq)
    return freq


