import pygame
from .spriteGoomba import SpriteGoomba
from .spriteKoopaShell import SpriteKoopaShell

class SpriteKoopa(SpriteGoomba):
    """
    All sprites inherit from pygame.sprite.Sprite.
    Base class for all enemies
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got collected
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, player, blockgroup, enemygroup, envgroup):
        SpriteGoomba.__init__(self, y_pos, x_pos, player, blockgroup)

        self.image = pygame.Surface((16*2,32*2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos,y_pos)

        # Enemies have color
        self.image.fill((141,2,31))

        # Make a copy of the player's previous state
        self.playerPrevRect = self.player.rect.copy()

        # Goombas can walk left or right
        self.direction = +1

        self.blockGroup = blockgroup
        self.enemyGroup = enemygroup
        self.envGroup = envgroup

        self.velocityY = 0
        self.gravity = 0.5



    def update(self):
        """
        What enemies do on their own, independent of player inputs

        - Check collisions first
        - Update enemy model (e.g. new position)
        """

        print("before:  ", self.playerPrevRect.bottom, self.player.rect.bottom, self.rect.top, pygame.sprite.collide_rect(self, self.player))

        # Check if enemy collided with player ------------------------------------------------------------------
        if pygame.sprite.collide_rect(self, self.player):
            print("Collision!")

            # If the previous player location was a collision, the collision already got handled before!
            #if not self.playerPrevRect.colliderect(self.rect):

            # If not, then handle collision
            # If the previous position was higher than the enemy, then the collision came from the top
            # Necessary because yeeting into the enemy from the side should not kill them
            if self.playerPrevRect.bottom <= self.rect.top:
                self.player.velocityY = -11
                self.player.jumpKeyReleased()
                self._createKoopaShell()
                self.kill()
            else:
                if not self.player.immunity:
                    print("WHY ARE YOU HERE")
                    print(self.playerPrevRect.bottom, self.rect.top)
                    player_hit = self.player.enemyHit()  # communicate that player got hit
                    # True if hit, False if player "hits back" via star
                    if not player_hit:
                        self.player.velocityY = -11
                        self.player.jumpKeyReleased()
                        self._createKoopaShell()
                        self.kill()

        # Update previous position from player
        self.playerPrevRect = self.player.rect.copy()
        print("after:  ", self.playerPrevRect.bottom, self.player.rect.bottom,self.rect.top)


        # Handle walking -----------------------------------------------------------------------------------------
        self.walking()

        self.rect.y += self.velocityY
        self.applyGravity()
        self.enforceNoVerticalClipping()


    # enforceNoVerticalClipping(), applyGravity(), walking(), checkCollisions() is taken from superclass


    def _createKoopaShell(self):
        new_sprite = SpriteKoopaShell(self.rect.y+32, self.rect.x, self.player, self.blockGroup, self.enemyGroup)
        self.envGroup.add(new_sprite)
        self.enemyGroup.add(new_sprite)
