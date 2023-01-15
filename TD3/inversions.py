def merge_sort_inversions(l):
    n = len(l)

    if n==1:
        return l, 0

    k = n//2
    h1, a1 = merge_sort_inversions(l[:k])
    h2, a2 = merge_sort_inversions(l[k:])
    c = []

    i=0
    j=0
    invs = a1 + a2

    while i<len(a1) and j<len(a2):
        if a1[i] <= a2[j]:
            c.append(a1[i])
            i+=1
        else:
            c.append(a2[j])
            j+=1
            invs += (len(a1)-i)
    c += a1[i:]
    c += a2[j:]
    return c, invs

