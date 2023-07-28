import pygame
import sys
from .importFolder import import_folder
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

        # Piranha flower is 2 tiles high
        self.image = pygame.Surface((16 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)

        self.time = 0
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'flower'

    def import_character_assets(self):
        character_path = sys.path[1] + '/data/Graphics/'
        self.animations = {'flower': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

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
        elif self.time < 50+32*2+1+1: #83:
            self.rect.y += 1  # go down [50:82]
        elif self.time < 50+32*2+1+50+1+1: #133:
            pass  # stay down [83:132]
        elif self.time < 50+32*2+1+50+1+32*2+1+1:#166:
            self.rect.y -= 1  # go up [133:166]
        else:  # when time=1000
            self.time = 0

        self.time += 1

        self.animate()


    def writeState(self, matrix, playerX, playerY):
        """
        Writing its own position into the state.
        :param matrix:
        :param playerX:
        :param playerY:
        :return:
        """
        height = 2

        for tile in range(height):
            if self._withinStateMatrix(playerX, playerY, self.rect.x, self.rect.y + 32*tile):
                # Normalize positions
                newx = self.rect.x - (playerX + self.normX)
                newy = self.rect.y + 32*tile - (playerY + self.normY)

                # Save state in first matrix
                matrix[newy // 32, newx // 32, 0] = -1
