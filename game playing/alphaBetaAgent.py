
import numpy as np
import sys
import copy
import time
import random
import argparse
######################################################

class alphaBetaAgent: 
    def __init__(self):
        self.name = "Allison the AlphaBetaAgent"
    
    def suggestMove(self, gameState):
        v,a = self.maxValue(gameState, -1, float("-inf"), float("inf"))
        return a

    # max layer of minimax tree
    def maxValue(self, game, level, alpha, beta):
        # recursion depth limit
        if level > 2 and not game.complete():
            return game.heuristic_value(),0

        # utility of a terminal state        
        if game.complete():
            if type(game).__name__=='connect4':
                return game.result(0), 0
            if type(game).__name__=='breakthrough':
                return game.heuristic_value(), 0

        a = 0
        v = -100000        
        for m in game.getMoves():
            copy = game.clone()
            copy.move(m)
            u,_ = self.minValue(copy, level+1, alpha, beta)
            if u > v:
                v = u
                a = m
                if v >= beta:
                    return v,a
            alpha = max(alpha, v)
        
        return v,a

    def minValue(self, game, level, alpha, beta):
        if level > 2 and not game.complete():
            return game.heuristic_value(), 0

        if game.complete():
            if type(game).__name__=='connect4':
                return game.result(0),0
            if type(game).__name__=='breakthrough':
                return game.heuristic_value(), 0

        a = 0
        v = 100000
        for m in game.getMoves():
            copy = game.clone()
            copy.move(m)
            u,_ = self.maxValue(copy, level+1, alpha, beta)
            if u < v:
                v = u
                a = m
                if v <= alpha:
                    return v,a
                
            beta = min(beta, v)
            
        return v,a
