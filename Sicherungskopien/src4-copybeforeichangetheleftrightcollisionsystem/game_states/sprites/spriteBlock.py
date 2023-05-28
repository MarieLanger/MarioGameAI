import pygame

class SpriteBlock(pygame.sprite.Sprite):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic block sprite that does nothing
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, y_pos, x_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((16*2,16*2))
        self.image.fill((118,134,146))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos,y_pos)



    def update(self):
        """
        What sprites do on their own, independent of player inputs
        """
        pass


    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def moveLeft(self, value=5):
        self.rect.x -= value

    def moveRight(self, value=5):
        self.rect.x += value