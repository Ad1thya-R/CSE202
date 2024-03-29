# -*- coding: utf-8 -*-
from uf import Rank_UF
import random

class Hex:
    def __init__(self, N):
        # size of the board (counting extra rows / columns)
        self.size = N+2
        # initialisation of the board (all hexagons are free)
        self.board = [[0 for j in range(self.size)] for i in range(self.size)]

        # initialisation of the Union-Find object
        nelem = self.size**2
        self.uf = Rank_UF(nelem)
        
        # first player to play is player 1
        self.player = 0


        l = self.size-1
        # union of sides of each player
        # player 1 is affected to the extra rows, player 2 extra columns
        for i in range(1,self.size-1):
            self.board[0][i] = 1
            self.board[l][i] = 1
            self.board[i][0] = 2
            self.board[i][l] = 2

            
            if i > 0:
                self.uf.union(self.hex_to_int(1,0), self.hex_to_int(i,0))
                self.uf.union(self.hex_to_int(1,l), self.hex_to_int(i,l))        

                self.uf.union(self.hex_to_int(0,1), self.hex_to_int(0,i))
                self.uf.union(self.hex_to_int(l,1), self.hex_to_int(l,i))
        
        # get the indices in UF of the bottom and top sides of each player               
        self.bot1 = self.hex_to_int(0,1)
        self.top1 = self.hex_to_int(l,1)
        self.bot2 = self.hex_to_int(1,0)
        self.top2 = self.hex_to_int(1,l)
        

    def hex_to_int(self, i, j):
        return i*(self.size) +j
        
    def print_board(self):
        for i in range(1, self.size-1):
            print(' '*(i-1),end='')
            for j in range(1, self.size-1):
                if self.board[i][j] == 0:
                    print('_', end='')
                if self.board[i][j] == 1:
                    print('X', end='')
                if self.board[i][j] == 2:
                    print('O', end='')
            print()
            
    
    def neighbours(self, i, j):
        '''
        return the list of neighbours of the hexagon [i,j] and belong to the current player
        '''
        playa = 2
        if self.player == 0:
            playa = 1

        L = []
        for k in [-1, 1]:
            if self.board[i + k][j] == playa:
                L.append([i + k, j])
            if self.board[i][j + k] == playa:
                L.append([i, j + k])
            if self.board[i + k][j - k] == playa:
                L.append([i + k, j - k])
        return L

    
    def is_game_over(self):
        '''
        checks if the game is over: since the top side is connected to the bottom side by a path of red tokens.
        '''
        if self.player == 0 and self.uf.is_connected(self.bot1, self.top1):
            return True

        if self.player == 1 and self.uf.is_connected(self.bot2, self.top2):
            return True
        return False

    def random_turn(self):
        '''
        select randomly a free hexagon and assign it to the current player.
        Then make the union of the selected hexagon to the neighboring ones belonging to the current player.
        '''
        playa = 2
        if self.player == 0:
            playa = 1

        i = random.randint(1, self.size-2)
        j = random.randint(1, self.size-2)
        while self.board[i][j] != 0:
            i = random.randint(1, self.size-2)
            j = random.randint(1, self.size-2)
        self.board[i][j] = playa
        for k in self.neighbours(i, j):
            self.uf.union(self.hex_to_int(i,j), self.hex_to_int(k[0], k[1]))
        self.player = 1 - self.player
        
    def random_play(self):
        '''
            TO IMPLEMENT
        '''

        def random_play(self):
            '''
                TO IMPLEMENT
            '''

            num_turn = 0
            game_over = False
            while not game_over:
                self.random_turn()
                num_turn += 1

                game_over = self.is_game_over()

            return num_turn / (self.size - 2) ** 2
