from .spriteBasic import SpriteBasic


class SpriteEnemy(SpriteBasic):
    """
    The base class for all enemies.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: reference to the player
    """

    def __init__(self, y_pos, x_pos, player, game):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # References
        self.player = player
        self.game = game

    def update(self):
        """
        What enemies do on their own, independent of player inputs.
        """
        pass

    def kill(self):
        super().kill()
        self.game.increaseEnemyKillCounter()

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
            matrix[newy // 32, newx // 32, 0] = -1
