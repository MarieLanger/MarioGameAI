import pygame

from .spriteBasic import SpriteBasic


class SpriteCoin(SpriteBasic):
    """
    A coin which can be collected.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - game: Coin needs to communicate to the game when it got collected (=game is a reference)
        - player: Coin needs to know the player's position to detect collisions (=player is a reference)
    """

    def __init__(self, y_pos, x_pos, game, player):
        SpriteBasic.__init__(self, y_pos, x_pos)

        # Coin is a circle and has a color
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (182, 155, 25), (14, 14), 14, 28)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

        # References
        self.game = game
        self.player = player

    def update(self):
        """
        What sprites do on their own, independent of player inputs.
        Coin checks if player touched it and if yes, increase the coin counter.
        """
        if pygame.sprite.collide_rect(self, self.player):
            self.game.increaseCoinCounter()
            self.kill()
