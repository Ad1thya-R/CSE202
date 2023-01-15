import math

count = 0

# Question 1
"""
This function computes the Euclidean distance between two points
- p is the first point
- q is the second point

returns the Euclidean distance between p and q, i.e., the length of the segment pq
"""
def dist(p, q):
    assert len(p) == len(q)
    # Put your code below this line
    #compute the Euclidean distance between p and q
    distance = 0
    for i in range(len(p)):
        distance += (p[i] - q[i])**2
    return math.sqrt(distance)

# Question 2

def linear_scan(query, P):
    """
    For a given query point, this function returns the index of the point in an
    array of points P that is closest to query using the linear scan algorithm.
    - query is the query point
    - P is a set of points

    returns
    - the index of that nearest neighbour
    - the distance of query to its nearest neighbour in P
    """
    # Put your code below this line
    min_dist, idx = float('inf'), -1
    for i in range(len(P)):
        d = dist(query, P[i])
        if d < min_dist:
            min_dist, idx = d, i
    return idx, min_dist

# Question 3

def compute_median(P, start, end, coord):
    """
    This function computes the median of all the c coordinates
    of a sub-array P of n points that is P[start] .. P[end - 1]
    - P is a set of points
    - start is the starting index
    - end is the last index; the element P[end] is not considered
    - coord is the coordinate considered for the median computation

    returns the median along the coordinate coord
    """
    assert start <= end and 0 <= coord and coord < len(P[0])
    # take the sub array of points
    sub_array = [P[i][coord] for i in range(start, end)]
    # sort the sub array
    sub_array.sort()
    # return the median
    return sub_array[len(sub_array) // 2]



# Question 4
"""
Partitions the array P wrt to its median value of a coordinate
- P is a set of points (an array)
- start is the starting index
- end is the last index; the element P[end] is not considered
- coord is the coordinate used for partitioning

returns the index of the median value
"""
def partition(P, start, end, coord):
    assert start <= end and 0 <= coord and coord < len(P[0])
    #partition with respect to the median in linear time
    #take the median
    '''
    The function rearranges the points in the array P in such a way that every point within the subrange [start : idx] 
    has the coord-th coordinate less than or equal to that of m (with P[idx][coord] = m), while every point within the 
    subrange [idx + 1 : end] has a coord-th coordinate strictly greater than the median.
    '''
    idx = start
    m = compute_median(P, start, end, coord)
    while idx < end:
        if P[idx][coord] > m:
            P[idx], P[end - 1] = P[end - 1], P[idx]
            end -= 1
        elif P[idx][coord] < m:
            P[idx], P[start] = P[start], P[idx]
            start += 1
            idx += 1
        else:
            idx += 1
    return start


# Data structure for Question 5
class Node:
    """
    Constructs a node
    - index is the index of the data point stored at the node
    - coord is the coordinate used for the split
    - median is the split value
    - left is the left sub-tree
    - right is the right sub-tree
    """
    def __init__ (self, index, coord = None, median = None, left = None, right = None):
        self.index = index
        self.coord = coord
        self.median = median
        self.left = left
        self.right = right

    def __repr__ (self):
        return f"Node({self.index},{self.coord if self.coord is not None else 0},{self.median if self.median is not None else 0})"

    def __str__ (self):
        return f"Node(index = {self.index}, coord = {self.coord}, median = {self.median}, left index = {None if self.left is None else self.left.index}, right index = {None if self.right is None else self.right.index})"

# Question 5
"""
Builds the kd-Tree for the sub-cloud P[start:end]
- P is an array of points
- start is the starting index
- end is the last index; the element P[end] is not considered
- coord is the coordinate defining the hyperplane at the root of the tree

returns the kd-Tree for the sub-cloud P[start:end]
"""
def build(P, start, end, coord):
    assert start <= end and 0 <= coord and coord < len(P[0])
    '''
    To maintain the link between the tree nodes and cloud points, we store in each node the 
    index of the corresponding point. For internal nodes of the tree, we will additionally store 1) the (index of the) 
    coordinate used to partition the range during the construction of the node, and 2) the median value used to split 
    the range along that coordinate. This information will be used for the subsequent Nearest Neighbour queries.
    
    1. Sort the points of P along the coordinate c. In the example, for c = 0, we obtain: P = [(2,3),(4,7),(5,4),(7,2),(8,1),(9,6),(9,9)].
    2. Find the median point m. In the example, for c = 0, we take m = (7, 2).
    3. Create a node holding that point.
    4. Split the remaining points into two sub-clouds. In Figure 1a, this is represented by a vertical red line (ortogonal to the x axis) going through point (7, 2).
    5. If no points are left in the cloud, stop.
    6. Otherwise, use the coordinate (c + 1 mod k) to recursively build
    (a) the left sub-tree of the node from step 3 using the points before m in P (points [(2, 3), (4, 7), (5, 4)] in the example), and
    (b) the right sub-tree using the points after m in P (points [(8, 1), (9, 6), (9, 9)] in the example).
    7. return the kd-Tree for the sub-cloud P[start:end]

    '''
    # sort the points along the coordinate c
    m = compute_median(P, start, end, coord)
    # find the median point m
    idx = partition(P, start, end, coord)
    # create a node holding that point
    node = Node(idx, coord, m)
    # split the remaining points into two sub-clouds
    if idx - start > 0:
        node.left = build(P, start, idx, (coord + 1) % len(P[0]))
    if end - idx > 1:
        node.right = build(P, idx + 1, end, (coord + 1) % len(P[0]))
    return node





# Question 6
"""
Helper method for the defeatist search in a kd-Tree
- query is the query point
- P is an array of points
- node is the root of the current sub-node of the kd-tree
- index is the index of the *current* nearest neighbour of query in P
- dmin is the distance from query to that *current* nearest neighbour

returns
- the index of the *updated* nearest neighbour of the query point in P
- the distance from the query point to that *updated* nearest neighbour
"""
def defeatist_search_help(query, P, node, index, dmin):
    '''
    1. Compare q to the point p indexed by the current node: if dist(q,p) < dist(q,qˆ), the point p becomes the new candidate (update qˆ).
    2. If the current node is a leaf, return the current candidate.
    3. Otherwise, let c and m be, respectively, the coordinate and the median stored in the current node:
    (a) if the c-th coordinate of q is less than or equal to m, proceed recursively on the left sub-tree,
    (b) otherwise, proceed recursively on the right sub-tree.
    '''
    # compare q to the point p indexed by the current node
    if dist(query, P[node.index]) < dmin:
        index = node.index
        dmin = dist(query, P[node.index])
    # if the current node is a leaf, return the current candidate
    if node.left is None and node.right is None:
        return index, dmin
    # if the c-th coordinate of q is less than or equal to m, proceed recursively on the left sub-tree
    if query[node.coord] <= node.median:
        if node.left is not None:
            index, dmin = defeatist_search_help(query, P, node.left, index, dmin)
    # if the c-th coordinate of q is greater than m, proceed recursively on the right sub-tree
    else:
        if node.right is not None:
            index, dmin = defeatist_search_help(query, P, node.right, index, dmin)

    return index, dmin

"""
Defeatist search in a kd-Tree
- query is the query point
- P is an array of points

returns
- the index of the *updated* nearest neighbour of the query point in P
- the distance from the query point to that *updated* nearest neighbour
"""
def defeatist_search(query, P):
    # Put your code below this line
    # Prepare the kd-Tree, then call the helper method on its root
    node = build(P, 0, len(P), 0)
    index, dmin = defeatist_search_help(query, P, node, 0, math.inf)
    return index, dmin

# Question 7
"""
Helper method for the backtracking search in a kd-tree
- query is the query point
- P is the list of points in the point cloud
- node is the root of the kd-tree
- index is the index of the *current* nearest neighbour of query in P
- dmin is the distance from query to that *current* nearest neighbour

returns
- the index of the *updated* nearest neighbour of the query point in P
- the distance from the query point to that *updated* nearest neighbour
"""
def backtracking_search_help(query, P, node, index, dmin):
    global count
    count += 1
    #backtracking_search_help(query, P, node, index, dmin) modifying the previous algorithm, so as to check the other half-space, when necessary.
    # compare q to the point p indexed by the current node
    if dist(query, P[node.index]) < dmin:
        index = node.index
        dmin = dist(query, P[node.index])
    # if the current node is a leaf, return the current candidate
    if node.left is None and node.right is None:
        return index, dmin
    # if the c-th coordinate of q is less than or equal to m, proceed recursively on the left sub-tree
    if query[node.coord] <= node.median:
        if node.left is not None:
            index, dmin = backtracking_search_help(query, P, node.left, index, dmin)
    # if the c-th coordinate of q is greater than m, proceed recursively on the right sub-tree
    else:
        if node.right is not None:
            index, dmin = backtracking_search_help(query, P, node.right, index, dmin)
    #If dist(a,p) is smaller than the distance from a to the current splitting hyperplane (see Figure 2a),
    # then indeed it is sufficient to search for the nearest neighbour in the same half-space as a.
    # However, if dist(a,p) is greater than the distance from a to the current splitting hyperplane (see Figure 2b),
    # the actual nearest neighbour might turn out to be in the other half-space, which defeatist_search does not visit.
    if abs(query[node.coord] - node.median) < dmin:
        if query[node.coord] <= node.median:
            if node.right is not None:
                index, dmin = backtracking_search_help(query, P, node.right, index, dmin)
        else:
            if node.left is not None:
                index, dmin = backtracking_search_help(query, P, node.left, index, dmin)
    return index, dmin


"""
Backtracking search in a kd-tree
- query is the query point
- P is the list of points in the point cloud

returns
- the index of the *updated* nearest neighbour of the query point in P
- the distance from the query point to that *updated* nearest neighbour
"""
def backtracking_search(query, P):
    global count
    count = 0
    # Put your code below this line
    # Prepare the kd-Tree, then call the helper method on its root
    node = build(P, 0, len(P), 0)
    index, dmin = backtracking_search_help(query, P, node, 0, math.inf)
    return index, dmin

