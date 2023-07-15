import pygame
import sys
from ..state import State

class LevelEndHandler():
    def __init__(self, game):
        self.game = game

    def handleLevelEnd(self, outcome, progress, time, coins, enemies):
        """
        This method gets called after either the level got completed or a game over happened.

        :param outcome: Game over (-1) or level completed (+1)
        :param progress: Progress in pixels
        :param time: Time taken in seconds
        :param coins: Coins obtained (int)
        :param enemies: Enemies killed (int)
        :return:
        """
        pass







