import pygame
import sys
import os
import numpy as np
import neat
import pickle
import time
"""import random
random.seed(42)"""

from .inputHandler import InputHandler

class InputHandlerAI(InputHandler):
    def __init__(self, game):
        """
        A class that handles the AI inputs during gameplay.
        :param state:
        """
        InputHandler.__init__(self, game)

        self.gameState = None
        self.itemState = np.zeros(3)  # normal, big, star

        self.genome = None
        self.net = None
        self.testing = False

        # Load elements from config file
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, '../../../data/ai/config.txt')
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)




    def handleInputs(self):
        # Check pygame inputs and close window if necessary
        self._getUserInputs()

        # Get game states
        self._getGameState()
        self._getItemState()

        # Put states into net and calculate output
        output = self.net.activate(self.gameState.flatten('C').tolist() + self.itemState.flatten('C').tolist())

        self.game.leftKeyHold = False
        self.game.rightKeyHold = False
        self.game.upKeyHold = False

        # go left or go right
        if output[0] > output[2]:
            if output[0] > 5:
                self.game.leftKeyHold = True
        else:
            if output[2] > 5:
                self.game.rightKeyHold = True

        # jump or not jump
        if output[1] > 5:
            self.game.upKeyHold = True



    def _getItemState(self):
        states = self.game.player.getAllStates()
        for state in states:
            self.itemState[state.getID()] = 1

    def _getGameState(self):
        # W-Matrix:
        # 2 tiles behind player, 7 tiles in front of player --> x:10
        # 2 tiles under player, 5 tiles above player --> y: 8

        playerX = self.game.player.rect.x
        playerY = self.game.player.rect.bottom

        # Reset matrix
        """
        IMPORTANT:
        If matrix is modified, the next line *AND* the _withinStateMatrix()-method in SpriteBasic needs to be modified!
        """
        # W-matrix:
        self.gameState = np.zeros((8,10,2))

        # N-matrix:
        #self.gameState = np.zeros((12,6,2))

        # Idea: Delegate to sprites. Then sprites can decide whether or not they write or what they write
        for sprite in self.game.env_sprites.sprites():
            sprite.writeState(self.gameState, playerX, playerY)


    def _getUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.game.game.exitCurrentState()

    def setGenome(self, genome):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, self.config)
        if self.testing:
            for k, ng in genome.nodes.items():
                print(k, ng)
