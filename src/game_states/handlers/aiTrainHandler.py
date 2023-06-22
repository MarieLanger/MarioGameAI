import pygame
import sys
import os
import neat
import pickle
import time
from pathlib import Path

from .levelEndHandler import LevelEndHandler
from ..stateTrainingCompleted import StateTrainingCompleted

class AITrainHandler(LevelEndHandler):
    def __init__(self, game, inputHandler, fitnessfunction):
        """
        A class that handles the inputs from humans during gameplay.
        :param state:
        """
        LevelEndHandler.__init__(self, game)

        self.inputHandler = inputHandler
        self.fitnessfunction = fitnessfunction


        # load elements from config file
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, '../../../data/ai/config.txt')
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  config_path)

        # Initialize population
        #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
        self.p = neat.Population(self.config)
        self.genomes = list(self.p.population.items())
        self.genomeCount = len(self.genomes)
        self.currentGenomeID = 0
        self.currentGeneration = 0
        self.maxGenerations = 50

        print(self.genomes)
        print(self.genomeCount)
        print(self.genomes[self.currentGenomeID][1])

        self.inputHandler.setGenome(self.genomes[self.currentGenomeID][1])




        # Initialize reporters
        self.p.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.p.add_reporter(self.stats)
        self.p.add_reporter(neat.Checkpointer(1))

        # todo: maybe bad
        self.p.reporters.start_generation(self.p.generation)


        # todo: put this part into handleLevelEnd
        # Evaluate genomes 50 times max


    def handleLevelEnd(self, outcome, progress, time, coins, enemies):

        pass



