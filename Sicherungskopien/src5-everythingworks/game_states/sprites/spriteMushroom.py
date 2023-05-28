import pygame
from .spriteItem import SpriteItem

class SpriteMushroom(SpriteItem):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic item
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, y_pos, x_pos, player):
        SpriteItem.__init__(self, y_pos, x_pos, player)



    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            top_state = self.player.peekState()
            top_state.handleItemCollision("mushroom")
            self.kill()