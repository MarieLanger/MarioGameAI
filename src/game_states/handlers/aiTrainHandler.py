import pygame
import sys
import os
import neat
import pickle
import time
from pathlib import Path
import shutil

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
        self.currentGeneration = 0

        if self.currentGeneration == 0:
            self.p = neat.Population(self.config)
        else:
            self.p = neat.Checkpointer.restore_checkpoint('../data/ai/genomes/neat-checkpoint-' + str(self.currentGeneration))

        # When starting from checkpoint 5, then generation 5 is finished and we need to continue with generation 6
        #self.currentGeneration += 1

        self.genomes = list(self.p.population.items())
        self.genomeCount = len(self.genomes)
        self.currentGenomeID = 0
        self.maxGenerations = 50

        # print(self.genomes)
        # print(self.genomeCount)
        # print(self.genomes[self.currentGenomeID][1])

        self.inputHandler.setGenome(self.genomes[self.currentGenomeID][1])

        self.fitnesses = []




        # Initialize reporters
        self.p.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.p.add_reporter(self.stats)
        self.p.add_reporter(neat.Checkpointer(1))

        # Start the generation
        self.p.reporters.start_generation(self.p.generation)








    def handleLevelEnd(self, outcome, progress, time, coins, enemies):
        pass


