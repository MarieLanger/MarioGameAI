import pygame

from .spriteItem import SpriteItem


class SpriteMushroom(SpriteItem):
    """
    A mushroom that gives Peach "an extra life" and makes her taller.
    When hit, peach goes back to original state and is immune against enemy attacks temporarily.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: reference to the player
        - blockgroup: reference to the respective sprite group
    """

    def __init__(self, y_pos, x_pos, player, blockgroup):
        SpriteItem.__init__(self, y_pos, x_pos, player)

        # References (self.player got set in superclass)
        self.blockGroup = blockgroup

        self.velocityY = 0
        self.gravity = 0.5
        self.direction = +1

        # When activated, movement starts, prevents moving from the very start when still in container
        self.activated = False

    def activate(self):
        self.activated = True

    def update(self):
        """
        What items do on their own, independent of player inputs.
        Checks collisions with the player and "walks" similarly to Goombas.
        """
        if pygame.sprite.collide_rect(self, self.player):
            top_state = self.player.peekState()
            top_state.handleItemCollision("mushroom")
            self.kill()

        if self.activated:
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
