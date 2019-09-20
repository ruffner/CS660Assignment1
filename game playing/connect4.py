
import numpy as np
import sys
import copy
import time
import random

class connect4:
    def __init__(self):
        self.ROW = 6 
        self.COLUMN = 7
        self.LINE = 4
        self.player = 0
        self.bitboard = [0,0] # bitboard for each player
        self.dirs = [1, (self.ROW+1), (self.ROW+1)-1, (self.ROW+1)+1] # this is used for bitwise operations
        self.heights = [(self.ROW+1)*i for i in range(self.COLUMN)] # top empty row for each column 
        self.lowest_row = [0]*self.COLUMN # number of stones in each row
        self.board = np.zeros((self.ROW, self.COLUMN), dtype=int) # matrix representation of the board (just for printing)
        self.top_row = [(x*(self.ROW+1))-1 for x in range(1, self.COLUMN+1)] # top row of the board (this will never change)

        
    #Returns a copy of the current game object. This could be useful for storing the current state of the game. 
    def clone(self):
        Clone = connect4()
        Clone.bitboard = copy.deepcopy(self.bitboard)
        Clone.heights = copy.deepcopy(self.heights)
        Clone.lowest_row = copy.deepcopy(self.lowest_row)
        Clone.board = copy.deepcopy(self.board)
        Clone.top_row = copy.deepcopy(self.top_row)
        Clone.player = self.player
        return Clone
        
    #Executes a move. While not especially important, moves in connect 4 are represented by the column that you wish to place a piece. 
    def move(self, col):
        m2 = 1 << self.heights[col] # position entry on bitboard
        self.heights[col] += 1 # update top empty row for column
        self.player ^= 1
        self.bitboard[self.player] ^= m2 # XOR operation to insert stone in player's bitboard
        self.board[self.lowest_row[col]][col] = self.player + 1 # update entry in matrix (only for printing)
        self.lowest_row[col] += 1 # update number of stones in column
    
    def result(self, player):
        if self.winner(player): return 0 # player wins
        elif self.winner(player^1): return 1 # if opponent wins
        elif self.draw(): return 0.5 
    
    #Returns a heuristic value for how good or bad a state is. In this case, the heuristic is the length of the longest "open" sequence of player pieces on the vertical or horizontal axis. This is not a very good heuristic. 
    def heuristic_value(self):
        longestValue = 0
        symbol = ""
        value = self.player+1
        print(value)
        currentLongest = 0

        #Search Right
        for i in range(len(self.board)):
            currentStreak = 0
            previousChar=-1
            for j in range(len(self.board[i])):
                if self.board[i][j] != previousChar:
                    previousChar = self.board[i][j]
                    if previousChar == 0 and currentLongest < currentStreak:
                        currentLongest = currentStreak
                    currentStreak = 0
                if self.board[i][j] == previousChar and previousChar == value:
                    currentStreak += 1

        #Search Left
        for i in range(len(self.board)):
            currentStreak = 0
            previousChar=-1
            for j in reversed(range(len(self.board[i]))):
                if self.board[i][j] != previousChar:
                    previousChar = self.board[i][j]
                    if previousChar == 0 and currentLongest < currentStreak:
                        currentLongest = currentStreak
                    currentStreak = 0
                if self.board[i][j] == previousChar and previousChar == value:
                    currentStreak += 1


        #Search Up
        for i in range(len(self.board[0])):
            currentStreak = 0
            previousChar= -1
            for j in range(len(self.board)):
                if self.board[j][i] != previousChar:
                    previousChar = self.board[j][i]
                    if previousChar == 0 and currentLongest < currentStreak:
                        currentLongest = currentStreak
                    currentStreak = 0
                if self.board[j][i] == previousChar and previousChar == value:
                    currentStreak += 1
        return currentLongest

    # checks if column is full
    def isValidMove(self, col): 
        return self.heights[col] != self.top_row[col]
    
    # evaluate board, find out if there's a winner
    def winner(self, color):
        for d in self.dirs:
            bb = self.bitboard[color]
            for i in range(1, self.LINE): 
                bb &= self.bitboard[color] >> (i*d)
            if (bb != 0): return True
        return False
    

    #Prints the game board in a relatively easy to interpret format. 
    def print_board(self):
        board = np.flip(self.board, axis=0)
        for row in board:
            sys.stdout.write('\t')
            for col in row:
                output = '-OX'[col]
                sys.stdout.write(output)
            sys.stdout.write('\n')
        sys.stdout.write('\t')
        for i in range(1, self.COLUMN+1):
            sys.stdout.write(str(i))
        sys.stdout.write('\n\n')

    
    def draw(self): # is it draw?
        return not self.getMoves() and not self.winner(self.player) and not self.winner(self.player^1)
    
    def complete(self): # is it game over? 
        return self.winner(self.player) or self.winner(self.player^1) or not self.getMoves()
    
    # returns list of available moves
    def getMoves(self):
        if self.winner(self.player) or self.winner(self.player^1): return [] # if terminal state, return empty list
        
        listMoves = []
        for i in range(self.COLUMN):
            if self.lowest_row[i] < self.ROW: 
                listMoves.append(i)
        return listMoves

    #Functions that enable you to directly compare connect4 objects. This will allow you to use both the '==' and '!=' operators. 
    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.player == other.player and self.bitboard == other.bitboard and np.array_equal(self.board, other.board)

    def __ne__(self, other):
        """Override the default Unequal behavior"""
        return self.player != other.player or self.bitboard != other.bitboard or not np.array_equal(self.board, other.board)