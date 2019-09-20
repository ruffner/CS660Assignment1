import numpy as np
import sys
import copy
import time
import random
from connect4 import connect4
from breakthrough import breakthrough
from randAgent import randomAgent
from minMaxAgent import minMaxAgent
from alphaBetaAgent import alphaBetaAgent
from MCTSAgent import MCTSAgent
import argparse
######################################################
AGENTS_MAP = {'randomAgent' : randomAgent,
               'minMaxAgent' : minMaxAgent,
               'alphaBetaAgent': alphaBetaAgent,
               'MCTSAgent': MCTSAgent  }


GAME_MAP = {'connect4' : connect4,'breakthrough' : breakthrough}
                
#The controller class. For the most part you shouldn't need to do anything here. This just sets up the players using command line parameters. 
class controller: 
    def __init__(self, agent1, agent2, game):
        testGame = connect4()
        player1func=AGENTS_MAP[agent1]
        player2func=AGENTS_MAP[agent2]
        gamefunc=GAME_MAP[game]
        self.currentGame = gamefunc()
        self.player1 = player1func()
        self.player2 = player2func()
        
    #Sets up the games to play. Player 1 will always go first (plays circles) and Player 2 will always go second (plays crosses). 
    def play_game(self):
        currentTurn = 0
        currentPlayers = [self.player1, self.player2]
        if args.verbose:
            self.currentGame.print_board()
        while(not self.currentGame.complete()):
            suggestedMove = ""
            if currentTurn == 0:
                suggestedMove = self.player1.suggestMove(self.currentGame)
                currentTurn = 1
                
            else:
                suggestedMove = self.player2.suggestMove(self.currentGame)
                currentTurn = 0
            self.currentGame.move(suggestedMove)
            if args.verbose:
                print("MAKING MOVE: ", suggestedMove)
            
                self.currentGame.print_board()
            
        if not self.currentGame.draw(): print('%s won' % currentPlayers[self.currentGame.player].name+" "+str(self.currentGame.player))
        else: print('Draw') 

 

#Set of command line arguments that can be used to customize your tests. Can define the type of agent (random, minMax, alphaBeta, or MCTS), the game (connect4 or breakthrough), whether you want additional information printed (verbose mode) and how many games you want the agents to play. 
parser = argparse.ArgumentParser(description='Define the player agents and the game to play.')
parser.add_argument('--agent1', choices=AGENTS_MAP.keys(), default='randomAgent', help='The player 1 AI. Can be randomAgent, minMaxAgent, alphaBetaAgent, or MCTSAgent')
parser.add_argument('--agent2', choices=AGENTS_MAP.keys(), default='randomAgent', help='The player 1 AI. Can be randomAgent, minMaxAgent, alphaBetaAgent, or MCTSAgent')
parser.add_argument('--game', choices=GAME_MAP.keys(), default='connect4', help='The game that the agents will play. Can be either connect4 or breakthrough.')
parser.add_argument('--verbose', help='Print more information.', action='store_true')
parser.add_argument('--num_plays', type=int, default = 1, help='Number of games you want the agents to play.')
args = parser.parse_args()
#Runs a game the specified number of times. 
for numRuns in range(args.num_plays):
    gameControl = controller(args.agent1, args.agent2, args.game)
    gameControl.play_game()