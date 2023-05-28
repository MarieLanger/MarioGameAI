import pygame
import random
from .spriteItem import SpriteItem

class SpriteStar(SpriteItem):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic item
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, y_pos, x_pos, player, blockgroup):
        SpriteItem.__init__(self, y_pos, x_pos, player)

        self.velocityY = 0
        self.gravity = 0.5

        self.direction = +1
        self.blockGroup = blockgroup

        self.counter = 20
        self.nextJump = random.randint(30, 80)

        self.activated = False



    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            top_state = self.player.peekState()
            top_state.handleItemCollision("star")
            self.kill()

        if self.activated:
            self.walking()
            self.rect.y += self.velocityY
            self.applyGravity()
            self.enforceNoVerticalClipping()

            # Simulate jumping behaviour of star
            self.counter += 1
            if self.counter==self.nextJump:
                self.counter = 0
                self.nextJump = random.randint(20, 60)
                self.velocityY = -7

    def activate(self):
        self.activated = True


    def enforceNoVerticalClipping(self):
        col_list = pygame.sprite.spritecollide(self, self.blockGroup, False)
        if len(col_list) == 0:
            return  # No clipping, wonderful, we can stop here
        else:
            for collided in col_list:

                x_col = not (self.rect.right < collided.rect.left or self.rect.left > collided.rect.right)
                y_col = not (self.rect.bottom < collided.rect.top or self.rect.top > collided.rect.bottom)
                if x_col and y_col:

                    # collision on top
                    if self.rect.top <= collided.rect.bottom and self.rect.top >= collided.rect.top:
                        self.rect.top = collided.rect.bottom #+1
                        self.velocityY = 0

                    # collision at the bottom
                    if self.rect.bottom >= collided.rect.top and self.rect.bottom <= collided.rect.bottom:
                        # Place on top of sprite
                        self.rect.bottom = collided.rect.top #- 1
                        self.velocityY = 0  # set y-velocity to zero so that the sprite stops jumping



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