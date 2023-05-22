import pygame
from .spriteBasic import SpriteBasic

class SpriteCoin(SpriteBasic):
    """
    All sprites inherit from pygame.sprite.Sprite.
    Coin which can be collected
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got collected
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, game, player):
        SpriteBasic.__init__(self, y_pos, x_pos)



        # Coin has color
        #self.image.fill((255,223,0))


        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (212,175,55), (14, 14), 14, 28)
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))







        # References
        self.game = game
        self.player = player



    def update(self):
        """
        What sprites do on their own, independent of player inputs
        """

        if pygame.sprite.collide_rect(self, self.player):
            self.game.increaseCoinCounter()
            self.kill()


