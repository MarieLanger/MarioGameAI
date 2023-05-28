import pygame
from .spriteBasic import SpriteBasic

class SpriteEnemy(SpriteBasic):
    """
    All sprites inherit from pygame.sprite.Sprite.
    Base class for all enemies
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got collected
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, player):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # References
        self.player = player



    def update(self):
        """
        What enemies do on their own, independent of player inputs

        - Check collisions first
            # Check if enemy collided with player
            if pygame.sprite.collide_rect(self, self.player):
        - Update enemy model (e.g. new position)
        """
        pass




