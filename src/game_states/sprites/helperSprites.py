import pygame

class HelperSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        pass


class SpriteButton(HelperSprite):
    """
    Renders buttons onto the screen and they turn red when pressed.
    """
    def __init__(self, x, y):
        HelperSprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill((155, 155, 155))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        self.active = False
        self.image.fill((55, 55, 55))

    def update(self):
        pass

    def checkInputs(self, activeButton):
        if activeButton:
            if activeButton != self.active:
                self.active = not self.active
                self.image.fill((155, 155, 155))
        else:
            if activeButton != self.active:
                self.active = not self.active
                self.image.fill((55, 55, 55))





class FallingHelperSprite(HelperSprite):
    """
    Detects when player falls down a hole and communicates game over.
    """

    def __init__(self, player, game):
        HelperSprite.__init__(self)
        self.image = pygame.Surface((320 * 2, 60))
        #self.image.fill((255, 105, 180))
        #self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 420)

        self.player = player
        self.game = game

    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.game.setLevelOutcome(-1)


class KillEnvironmentHelperSprite(HelperSprite):
    """
    Kills sprites after they move outside of the screen to the left.
    Killing off sprites leads to less collision-comparisons.
    """

    def __init__(self, env_sprites):
        HelperSprite.__init__(self)
        self.image = pygame.Surface((32, 480))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (-150, 440)

        self.env_sprites = env_sprites

    def update(self):
        col_list = pygame.sprite.spritecollide(self, self.env_sprites, False)
        for sprite in col_list:
            for group in sprite.groups():
                sprite.remove(group)
