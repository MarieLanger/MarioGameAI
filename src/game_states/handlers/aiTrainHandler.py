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

        # If evaluating of the whole population has not finished yet
        if self.currentGenomeID < self.genomeCount:

            # set fitness for genome with outcome, progress, time, coins, enemies
            if self.fitnessfunction == 1:
                if outcome == -1:
                    self.genomes[self.currentGenomeID][1].fitness = progress
                if outcome == +1:
                    self.genomes[self.currentGenomeID][1].fitness = 10000 + 500 - time

            elif self.fitnessfunction == 2:
                if outcome == -1:
                    self.genomes[self.currentGenomeID][1].fitness = progress + coins*300
                if outcome == +1:
                    self.genomes[self.currentGenomeID][1].fitness = 100000 + coins*300 + (5000 - (time*2))

            elif self.fitnessfunction == 3:
                if outcome == -1:
                    self.genomes[self.currentGenomeID][1].fitness = progress + coins*300 + enemies*300
                if outcome == +1:
                    self.genomes[self.currentGenomeID][1].fitness = 100000 + coins*300 + enemies*300 + (5000 - (time*2))

            print("Genome", self.currentGenomeID, "has fitness:", self.genomes[self.currentGenomeID][1].fitness)


            # Go to next genome and reset level
            self.currentGenomeID += 1

            if not self.currentGenomeID == self.genomeCount:
                self.inputHandler.setGenome(self.genomes[self.currentGenomeID][1])
                self.game.initializeLevel()

        else:
            # Else, go either to a new generation (if) or terminate training (else)
            if self.currentGeneration < 50:

                # todo: mutate and stuff

                # Gather and report statistics.
                best = None
                #print("Count:", len(self.p.population.values()))
                for g in self.p.population.values():
                    #print(g.fitness, g.key)
                    if g.fitness is None:
                        raise RuntimeError("Fitness not assigned to genome {}".format(g.key))

                    if best is None or g.fitness > best.fitness:
                        best = g
                self.p.reporters.post_evaluate(self.p.config, self.p.population, self.p.species, best)

                # Track the best genome ever seen.
                if self.p.best_genome is None or best.fitness > self.p.best_genome.fitness:
                    self.p.best_genome = best

                if not self.p.config.no_fitness_termination:
                    # End if the fitness threshold is reached.
                    fv = self.p.fitness_criterion(g.fitness for g in self.p.population.values())
                    if fv >= self.p.config.fitness_threshold:
                        self.p.reporters.found_solution(self.p.config, self.p.generation, best)
                        #break

                # Create the next generation from the current generation.
                self.p.population = self.p.reproduction.reproduce(self.p.config, self.p.species,
                                                              self.p.config.pop_size, self.p.generation)

                # Check for complete extinction.
                if not self.p.species.species:
                    self.p.reporters.complete_extinction()

                    # If requested by the user, create a completely new population,
                    # otherwise raise an exception.
                    if self.p.config.reset_on_extinction:
                        self.p.population = self.p.reproduction.create_new(self.p.config.genome_type,
                                                                       self.p.config.genome_config,
                                                                       self.p.config.pop_size)
                    else:
                        print("CompleteExtinctionException!!")

                # Divide the new population into species.
                self.p.species.speciate(self.p.config, self.p.population, self.p.generation)

                self.p.reporters.end_generation(self.p.config, self.p.population, self.p.species)

                self.p.generation += 1


                if self.p.config.no_fitness_termination:
                    self.p.reporters.found_solution(self.p.config, self.p.generation, self.p.best_genome)

                winner = self.p.best_genome



                #"../data/ai/" +
                # Save best one in folder
                name = "../data/ai/genomes/" + "Gen" + str(self.currentGeneration).zfill(2) + "_best.pickle"

                with open(name, "wb") as f:
                    pickle.dump(winner, f)

                # Go to new generation
                self.genomes = list(self.p.population.items())
                self.currentGenomeID = 0
                self.currentGeneration += 1
                self.inputHandler.setGenome(self.genomes[self.currentGenomeID][1])
                self.p.reporters.start_generation(self.p.generation)  # todo: maybe bad

                # Move the checkpoint file
                name = "neat-checkpoint-" + str(self.currentGeneration)
                Path(name).rename("../data/ai/genomes/" + name)


            else:
                # Finish the algorithm and go back to title screen
                return StateTrainingCompleted(self.game.game, self.game)




    '''

    def evaluateGenomes(self, genomes, config):
        # Enumerate all genomes

        """for count, value in enumerate(values):
            print(count, value)

        with values = ["A","B","C"] this gives:
        1 "A"
        2 "B"
        3 "C"

        """

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
            game_info = self.game.loop()

            # Moving the paddles and calculating the fitness?
            self.move_ai_paddles(net1)

            # Draw game
            pygame.display.update()

            # calculate fitness with the hits and the time taken
            duration = time.time() - start_time
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.genome1.fitness += game_info.left_hits + duration
                break

        return False'''
