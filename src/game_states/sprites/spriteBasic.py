import pygame


class SpriteBasic(pygame.sprite.Sprite):
    """
    All sprites inherit from this class.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """

    def __init__(self, y_pos, x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16 * 2, 16 * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)

        self.normX = 0
        self.normY = 0



    def update(self):
        """
        What sprites do on their own, independent of player inputs.
        """
        pass

    def writeState(self, matrix, playerX, playerY):
        """
        Checking if own position is inside the matrix and if yes, write to the corresponding one
        :param matrix:
        :param playerX:
        :param playerY:
        :return:

        MATRICES -----------------------------------------------
        Blocks: matrix[y,x,0] = +1
        Enemies: matrix[y,x,0] = -1
        Coins/Containers: matrix[y,x,1] = -1
        Items/Containers/End flag: matrix[y,x,1] = +1

        IMPLEMENTATIONS ----------------------------------------
        Basic implementation in:
        - Blocks
        - Enemies
        - Coins
        - Items

        Implementation with additional content-variable (+1 or -1) in:
        - Container

        Implementation that takes height into account in:
        - End flag
        - Pipe
        - Koopa
        """
        pass




    def _withinStateMatrix(self, playerX, playerY, x, y):
        """
        Checks whether the current tile is inside the matrix-boundaries
        :param playerX:
        :param playerY:
        :param x:
        :param y:
        :return:
        """
        # left x, right x, up y, down y
        within = (x >= playerX-2*32) and (x < playerX+8*32) and (y >= playerY-6*32) and (y < playerY + 2*32)
        self.normX = -2*32
        self.normY = -6*32

        #within = (x >= playerX-1*32) and (x < playerX+5*32) and (y >= playerY-7*32) and (y < playerY + 5*32)
        #self.normX = -1*32
        #self.normY = -7*32



        return within

    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def moveLeft(self, value=5):
        self.rect.x -= value

    def moveRight(self, value=5):
        self.rect.x += value

    def move_x(self, value):
        self.rect.x += value
