import pygame
from .spriteGoomba import SpriteGoomba


class SpriteKoopaShell(SpriteGoomba):
    """
    A shell that gets dropped from a Koopa.
    If player jumps on its left side, it slides to the right, if on right side, it slides to the left.
    While sliding, it can hit both the player and other enemies.
    When jumping on a sliding shell, the shell gets stopped. If it doesn't move, it cannot kill enemies,
    but hit the player.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: reference to the player
        - blockgroup, enemygroup: references to the respective sprite groups
    """

    def __init__(self, y_pos, x_pos, player, blockgroup, enemygroup):
        SpriteGoomba.__init__(self, y_pos, x_pos, player, blockgroup)

        # References
        self.blockGroup = blockgroup
        self.enemyGroup = enemygroup

        # Shape and color of Koopa shell
        self.image = pygame.Surface((28, 17), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (141, 2, 31), (14, 14), 14, 28)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.image.fill((141, 2, 31))

        # Make a copy of the player's previous state
        self.playerPrevRect = self.player.rect.copy()

        # shells are not moving at the start
        self.direction = 0

    def update(self):
        """
        What enemies do on their own, independent of player inputs

        - Check collisions first
        - Update enemy model (e.g. new position)
        """

        # top has collision AND (right side of player collided OR left side of player collided)
        if pygame.sprite.collide_rect(self, self.player):
            # If the previous position was higher than the enemy, then the collision came from the top
            if self.playerPrevRect.bottom <= self.rect.top:
                # Direction change
                if self.direction != 0:
                    self.direction = 0  # if player stomped from going shell, stop shell
                else:
                    if self.player.rect.left < self.rect.left:
                        self.direction = +1  # if player stomped from left, go right
                    else:
                        self.direction = -1  # if player stomped from right, go left

                # todo: The problem seemed to be that i was so "deep" in the shell that even after I jumped up, I
                # todo: was not able to get "out" of it.
                # todo: The solution is now to just make the player jump higher
                self.player.velocityY = -17
                self.player.jumpKeyReleased()
            else:
                if not self.player.immunity:
                    player_hit = self.player.enemyHit()  # communicate that player got hit
                    # True if hit, False if player "hits back" via star
                    if not player_hit:
                        self.kill()

        # Kill enemies if moving currently
        if self.direction != 0:
            enemyList = pygame.sprite.spritecollide(self, self.enemyGroup, False)
            if len(enemyList) != 0:
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
