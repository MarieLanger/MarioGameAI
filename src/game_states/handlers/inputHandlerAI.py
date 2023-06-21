import pygame
import sys
import os
import numpy as np
import neat
import pickle
import time

from .inputHandler import InputHandler

class InputHandlerAI(InputHandler):
    def __init__(self, game):
        """
        A class that handles the AI inputs during gameplay.
        :param state:
        """
        InputHandler.__init__(self, game)

        self.gameState = np.zeros((8,10,2))
        self.itemState = np.zeros(3)  # normal, big, star

        self.genome = None
        self.net = None

        # Load elements from config file
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, '../../../data/ai/config.txt')
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)


        # Initialize population
        #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
        self.p = neat.Population(self.config)

        # Initialize reporters
        self.p.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.p.add_reporter(self.stats)
        self.p.add_reporter(neat.Checkpointer(1))



        """
        Within eval_genomes, the fitness is modified.
        Hence, run() can stop early if the max fitness was reached.
        Idea:
        Within eval_genomes, iterate through genomes
        - For each genome, play 1 level
        - After level got finished, assess fitness, mutate and recombine
        
        For genome in genomes
        - Restart level
        - Create network
        - handleInputs() is basically moveAIPaddles()
        - Within handleInputs(), game state gets queried
        
        
        
        """


    def handleInputs(self):
        # Check pygame inputs and close window if necessary
        self._getUserInputs()

        # Get game states
        self._getGameState()
        self._getItemState()

        # Put states into net and calculate output
        output = self.net.activate(self.gameState.flatten('C').tolist() + self.itemState.flatten('C').tolist())
        decision = output.index(max(output))

        self.game.leftKeyHold = False
        self.game.rightKeyHold = False
        self.game.upKeyHold = False

        if decision == 0:
            self.game.leftKeyHold = True
        elif decision == 1:
            self.game.upKeyHold = True
        elif decision == 2:
            self.game.rightKeyHold = True


    def _getItemState(self):
        states = self.game.player.getAllStates()
        for state in states:
            self.itemState[state.getID()] = 1

    def _getGameState(self):
        # MATRIX:
        # 2 tiles behind player, 7 tiles in front of player --> x:10
        # 2 tiles under player, 5 tiles above player --> y: 8

        playerX = self.game.player.rect.x
        playerY = self.game.player.rect.bottom

        # Reset matrix
        self.gameState = np.zeros((8,10,2))

        # Idea: Delegate to sprites. Then sprites can decide whether or not they write or what they write
        for sprite in self.game.env_sprites.sprites():
            sprite.writeState(self.gameState, playerX, playerY)

        #print(self.gameState[:,:,1])

    def _getUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.game.exitCurrentState()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.game.game.exitCurrentState()

    def setGenome(self, genome):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, self.config)
