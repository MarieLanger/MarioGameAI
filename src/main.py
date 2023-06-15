import pygame

from game_states.stateTitle import StateTitle
# from controller.controllerClass import *
# from controller import controllerClass
from settings import *


class Game:
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
        # Event loop
        while True:
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
    print("Starting Super Princess Peach")
    game = Game()
    game.run()
