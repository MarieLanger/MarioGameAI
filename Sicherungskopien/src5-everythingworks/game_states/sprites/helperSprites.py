import pygame

class GameOverSprite(pygame.sprite.Sprite):
    """
    Detects it when player falls down a hole
    """
    def __init__(self, player, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((320*2,20))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0,440)

        self.player = player
        self.game = game


    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.game.setLevelOutcome(-1)



class KillEnvironmentSpritesSprite(pygame.sprite.Sprite):
    """
    All sprites inherit from this sprite
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, env_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((6,480))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (-40,440)

        self.env_sprites = env_sprites


    def update(self):
        col_list = pygame.sprite.spritecollide(self, self.env_sprites, False)
        for sprite in col_list:
            sprite.kill()