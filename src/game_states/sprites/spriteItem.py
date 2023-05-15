import pygame
from .spriteBasic import SpriteBasic

class SpriteItem(SpriteBasic):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic item
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, y_pos, x_pos, player):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # Item color
        self.image.fill((190,149,237))

        self.player = player


    def update(self):
        pass
