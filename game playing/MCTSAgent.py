import math
import numpy as np
import sys
import copy
import time
import random
import argparse
from collections import defaultdict
######################################################

class MCTSTree:
    ''' MCTS Tree class '''
    def __init__(self):
        self.winCount = defaultdict(int)  # cumulative reward
        self.visitCount = defaultdict(int)  # cumulative visits
        self.children = dict()  # keep track of children
        self.exploration_weight = math.sqrt(2)
        self.nodeCount = 0

    def getBestMove(self, node):
        if node.is_terminal():
            print("error.. no best move from an end-game state")
            return

        if node not in self.children:
            print("finding random child")
            return node.find_random_child()

        #print("i have ", self.nodeCount, " children")
        
        def nodeScore(n):
            if self.visitCount[n] == 0:
                return float("-inf")
            return self.winCount[n] / self.visitCount[n]

        return max(self.children[node], key=nodeScore)
        
    # 'rollout' a node aka randomly take moves until
    # terminal state is reached
    def do_a_rollout(self, node):
        #print("in rollout with node",hash(node))

        path = self._selection(node)
        leafNode = path[-1]

        #print("   in doarollout, path is ", path)
        #print("   in doarollout, leafNode is ",leafNode)
        
        self._expansion(leafNode)
        reward = self._simulation(leafNode)
        self._backprop(path, reward)

    # select an unexplored descendant of a node
    def _selection(self, node):
        path = []

        #print("in selection, NODE is ", node)
        
        while True:
            path.append(node)

            # if this node is not in the tree or
            # the entry in the tree is invalid then this
            # input node is indeed an unexplored node
            if node not in self.children or not self.children[node]:
                #print("  returning path as is..")
                return path

            #print("-- in selection, self.children[node] is ", self.children[node])
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)

            
    # update child node tracking information
    def _expansion(self, node):
        # if already expanded do nothing
        if node in self.children:
            #print("      in expansion, node is already in tree")
            return
        self.children[node] = node.find_children()
        self.nodeCount += len(self.children[node])

    # get reward associated with a random simulation to
    # a terminal state
    def _simulation(self, node):
        myTurn = True
        while True:
            if node.is_terminal():
                reward = node.reward(myTurn)
                return reward if myTurn else (1 - reward)
            node = node.find_random_child()
            myTurn = not myTurn

    # populate intermediate node values with information
    # learned during descent
    def _backprop(self, path, reward):
        for node in reversed(path):
            self.visitCount[node] += 1
            self.winCount[node] += reward
            reward = 1 - reward

    def _uct_select(self, node):
        
        # All children of node should already be expanded
        assert all(n in self.children for n in self.children[node])

        def uct(n):
            c = self.exploration_weight
            uc = c * math.sqrt( math.log(self.visitCount[n]) / (self.visitCount[n] + 1) ) # avoid divide by zero if unexplored
            uc = uc + self.winCount[n] / (self.visitCount[n] + 1)
            return uc

        return max(self.children[node], key=uct)


''' MCTS Node class '''
class MCTSNode:
    def __init__(self, gameState, mostRecentMove):
        self.gs = gameState
        self.move = mostRecentMove

    # implement hash, eq and neq so this object
    # can be used as a dictionary key
    def __eq__(self, other):
        return self.gs == other.gs

    def __ne__(self, other):
        return not(self.gs == other.gs)
    
    # string hashes are the same on a per process basis
    def __hash__(self):

        if type(self.gs).__name__ == "breakthrough":
            board = ""
            for row in self.gs.board:
                for letter in row:
                    board += (letter)
            return hash(tuple(board))
        else:
            board = ""
            for row in self.gs.board:
                for letter in row:
                    board += str(letter)
            return hash(tuple(board))

    def reward(self, myTurn = False):
        if self.gs.complete():
            if type(self.gs).__name__ == "connect4":
                return self.gs.result(not(myTurn))
            else:
                if self.gs.terminal_state() == self.gs.get_turn():
                    return 1
                else:
                    return 0
        else:
            print("reward error")
            return 0
            
    def is_terminal(self):
        return self.gs.complete()

    def find_random_child(self):
        if self.gs.complete():
            return None
        else:
            copy = self.gs.clone()
            numMoves = len(copy.getMoves())
            randomMove = self.gs.getMoves()[round(random.random()*(numMoves-1))]
            copy.move(randomMove)
            return MCTSNode(copy, randomMove)

    def find_children(self):
        if self.is_terminal():
            return set()
        else:
            children = set()
            for move in self.gs.getMoves():
                copy = self.gs.clone()
                copy.move(move)
                node = MCTSNode(copy, move)
                children.add(node)
            return children
    
        
## Agent class
class MCTSAgent():
    ''' The MCTS Agent class that interacts with the game '''
    def __init__(self):
        #self.currentState.print_board()
        self.name = "Mallory the MCTSAgent"
        
    def suggestMove(self, gameState):

        # create and initialize tree with root node
        # this is an inefficient way to do things since I
        # throw away the tree on every move reccommendation
        
        #TODO: implement tracking to compare the current board state
        # to the previous board state in order to choose the next leaf
        # in the simulated tree that corresponds to the move that the opponnent
        # took. This way you are at a known state in the already existing
        # tree and dont have to worry about making moves that are now invalid
        tree = MCTSTree()
        node = MCTSNode(gameState, None)

        # do rollouts on the tree until each direct leaf has been done 4 times
        # or tree has 10000 nodes, whichever comes first
        numRollouts = 10
        if type(gameState).__name__ == "connect4":
            numRollouts = 50
        else:
            numRollouts = len(gameState.getMoves())*4
        for i in range(numRollouts):
            tree.do_a_rollout(node)
            if tree.nodeCount > 10000:
                break

        # reccommend move
        return tree.getBestMove(node).move
