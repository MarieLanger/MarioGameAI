import pygame
from .spriteEnemy import SpriteEnemy

class SpritePiranha(SpriteEnemy):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A piranha sprite that moved up or down
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got collected
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, player):
        SpriteEnemy.__init__(self, y_pos, x_pos, player)

        # Enemies have color
        self.image.fill((141,2,31))

        self.time = 0



    def update(self):
        """
        What enemies do on their own, independent of player inputs

        - Check collisions first
        - Update enemy model (e.g. new position)
        """

        # Check if enemy collided with player ------------------------------------------------------------------
        if pygame.sprite.collide_rect(self, self.player):
            self.player.enemyHit()  # communicate that player got hit


        # Handle movement -----------------------------------------------------------------------------------------

        # Depending on "time" passed, do other things
        if self.time < 50:
            pass  # stay up [0:49]
        elif self.time < 83:
            self.rect.y += 1 # go down [50:82]
        elif self.time < 133:
            pass  # stay down [83:132]
        elif self.time < 166:
            self.rect.y -= 1  # go up [133:166]
        else: # when time=1000
            self.time = 0

        self.time += 1
