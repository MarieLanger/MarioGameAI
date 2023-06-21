from .state import State
from .stateGame import StateGame

import os
import neat
import pickle
import pygame
import time


class StateTraining(State):
    def __init__(self, program):
        State.__init__(self, program)
        self.levelSimulator = StateGame(self.game, "AI", "Train")

        # load elements from config file
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

        # Evaluate genomes 50 times max
        winner = self.p.run(self.evaluateGenomes, 50)
        with open("best.pickle", "wb") as f:
            pickle.dump(winner, f)

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


    def evaluateGenomes(self, genomes, config):
        # Enumerate all genomes and train each one separately
        for i, (genome_id1, genome1) in enumerate(genomes):
            force_quit = self.trainAI(genome1, config)
            if force_quit:
                quit()


    def trainAI(self,genome1, config):
        """
        TrainAI() is that method that gets executed for every genome.
        It ONLY gets exited after the training of that genome got completed!
        So basically:
        - Reload level
        - Play game
        - Exit if game over/ level completed
        """
        run = True
        start_time = time.time()

        # Create the networks
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        self.genome1 = genome1

        max_hits = 50

        while run:
            # Check force quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            # run the game loop and generate infos about the game
            game_info = self.levelSimulator.update()

            # Moving the paddles and calculating the fitness?
            # todo
            #self.move_ai_paddles(net1)



            # calculate fitness with the hits and the time taken
            duration = time.time() - start_time
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.genome1.fitness += game_info.left_hits + duration
                break

        return False


    def update(self):

        self.levelSimulator.update()




    def display(self):
        self.levelSimulator.display()