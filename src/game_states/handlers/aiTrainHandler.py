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
        """
        Evaluate genomes and handle the population and the training as a whole.

        If not all genomes from a population have been evaluated, evaluate the remaining genomes.
        If all genomes have been evaluated, recombine, mutate and do natural selection.

        NOTE:
        This method is based on the NEAT library's population.run()-method and the code called after a population
        has finished evaluating is taken from it.
        population.run()'s first parameter is a method. In this method, a game loop is created and the game is run.
        However, in our case, the NEAT algorithm is run from inside the program, and not vice versa.
        (=There is already a game loop). To run NEAT from within an existing game loop, the method got altered.
        The source code can be found here:
        https://neat-python.readthedocs.io/en/latest/_modules/population.html

        :param outcome:
        :param progress:
        :param time:
        :param coins:
        :param enemies:
        :return:
        """

        # If evaluating of the whole population has not finished yet
        if self.currentGenomeID < self.genomeCount:

            # Set fitness for genome with outcome, progress, time, coins, enemies
            if self.fitnessfunction == 1:
                if outcome == -1:
                    self.genomes[self.currentGenomeID][1].fitness = progress  # goes up until ~6500, and 50s for level
                    self.fitnesses.append(progress)
                elif outcome == +1:
                    self.genomes[self.currentGenomeID][1].fitness = 8000 + 500 - time
                    self.fitnesses.append(8000 + 500 - time)

            elif self.fitnessfunction == 2:
                if outcome == -1:
                    self.genomes[self.currentGenomeID][1].fitness = progress + coins*300
                elif outcome == +1:
                    self.genomes[self.currentGenomeID][1].fitness = 80000 + coins*300 + (5000 - (time*2))

            elif self.fitnessfunction == 3:
                if outcome == -1:
                    self.genomes[self.currentGenomeID][1].fitness = progress + coins*300 + enemies*300
                elif outcome == +1:
                    self.genomes[self.currentGenomeID][1].fitness = 80000 + coins*300 + enemies*300 + (5000 - (time*2))

            else:
                print("Error: Invalid fitness function")

            print("Genome", self.currentGenomeID, "has fitness:", self.genomes[self.currentGenomeID][1].fitness)


            # Go to next genome and reset level
            self.currentGenomeID += 1
            if not self.currentGenomeID == self.genomeCount:
                self.inputHandler.setGenome(self.genomes[self.currentGenomeID][1])
                self.game.initializeLevel()


        # If all genomes have been evaluated:
        else:
            # Else, go either to a new generation (if) or terminate training (else)
            if self.currentGeneration < 50:

                # Source of the following code: NEAT library's population.run() method.

                # Gather and report statistics.
                best = None
                for g in self.p.population.values():
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


                # Writing output into file
                # Note: This code got added by us and was not part of Population.run()
                with open('../data/ai/genomes/summary.txt', 'a') as file:
                    for sid in sorted(self.p.species.species):
                        # sid = species ID
                        s = self.p.species.species[sid]  # species
                        n = len(s.members)  # number members in species
                        file.write(str(sid) + "," + str(n))

                        for fitn in self.fitnesses:
                            file.write("," + str(fitn))
                    file.write("\n")


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



                # Note: Starting from here, the code got added by us and was not part of Population.run()

                # Save the best genome in folder
                name = "../data/ai/genomes/" + "Gen" + str(self.currentGeneration).zfill(2) + "_best.pickle"
                with open(name, "wb") as f:
                    pickle.dump(winner, f)

                # Move the checkpoint file
                name = "neat-checkpoint-" + str(self.currentGeneration)
                # Overwrite existing file
                if os.path.isfile(os.path.join("../data/ai/genomes/", name)):
                    os.remove(os.path.join("../data/ai/genomes/", name))
                shutil.move(os.path.join("", name), "../data/ai/genomes/")  # Move

                # Go to new generation
                self.genomes = list(self.p.population.items())
                self.genomeCount = len(self.genomes)
                self.currentGenomeID = 0
                self.currentGeneration += 1
                self.inputHandler.setGenome(self.genomes[self.currentGenomeID][1])
                self.p.reporters.start_generation(self.p.generation)  # todo: maybe bad
                self.fitnesses = []

            else:
                # Finish the algorithm and go back to title screen
                return StateTrainingCompleted(self.game.game, self.game)



