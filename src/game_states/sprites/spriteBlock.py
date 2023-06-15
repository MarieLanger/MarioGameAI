from .spriteBasic import SpriteBasic


class SpriteBlock(SpriteBasic):
    """
    A basic block sprite (=obstacle).
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """

    def __init__(self, y_pos, x_pos):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # Block has a color
        self.image.fill((98, 114, 126))

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
            newx = self.rect.x - (playerX - 2*32)
            newy = self.rect.y - (playerY - 6*32)

            # Save state in first matrix
            matrix[newy // 32, newx // 32, 0] = +1

