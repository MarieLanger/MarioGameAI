import pygame
import sys
import numpy as np

from .inputHandler import InputHandler

class InputHandlerAI(InputHandler):
    def __init__(self, game):
        """
        A class that handles the AI inputs during gameplay.
        :param state:
        """
        InputHandler.__init__(self, game)

        self.gameState = np.zeros((8, 10))
        self.itemState = np.zeros(3)  # normal, big, star


    def handleInputs(self):
        # Check pygame inputs and close window if necessary
        self._getUserInputs()

        # Get game states
        self._getGameState()
        self._getItemState()

        # todo: Feed states to model and calculate output

        # todo: Adjust game.rightKeyHold + game.leftKeyHold + game.upKeyHold + game.player.jumpKeyReleased()





    def _getItemState(self):
        states = self.game.getAllStates()
        for state in states:
            self.itemState[state.getID()] = 1

    def _getGameState(self):
        # MATRIX:
        # 2 tiles behind player, 7 tiles in front of player --> x:10
        # 2 tiles under player, 5 tiles above player --> y: 8

        playerX = self.game.player.rect.x
        playerY = self.game.player.rect.bottom

        # Reset matrix
        self.gameState = np.zeros((8,10,2))

        # Idea: Delegate to sprites. Then sprites can decide whether or not they write or what they write
        for sprite in self.game.env_sprites.sprites():
            sprite.writeState(self.gameState, playerX, playerY)

        print(self.gameState[:,:,1])

    def _getUserInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.game.exitCurrentState()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self.game.game.exitCurrentState()
