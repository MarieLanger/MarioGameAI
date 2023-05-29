import pygame
from .spriteBlock import SpriteBlock


class SpritePipe(SpriteBlock):
    """
    A pipe is basically a block, but bigger and varies in height.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - height: int-value of height in pixels
    """

    def __init__(self, y_pos, x_pos, height):
        SpriteBlock.__init__(self, y_pos, x_pos)

        # Redoing drawing because the height differs
        self.image = pygame.Surface((16 * 2, height))
        self.image.fill((46, 133, 87))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
