import pygame

from .spriteEnemy import SpriteEnemy


class SpritePiranha(SpriteEnemy):
    """
    A piranha sprite that moves up or down.
    Is supposed to be put on top of pipes.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: reference to the player
    """

    def __init__(self, y_pos, x_pos, player, game):
        SpriteEnemy.__init__(self, y_pos, x_pos, player, game)

        # Enemies have color
        self.image.fill((141, 2, 31))

        self.time = 0

    def update(self):
        """
        What enemies do on their own, independent of player inputs.
        The flower checks for collisions and checks when to move up/down.
        """

        # Check if enemy collided with player
        if pygame.sprite.collide_rect(self, self.player):
            player_hit = self.player.enemyHit()
            # True if hit, False if player "hits back" via star
            if not player_hit:
                self.kill()

        # Depending on time passed, do adjust position
        if self.time < 50:
            pass  # stay up [0:49]
        elif self.time < 83:
            self.rect.y += 1  # go down [50:82]
        elif self.time < 133:
            pass  # stay down [83:132]
        elif self.time < 166:
            self.rect.y -= 1  # go up [133:166]
        else:  # when time=1000
            self.time = 0

        self.time += 1
