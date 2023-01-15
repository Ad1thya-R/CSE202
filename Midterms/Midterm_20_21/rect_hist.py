# -*- coding: utf-8 -*-
"""
Given a histogram, find the largest area of a rectangle contained in the
histogram.
"""
import math

def rect_from_left(hist, i):
    """compute max area of a rectangle [i,j] for all j, in linear time"""
    n = len(hist)
    max_area = hist[i]
    min_height = hist[i]
    for k in range(i+1,n):
        curr_h = hist[k]
        if curr_h<min_height:
            min_height = curr_h
        curr_area = (k-i+1)*min_height
        if curr_area>max_area:
            max_area = curr_area
    return max_area


def rect_hist_brute(hist):
    """brute force (n^2) solution"""
    n = len(hist)
    max_area = 0
    for i in range(n):
        curr_area = rect_from_left(hist, i)
        if curr_area > max_area:
            max_area = curr_area
    return max_area

def expand_rect(hist, i, j, left, right, h):
    """expand rectangle [l:r] to the left or the right, update height"""
    min_h = h
    l=left
    r=right
    if left == i:
        r += 1
        curr_h = hist[r-1]
        if curr_h < min_h:
            min_h = curr_h
    elif right == j:
        l -= 1
        curr_h = hist[l]
        if curr_h < min_h:
            min_h = curr_h
    elif hist[left-1]>hist[right]:
        l -= 1
        curr_h = hist[l]
        if curr_h < min_h:
            min_h = curr_h
    else:
        r += 1
        curr_h = hist[r-1]
        if curr_h < min_h:
            min_h = curr_h
    return (l,r,min_h)

def best_from_middle(hist, i, j, m):
    """compute max area of a rectangle that includes bar at position m"""
    l = m
    r = m + 1
    h = hist[l]
    max_area = (r-l)*h
    while l != i or r != j:
        l,r,h = expand_rect(hist, i, j, l, r, h)
        curr_area = (r-l)*h
        if curr_area>max_area:
            max_area = curr_area
    return max_area


def rect_hist_dac_aux(hist, i, j):
    """solve over interval [i,j)"""
    if i==j:
        return -math.inf
    m = (i + j) // 2
    return max(rect_hist_dac_aux(hist, i, m),
                   rect_hist_dac_aux(hist, m + 1, j), best_from_middle(hist, i, j, m))


def rect_hist_dac(hist):
    """divide-and-conquer (nlog(n)) solution"""
    return rect_hist_dac_aux(hist, 0, len(hist))
