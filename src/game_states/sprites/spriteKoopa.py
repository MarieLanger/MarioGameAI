import pygame

from .spriteGoomba import SpriteGoomba
from .spriteKoopaShell import SpriteKoopaShell


class SpriteKoopa(SpriteGoomba):
    """
    A Koopa which is 2 tiles high.
    Behaves like a Goomba, with the addition of dropping a Koopa Shell when being hit from above (not star!).
    Koopa shell: See file spriteKoopaShell.py
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - blockgroup, enemygroup, envgroup: References to the respective sprite groups
    """

    def __init__(self, y_pos, x_pos, player, blockgroup, enemygroup, envgroup, game):
        SpriteGoomba.__init__(self, y_pos, x_pos, player, blockgroup, game)

        # References
        self.blockGroup = blockgroup
        self.enemyGroup = enemygroup
        self.envGroup = envgroup

        # Koopa is bigger than Goomba
        self.image = pygame.Surface((16 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
        self.image.fill((141, 2, 31))

        # Make a copy of the player's previous state
        self.playerPrevRect = self.player.rect.copy()


    def update(self):
        """
        What enemies do on their own, independent of player inputs
        Checks for collisions and acts according to class-description.
        """

        # Check if enemy collided with player ------------------------------------------------------------------
        if pygame.sprite.collide_rect(self, self.player):
            # If the previous position was higher than the enemy, then the collision came from the top
            if self.playerPrevRect.bottom <= self.rect.top:
                self.player.velocityY = -11
                self.player.jumpKeyReleased()
                self._createKoopaShell()
                self.kill()
            else:
                # If player came from side, communicate that player got hit
                player_hit = self.player.enemyHit()
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


    def _createKoopaShell(self):
        new_sprite = SpriteKoopaShell(self.rect.y + 32, self.rect.x, self.player, self.blockGroup, self.enemyGroup, self.game)
        self.envGroup.add(new_sprite)
        self.enemyGroup.add(new_sprite)

    # enforceNoVerticalClipping(), applyGravity(), walking(), checkCollisions() is taken from superclass
