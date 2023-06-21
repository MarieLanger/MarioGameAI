import pygame
import sys
from .levelEndHandler import LevelEndHandler
from ..stateLevelCompleted import StateLevelCompleted
from ..stateGameOver import StateGameOver

class StandardPlayHandler(LevelEndHandler):
    def __init__(self, game):
        """
        A class that handles the inputs from humans during gameplay.
        :param state:
        """
        LevelEndHandler.__init__(self, game)

    def handleLevelEnd(self, outcome, progress, time, coins, enemies):
        # If game over
        if outcome == -1:
            return StateGameOver(self.game.game, self.game)
        # If level completed
        elif outcome == +1:
            return StateLevelCompleted(self.game.game, self.game)
