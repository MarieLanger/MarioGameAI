import pygame
from .spriteBlock import SpriteBlock


class SpritePipe(SpriteBlock):
    """
    A pipe is basically a block, but bigger and varies in height.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - height: int-value of height in pixels
    """

    def __init__(self, y_pos, x_pos, height):
        SpriteBlock.__init__(self, y_pos, x_pos)

        # Redoing drawing because the height differs
        self.image = pygame.Surface((16 * 2, height))
        self.image.fill((46, 133, 87))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)

        self.height = height//32

    def writeState(self, matrix, playerX, playerY):
        """
        Writing its own position into the state.
        :param matrix:
        :param playerX:
        :param playerY:
        :return:
        """

        for tile in range(self.height):
            if self._withinStateMatrix(playerX, playerY, self.rect.x, self.rect.y + 32*tile):
                # Normalize positions
                newx = self.rect.x - (playerX - 2*32)
                newy = self.rect.y + 32*tile - (playerY - 6*32)

                # Save state in first matrix
                matrix[newy // 32, newx // 32, 0] = +1