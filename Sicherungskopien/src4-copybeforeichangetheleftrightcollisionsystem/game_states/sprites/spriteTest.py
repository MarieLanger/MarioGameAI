import pygame

class SpriteTest(pygame.sprite.Sprite):
    """
    All sprites inherit from pygame.sprite.Sprite.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # starting positions
        self.x_pos = 400
        self.y_pos = 200

        self.image = pygame.Surface((50,50))
        self.image.fill((50,200,40))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos,self.y_pos)




    def update(self):
        """
        Sprites have to overwrite this method.
        """
        self.rect.x += 1


    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def moveLeft(self):
        self.rect.x -= 2

    def moveRight(self):
        self.rect.x += 2