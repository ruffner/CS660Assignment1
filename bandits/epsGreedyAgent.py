import math
import numpy as np
import sys
import copy
import time
import random
import argparse
######################################################

#Okay what do we need to do. First, create agents. This should use command line args. 
#Also we need to create the game
class epsGreedyAgent: 
    def __init__(self):
        #self.currentState.print_board()
        self.name = "Eric the Epsilon Greedy Agent"

    def eps(self,t):
        return 1-math.exp((-1*t)/200)

    def recommendArm(self, bandit, history):
        narms = bandit.getNumArms()
        Nt = [0]*narms
        Q = [0]*narms

        if len(history):
            for turn in history:
                Nt[turn[0]] += (1 if turn[1] else 0)
            Q = [n/len(history) for n in Nt]

        ee = random.random()

        if ee < self.eps(len(history)):
            return Q.index(max(Q))
        else:
            return round( random.random()*(narms-1) )
