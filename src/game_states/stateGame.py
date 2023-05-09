import pygame
import sys
from .state import State
#from .stateTitle import StateTitle    no!!!! because we want to exit this state, not put another title on top of it!!
#otherwise circular dependency!!!!!!

class StateGame(State):
    """
    State for when the game gets played
    """

    def __init__(self, game):
        self.game = game


    def handleInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game.exitCurrentState()

    def display(self, screen):
        screen.fill('black')

        #Update everything
        pygame.display.update()


