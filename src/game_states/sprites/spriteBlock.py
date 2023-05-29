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

