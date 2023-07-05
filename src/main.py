import pygame
import time

from game_states.stateTitle import StateTitle
# from controller.controllerClass import *
# from controller import controllerClass
from settings import *


class Main:
    """
    Main class which holds all the game components.
    """

    def __init__(self):
        """
        This method gets run when Game() gets initialized.
        """

        # Create state machine and push first state onto it
        self.stateMachine = StateMachine()
        self.stateMachine.push(StateTitle(self))  # title screen
        # Setup pygame
        pygame.init()
        # Game canvas is w=320, h=240
        self.gameCanvas = pygame.Surface((WIDTH, HEIGHT))

        # Upscale to: w=640, h=480
        self.screen = pygame.display.set_mode((WIDTH * 2, HEIGHT * 2))

        # Initialize clock
        self.clock = pygame.time.Clock()

    def run(self):
        """
        Run the actual game.
        """
        """start_time = time.time()
        with open('summary3WE.txt') as f:
            lines = f.readlines()
            generation = -1
            species = 999
            max = None
            mean = None

            # Iterate all generations
            for i in range(len(lines)):
                line = lines[i]
                tmp = line.split(",")

                if int(tmp[0])<species:
                    generation += 1

                species = int(tmp[0])
                # n = tmp[1]  --> not needed
                tmpArray = tmp[2:]
                tmpArray = list(map(int, tmpArray))

                sum = 0
                max = 0
                for i in range(len(tmpArray)):
                    sum += tmpArray[i]
                    if tmpArray[i] > max:
                        max = tmpArray[i]
                mean = int(sum/len(tmpArray))

                    #print(sum, mean)

                with open('converted_summary.txt', 'a') as file:
                    file.write(str(generation) + "," + str(species) + "," + str(max) + "," + str(mean) + "\n")
        print("--- %s seconds ---" % (time.time() - start_time))



        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np



        df = pd.read_csv('converted_summary.txt', header=None)



        x = df[0]
        species = df[1]
        max_values = df[2]
        values = df[3]

        unique_species = species.unique()
        species_codes = np.arange(len(unique_species))



        color_map = plt.cm.get_cmap('Set1',len(unique_species))



        group_1_species = unique_species[unique_species <=6]

        group_2_species = unique_species[unique_species >6]


        plt.figure(1)

        for i, spec in enumerate(group_1_species):
            mask = (species == spec)

            plt.plot(x[mask], values[mask], marker='',
                 linestyle=':', color=color_map(species_codes[i]), markersize=5)

            plt.plot(x[mask], max_values[mask], linestyle='-',
                 color=color_map(species_codes[i]))



        plt.xlabel('GenID')
        plt.ylabel('Fitness Values')
        plt.title('Species 1-6: Max - line, Mean - line')
        plt.grid(True)


        legend_elements_1 = [plt.Line2D([0],
                                        [0], marker='o', color='w',
                                        label=spec,
                                        markerfacecolor=color_map(species_codes[i]), markersize=8)

                             for i, spec in enumerate(group_1_species)]

        plt.legend(handles=legend_elements_1, title='Species', bbox_to_anchor=(1.02,1), loc='upper left')


        plt.figure(2)

        for i, spec in enumerate(group_2_species):
            mask = (species == spec)

            plt.plot(x[mask], values[mask], marker='',
                 linestyle=':', color=color_map(species_codes[i]), markersize=5)
            plt.plot(x[mask], max_values[mask], linestyle='-',
                 color=color_map(species_codes[i]))



        plt.xlabel('GenID')
        plt.ylabel('Fitness Values')
        plt.title('Species 7-12: Max - line, Mean - line')
        plt.grid(True)

        legend_elements_2 = [plt.Line2D([0],
                                        [0], marker='o', color='w',
                                        label=spec,

                                        markerfacecolor=color_map(species_codes[i]), markersize=8)

                             for i, spec in enumerate(group_2_species)]

        plt.legend(handles=legend_elements_2, title='Species', bbox_to_anchor=(1.02,
                                                                               1), loc='upper left')

        plt.show()"""






# Event loop -----------------------------------------------------------------
        while True:
            #print(self.clock.get_fps())
            # Get state which lies on top of stack
            topState = self.stateMachine.peek()

            # Handle events and update underlying model accordingly
            newState = topState.update()

            # HandleInputs returns something when a new state has to be entered
            if newState is not None:
                self.stateMachine.push(newState)

            # Display current model
            topState.display(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

    def exitCurrentState(self):
        self.stateMachine.pop()


class StateMachine():
    """
    State machine which keeps track of all the game states.
    Contains a statestack where the states get stored.
    States in the statestack need to implement handleInputs() and display()
    """

    def __init__(self):
        self.stateStack = []

    # Looks onto top of stack without altering it
    def peek(self):
        try:
            return self.stateStack[-1]
        except IndexError:  # if stack empty
            return None

    # Pushes new state onto the stack
    def push(self, state):
        self.stateStack.append(state)
        return

    # Removes top element and returns it
    def pop(self):
        if len(self.stateStack) < 1:
            return None
        else:
            self.stateStack.pop()


if __name__ == '__main__':
    print("Starting Super M[ai]RIO BROS")
    game = Main()
    game.run()
