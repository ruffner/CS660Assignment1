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
        self.a = None
        self.b = None
        
    def eps(self,t):
        return 1-math.exp((-1*t)/200)

    def recommendArm(self, bandit, history):
        narms = bandit.getNumArms()
        if self.a is None:
            self.a = [0]*narms
        if self.b is None:
            self.b = [0]*narms
        Q = [0]*narms
        
        if len(history):
            turn = history[-1]
            self.a[turn[0]] += 1
            self.b[turn[0]] += turn[1]
                            
            Q = [reward/(pulls+1) for pulls,reward in zip(self.a,self.b)]
            
        ee = random.random()
        
        if ee < self.eps(len(history)):
            return Q.index(max(Q))
        else:
            return round( random.random()*(narms-1) )
