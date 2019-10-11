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
class UCBAgent:
    def __init__(self):
        #self.currentState.print_board()
        self.name = "Uma the UCB Agent"
        self.a = None
        self.b = None
        
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

            Q = [(reward/(pulls+1))+math.sqrt((2*math.log(len(history)))/(pulls+1)) for pulls,reward in zip(self.a,self.b)]

        return Q.index(max(Q))
