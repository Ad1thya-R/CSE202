# -*- coding: utf-8 -*-

from uf import Rank_UF

import random


def draw_grid(grid, N):
    for ii in range(N):
        i = ii+1
        for j in range(N):
            if grid[i][j] == 0:
                print('X', end='')
            else:
                print(' ', end='')
        print()

def pos_to_int(N, i, j):
    return N*i+j


def get_vacant_neighbors(G,N,i,j):
    '''
    given a grid G, a position (i,j) and the size N of the grid, returns the list of vacant neighbors of (i,j)
    '''
    neighbors = []
    for pos in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
        if pos[0] in range(N+2) and pos[1] in range(N) and G[pos[0]][pos[1]]:
            neighbors.append(pos)
    return neighbors

def make_vacant(UF, G, N, i, j):
    '''
    given a grid G, a position (i,j) and the size N of the grid, makes the position vacant and joins it to its vacant neighbors
    '''
    G[i][j] = True
    for pos in get_vacant_neighbors(G, N, i, j):
        UF.union(pos_to_int(N, i, j), pos_to_int(N, pos[0], pos[1]))


def ratio_to_percolate(N):
    '''
    1. Generate an (N + 2) × N grid of non-vacant cells (first and last row all vacant).
    2. Initialize a union–find object of size (N + 2)N and perform the union of the cells we unite cells that are on the same row for first and last rows
    3. While the top and bottom are not connected (check using the union–find object):
    (i) randomly select a position (i, j) within the grid (which does not belong to the first and last row),
    (ii) if the corresponding cell is not vacant, make it vacant using make_vacant. 4. Returns the ratio of vacant cells (not counting first and last row).
    '''
    G = [[False for j in range(N)] for i in range(N)]
    G += [[True for j in range(N)]]
    G = [[True for j in range(N)]] + G
    uf = Rank_UF((N+2)*N)
    for i in range(1,N):
        uf.union(pos_to_int(N, 0, 0), pos_to_int(N, 0, i))
        uf.union(pos_to_int(N, N+1, 0), pos_to_int(N, N+1, i))
    top = pos_to_int(N, 0, 0)
    bottom = pos_to_int(N, N + 1, 0)
    count = 0
    while not uf.is_connected(top, bottom):
        i = random.randint(1, N)
        j = random.randint(0, N - 1)

        if not G[i][j]:
            make_vacant(uf, G, N, i, j)
            count += 1
    return count / (N * N)