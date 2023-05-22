import pygame
import pygame.gfxdraw
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
        #self.image.fill((190,149,237))

        self.player = player

        points = [(6, 14),(16,4),  (26,14), (16,24)]

        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.gfxdraw.filled_polygon(self.image, points, (63,234,255))
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))




    def update(self):
        pass