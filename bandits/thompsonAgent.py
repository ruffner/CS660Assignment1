
import numpy as np
import sys
import copy
import time
import random
import argparse
######################################################

class thompsonAgent: 
    def __init__(self):
        self.name = "Terry the Thompson Sampling Agent"
        self.alpha = None
        self.beta  = None
        
    def recommendArm(self, bandit, history):
        narms = bandit.getNumArms()
        if self.alpha is None:
            self.alpha = [1]*narms
        if self.beta is None:
            self.beta  = [1]*narms

        # update posterior probs
        if len(history):
            turn = history[-1]
            if turn[1]:
                self.alpha[turn[0]] += 1
            else:
                self.beta[turn[0]]  += 1

        # calculate means
        Q = [a/(a + b) for a,b in zip(self.alpha,self.beta)]

        return Q.index(max(Q))

