import json
import sys
import os

import pygame

from .state import State



class StateOther(State):
    """
    The title state for when the game gets started.
    Allows the user to navigate to other states, such as the gameplay-state, as well as to select options.
    """

    def __init__(self, game):
        State.__init__(self, game)

        # Initialize all the text
        self.text = "SUPER M[ai]RIO BROS"
        self.text_pos = (80, 20)  # x-position(low:left,high:right)   y-position (low:up, high:down)
        self.text_col = (255, 255, 255)

        self.description = """
        Nowadays, traditional methods to save one's princess 
        (e.g."saving the princess yourself") are no longer 
        trendy. To go with the modern times, Mario has decided
        to entrust the saving of his dear princess to various
        neural networks created by the NEAT algorithm (Stanley 
        et al., 2002). 
        Will they be able to clear all obstacles and finish all 
        levels successfully? Only one way to find out.... 
        
        (Press X to go back to the title screen.)
"""

        # Initialize fonts
        pygame.font.init()
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 19)
        self.mediumFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.bigFont = pygame.font.SysFont('Comic Sans MS', 45)



    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Switch from main menu to submenu
                if event.key == pygame.K_x:
                    self.game.exitCurrentState()
        return None

    def display(self, screen):
        screen.fill('black')

        # Title
        x_pos = (640 - self.bigFont.size(self.text)[0]) / 2
        self._displayText(self.text, self.text_col, (x_pos, self.text_pos[1]), self.bigFont, screen)


        self._displayText(self.description, self.text_col, (0, 90), self.smallFont, screen)

    def _displayText(self, content, color, position, font, screen):
        """
        Helper function to display text.
        """
        textSurface = font.render(content, False, color)
        screen.blit(textSurface, position)

