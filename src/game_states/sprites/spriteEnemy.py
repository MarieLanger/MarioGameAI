from .spriteBasic import SpriteBasic


class SpriteEnemy(SpriteBasic):
    """
    The base class for all enemies.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: reference to the player
    """

    def __init__(self, y_pos, x_pos, player):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # References
        self.player = player

    def update(self):
        """
        What enemies do on their own, independent of player inputs.
        """
        pass
