import pygame
from .spriteEnemy import SpriteEnemy

class SpriteGoomba(SpriteEnemy):
    """
    All sprites inherit from pygame.sprite.Sprite.
    Base class for all enemies
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got collected
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, player, blockgroup):
        SpriteEnemy.__init__(self, y_pos, x_pos, player)

        # Enemies have color
        self.image.fill((141,2,31))

        # Make a copy of the player's previous state
        self.playerPrevRect = self.player.rect.copy()

        # Goombas can walk left or right
        self.direction = -1

        self.blockGroup = blockgroup

        self.velocityY = 0
        self.gravity = 0.5



    def update(self):
        """
        What enemies do on their own, independent of player inputs

        - Check collisions first
        - Update enemy model (e.g. new position)
        """

        # Check if enemy collided with player ------------------------------------------------------------------
        if pygame.sprite.collide_rect(self, self.player):
            print("yeee")

            # If the previous player location was a collision, the collision already got handled before!
            #if not self.playerPrevRect.colliderect(self.rect):

            # If not, then handle collision
            # If the previous position was higher than the enemy, then the collision came from the top
            # Necessary because yeeting into the enemy from the side should not kill them
            if self.playerPrevRect.bottom < self.rect.top:
                self.kill()
            else:
                if not self.player.immunity:
                    player_hit = self.player.enemyHit()  # communicate that player got hit
                    # True if hit, False if player "hits back" via star
                    if not player_hit:
                        self.kill()

        # Update previous position from player
        self.playerPrevRect = self.player.rect.copy()


        # Handle walking -----------------------------------------------------------------------------------------
        self.walking()

        self.rect.y += self.velocityY
        self.applyGravity()
        self.enforceNoVerticalClipping()


    def enforceNoVerticalClipping(self):
        # todo: Same code as in spritePlayer() --> Code duplication!
        col_list = pygame.sprite.spritecollide(self, self.blockGroup, False)
        if len(col_list) == 0:
            return  # No clipping, wonderful, we can stop here
        else:
            for collided in col_list:
                if not (self.rect.bottom < collided.rect.top or self.rect.top > collided.rect.bottom):
                    # collision at the bottom
                    if self.rect.bottom >= collided.rect.top and self.rect.bottom <= collided.rect.bottom:
                        # Place on top of sprite
                        self.rect.bottom = collided.rect.top #- 1
                        self.velocityY = 0  # set y-velocity to zero


    def applyGravity(self):
        # todo: The exact same as in spritePlayer() --> Code duplication
        # terminal velocity
        if self.velocityY + self.gravity > 6:
            self.velocityY = 6
        else:
            self.velocityY += self.gravity


    def walking(self):
        self.rect.x += self.direction*2

        adjusted_pos = self._checkCollisions()

        if adjusted_pos == 0:
            return
        else:
            self.rect.x += adjusted_pos*self.direction
            self.direction = self.direction*(-1)


    def _checkCollisions(self):
        """
        Checks if after walking, peach clipped into something.
        If yes, adjust x-position of everything
        :return: 0: If nothing needs to be changed, -2 if position has to be adjusted by 2 to the left, etc
        """
        # todo: This is the exact same method that stateGame() has, so code duplication! = bad
        move = 0
        col_list = pygame.sprite.spritecollide(self, self.blockGroup, False)
        if len(col_list) == 0:
            return move # No clipping occured
        else:
            for collided in col_list:

                # Then player collided with right side
                if self.rect.left < collided.rect.left:
                    # If a collision happened
                    if self.rect.right > collided.rect.left:
                        # put to the left of it
                        if abs(collided.rect.left - self.rect.right) > abs(move):
                            move = collided.rect.left - self.rect.right

                # Else, player collided with left side
                else:
                    if self.rect.left < collided.rect.right:
                        # put to the left of it
                        if abs(collided.rect.right - self.rect.left) > abs(move):
                            move = self.rect.left - collided.rect.right

            # At the end, return the absolute biggest move
            return move





