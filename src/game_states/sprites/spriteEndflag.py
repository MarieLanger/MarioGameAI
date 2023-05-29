import pygame

from .spriteBasic import SpriteBasic


class SpriteEndflag(SpriteBasic):
    """
    After touching this "flag", the level gets completed.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - game: reference to the game
        - player: reference to the player
    """

    def __init__(self, y_pos, x_pos, game, player):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # Shape and color of flag
        self.image = pygame.Surface((8, 16 * 2 * 4))
        self.image.fill((63, 234, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)

        # References
        self.game = game
        self.player = player

    def update(self):
        """
        What sprites do on their own, independent of player inputs.
        Flag checks for collisions with player.
        """

        if pygame.sprite.collide_rect(self, self.player):
            self.game.setLevelOutcome(+1)
