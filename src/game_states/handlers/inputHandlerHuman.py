import pygame
import sys
from .inputHandler import InputHandler

class InputHandlerHuman(InputHandler):
    def __init__(self, game):
        """
        A class that handles the inputs from humans during gameplay.
        :param state:
        """
        InputHandler.__init__(self, game)

    def handleInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.game.exitCurrentState()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.game.game.exitCurrentState()
                if event.key == pygame.K_RIGHT:
                    self.game.rightKeyHold = True
                if event.key == pygame.K_LEFT:
                    self.game.leftKeyHold = True
                if event.key == pygame.K_UP:
                    self.game.upKeyHold = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.game.rightKeyHold = False
                if event.key == pygame.K_LEFT:
                    self.game.leftKeyHold = False
                if event.key == pygame.K_UP:
                    self.game.upKeyHold = False
