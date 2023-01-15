# -*- coding: utf-8 -*-

# the input is represented by a list of (left,height,right)
# the output (skyline) is represented by an ordered list of (left,height) and always ends with 
# a (left,0) entry

def rects_height_at(rects, x):
    """
    given a list of rectangles and a position, return h(x)=max{y:(l,r,y) in rects and l<=x<r}
    note that the inequality l<=x<r is assymetric: large on the left and strict on the right
    """
    max_h=0
    for (l, h, r) in rects:
        if x>=l and x<r and h>max_h:
            max_h = h
    return max_h



def simplify_skyline(skyline):
    """simplify a skyline by removing redundant entries"""
    '''
    simplified = [skyline[0]]
    curr_h = skyline[0][1]
    for i in range(1, len(skyline)):
        x1, h1 = skyline[i]
        if h1==curr_h:
            continue
        else:
            simplified.append(skyline[i])
            curr_h = h1
    return simplified
    '''
    res = [skyline[0]]
    for i in range(len(skyline)-1):
        x1, h1 = skyline[i]
        x2, h2 = skyline[i+1]
        if h1 == h2:
            continue
        else:
            res.append((x2,h2))
    return res


def skyline_naive(rects):
    """computes the skyline in O(n^2)"""
    skyline_set = sorted(set([l for (l,h,r) in rects] + [r for (l,h,r) in rects]))
    max_skyline = [(x, rects_height_at(rects,x)) for x in skyline_set]
    return simplify_skyline(max_skyline)

def merge_skylines(sky1, sky2):
    """merge two skylines"""
    curr1 = 0
    curr2 = 0
    currh1 = 0
    currh2 = 0
    n1 = len(sky1)
    n2 = len(sky2)
    res = []
    while curr1<n1 and curr2<n2:
        el1 = sky1[curr1]
        el2 = sky2[curr2]
        if el1[0] < el2[0]:
            currh1 = el1[1]
            maxh = max(currh1, currh2)
            res.append((el1[0], maxh))
            curr1+=1
        elif el1[0] > el2[0]:
            currh2 = el2[1]
            maxh = max(currh1, currh2)
            res.append((el2[0], maxh))
            curr2+=1
        elif el1[0] == el2[0]:
            currh1 = el1[1]
            currh2 = el2[1]
            maxh = max(currh1, currh2)
            res.append((el1[0], maxh))
            curr1 += 1
            curr2 += 1
    diff1 = n1 - curr1
    diff2 = n2 - curr2
    if diff2>0:
        res += [sky2[x] for x in range(curr2, n2)]
    if diff1>0:
        res += [sky1[x] for x in range(curr1, n1)]

    return simplify_skyline(res)




    pass

def skyline_dac(rects):
    if len(rects) == 1:
        (left, h, right) = rects[0]
        return [(left, h), (right, 0)]
    n = len(rects) // 2
    return merge_skylines(skyline_dac(rects[:n]), skyline_dac(rects[n:]))



