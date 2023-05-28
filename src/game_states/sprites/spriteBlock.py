import pygame
from .spriteBasic import SpriteBasic

class SpriteBlock(SpriteBasic):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic block sprite that does nothing
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, y_pos, x_pos):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # Block-color
        #self.image.fill((118,134,146))
        self.image.fill((98,114,126))





    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """
