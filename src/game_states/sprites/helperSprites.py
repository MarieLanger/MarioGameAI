import pygame


class GameOverSprite(pygame.sprite.Sprite):
    """
    Detects when player falls down a hole and communicates game over.
    """

    def __init__(self, player, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320 * 2, 20))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, 440)

        self.player = player
        self.game = game

    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.game.setLevelOutcome(-1)


class KillEnvironmentSpritesSprite(pygame.sprite.Sprite):
    """
    Kills sprites after they move outside of the screen to the left.
    Killing off sprites leads to less collision-comparisons.
    """

    def __init__(self, env_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 480))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (-150, 440)

        self.env_sprites = env_sprites

    def update(self):
        col_list = pygame.sprite.spritecollide(self, self.env_sprites, False)
        for sprite in col_list:
            sprite.remove(self.env_sprites)
