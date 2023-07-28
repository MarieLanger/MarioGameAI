import pygame
import sys
from .spriteItem import SpriteItem
from .importFolder import import_folder


class SpriteCoin(SpriteItem):
    """
    A coin which can be collected.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - game: Coin needs to communicate to the game when it got collected (=game is a reference)
        - player: Coin needs to know the player's position to detect collisions (=player is a reference)
    """

    def __init__(self, y_pos, x_pos, game, player):
        SpriteItem.__init__(self, y_pos, x_pos, player)

        # Coin is a circle and has a color
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (182, 155, 25), (14, 14), 14, 28)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

        # References
        self.game = game
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'Coin'

    def import_character_assets(self):
        character_path = sys.path[1] + '/data/Graphics/'
        self.animations = {'Coin': []}

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
        What sprites do on their own, independent of player inputs.
        Coin checks if player touched it and if yes, increase the coin counter.
        """
        if pygame.sprite.collide_rect(self, self.player):
            self.game.increaseCoinCounter()
            self.kill()

        self.animate()

    def writeState(self, matrix, playerX, playerY):
        """
        Writing its own position into the state.
        :param matrix:
        :param playerX:
        :param playerY:
        :return:
        """
        if self._withinStateMatrix(playerX, playerY, self.rect.x, self.rect.y):
            # Normalize positions
            newx = self.rect.x - (playerX + self.normX)
            newy = self.rect.y - (playerY + self.normY)

            # Save state in first matrix
            matrix[newy // 32, newx // 32, 1] = -1
