import pygame

from .spriteEnemy import SpriteEnemy


class SpriteGoomba(SpriteEnemy):
    """
    A goomba that moves left/right. When hitting a block, it changes its direction. May also fall off cliffs.
    When hitting an enemy from above, the enemy dies.
    When the enemy hits the player horizontally, the enemy delegates the response to the player, as the player might
    get hit or might hit back depending on its current item-state.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: reference to the player
        - blockgroup: reference to the respective sprite group
    """

    def __init__(self, y_pos, x_pos, player, blockgroup, game):
        SpriteEnemy.__init__(self, y_pos, x_pos, player, game)

        # Enemies have color
        self.image.fill((141, 2, 31))

        # References (self.player already got declared in superclass)
        self.blockGroup = blockgroup

        # Make a copy of the player's previous state
        self.playerPrevRect = self.player.rect.copy()

        # Goombas can walk left or right, have a Y-velocity and gravity exists
        self.direction = -1
        self.velocityY = 0
        self.gravity = 0.5

    def update(self):
        """
        What enemies do on their own, independent of player inputs
        Checks collisions first and then updates the enemy model. See class-description.
        """

        # Check if enemy collided with player ------------------------------------------------------------------
        if pygame.sprite.collide_rect(self, self.player):
            # If the previous position was higher than the enemy, then the collision came from the top
            # Necessary because yeeting into the enemy from the side should not kill them
            if self.playerPrevRect.bottom <= self.rect.top:  # before: <
                self.player.velocityY = -11
                self.player.jumpKeyReleased()
                # --------
                self.kill()

            else:
                # If player came from side, communicate that player got hit
                player_hit = self.player.enemyHit()  # todo: false
                # True if hit, False if player "hits back" via star
                if not player_hit:
                    self.kill()  # todo: it goes there
                # If the player got hit, the enemy does not care!

        # Update previous position from player
        self.playerPrevRect = self.player.rect.copy()

        # Handle walking -----------------------------------------------------------------------------------------
        self.walking()

        self.rect.y += self.velocityY
        self.applyGravity()
        self.enforceNoVerticalClipping()

    def enforceNoVerticalClipping(self):
        """
        Check if there occured any vertical collisions while applying gravity.
        """
        col_list = pygame.sprite.spritecollide(self, self.blockGroup, False)
        if len(col_list) != 0:
            for collided in col_list:
                if not (self.rect.bottom < collided.rect.top or self.rect.top > collided.rect.bottom):
                    # If there was collision at the bottom, place on top of sprite + set Y-velocity to zero
                    if self.rect.bottom >= collided.rect.top and self.rect.bottom <= collided.rect.bottom:
                        self.rect.bottom = collided.rect.top
                        self.velocityY = 0

    def applyGravity(self):
        """
        Updates Y-velocity according to gravity. The terminal velocity is 6.
        """
        if self.velocityY + self.gravity > 6:
            self.velocityY = 6
        else:
            self.velocityY += self.gravity


    def walking(self):
        """
        Walks 2 pixels to the right and checks if collisions occured.
        Adjusts position accordingly if there were collisions.
        """
        self.rect.x += self.direction * 2

        adjusted_pos = self._checkCollisions()
        if adjusted_pos != 0:
            self.rect.x += adjusted_pos * self.direction
            self.direction = self.direction * (-1)


    def _checkCollisions(self):
        """
        Checks if after walking, peach clipped into something.
        If yes, adjust x-position of everything
        :return: 0: If nothing needs to be changed, -2 if position has to be adjusted by 2 to the left, etc
        """
        move = 0
        col_list = pygame.sprite.spritecollide(self, self.blockGroup, False)
        if len(col_list) == 0:
            return move  # No clipping occured
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
