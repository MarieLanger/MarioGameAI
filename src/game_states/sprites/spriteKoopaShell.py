import pygame
from .spriteGoomba import SpriteGoomba

class SpriteKoopaShell(SpriteGoomba):
    """
    All sprites inherit from pygame.sprite.Sprite.
    Base class for all enemies
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - Coin needs to communicate to the game when it got collected
        - Coin needs to know the player's position to detect collisions
    """
    def __init__(self, y_pos, x_pos, player, blockgroup, enemygroup):
        SpriteGoomba.__init__(self, y_pos, x_pos, player, blockgroup)

        # It's not a circle but I like it lmao?
        self.image = pygame.Surface((28, 17), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (141,2,31), (14, 14), 14, 28)
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))

        # mask for pixel perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # Enemies have color
        self.image.fill((141,2,31))

        # Make a copy of the player's previous state
        self.playerPrevRect = self.player.rect.copy()

        # shells are not moving at the start
        self.direction = 0

        self.blockGroup = blockgroup
        self.enemyGroup = enemygroup

        self.velocityY = 0
        self.gravity = 0.5



    def update(self):
        """
        What enemies do on their own, independent of player inputs

        - Check collisions first
        - Update enemy model (e.g. new position)
        """

        print("before:  ", self.playerPrevRect.bottom, self.player.rect.bottom, self.rect.top)
        print("PLayer:", self.player.rect.topleft, self.player.rect.bottomright)
        print("Self:", self.rect.topleft, self.rect.bottomright)


        # todo: Pygame does not do pixel perfect collision
        # todo: which means that when the 2 things collide with each other only with 1 pixel, it does not get noticed
        # todo: https://stackoverflow.com/questions/62399078/how-to-use-pixel-perfect-collision-with-two-images-pygame
        # https://stackoverflow.com/questions/48025283/pixel-perfect-collision-detection-for-sprites-with-a-transparent-background
        # Check if enemy collided with player ------------------------------------------------------------------

        # top has collision AND (right side of player collided OR left side of player collided)
        if pygame.sprite.collide_rect(self, self.player):
        #if pygame.sprite.collide_mask(self, self.player):
            print("Collision!!")
            # If the previous player location was a collision, the collision already got handled before!
            #if not self.playerPrevRect.colliderect(self.rect):

            # If not, then handle collision
            # If the previous position was higher than the enemy, then the collision came from the top
            # Necessary because yeeting into the enemy from the side should not kill them
            # todo: note, changed it into <= (before: <)
            if self.playerPrevRect.bottom <= self.rect.top:
                print("Yo")


                # code for direction change goes here
                if self.direction != 0:
                    self.direction = 0  # if player stomped from going shell, stop shell
                else:
                    if self.player.rect.left < self.rect.left:
                        self.direction = +1  # if player stomped from left, go right
                    else:
                        self.direction = -1  # if player stomped from right, go left

                # todo: The problem seemed to be that i was so "deep" in the shell that even after I jumped up, I
                # was not able to get "out" of it.
                # The solution is now to just make the player jump higher
                self.player.velocityY = -17
                self.player.jumpKeyReleased()
            else:
                if not self.player.immunity:
                    player_hit = self.player.enemyHit()  # communicate that player got hit
                    # True if hit, False if player "hits back" via star
                    if not player_hit:
                        #self.player.velocityY = -11
                        #self.player.jumpKeyReleased()
                        self.kill()

        # Kill enemies
        enemyList = pygame.sprite.spritecollide(self,self.enemyGroup,False)
        print(enemyList)

        if self.direction != 0:
            if len(enemyList)!=0:
                for i in range(len(enemyList)):
                    if enemyList[i] is not self:
                        enemyList[i].kill()
        # Update previous position from player
        self.playerPrevRect = self.player.rect.copy()


        # Handle walking -----------------------------------------------------------------------------------------
        self.walking()
        self.walking()
        self.walking()

        self.rect.y += self.velocityY
        self.applyGravity()
        self.enforceNoVerticalClipping()


    # enforceNoVerticalClipping(), applyGravity(), walking(), checkCollisions() is taken from superclass

