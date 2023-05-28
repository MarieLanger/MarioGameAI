import pygame
from .spriteBasic import SpriteBasic

class SpriteEndflag(SpriteBasic):
    """
    All sprites inherit from pygame.sprite.Sprite.
    End flag, after touching level gets completed
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got touched
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, game, player):
        SpriteBasic.__init__(self, y_pos, x_pos)

        self.image = pygame.Surface((8,16*2*4))

        # Color of flag
        self.image.fill((63,234,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos,y_pos)








        # References
        self.game = game
        self.player = player



    def update(self):
        """
        What sprites do on their own, independent of player inputs
        """

        if pygame.sprite.collide_rect(self, self.player):
            self.game.setLevelOutcome(+1)


