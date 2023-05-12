import pygame


class SpritePlayer(pygame.sprite.Sprite):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic block sprite that does nothing
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """

    def __init__(self, y_pos, x_pos, blockgroup):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((16 * 2, 16 * 2))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()  # self.image.get_rect() is =Rect(0,0,32,32)
        self.rect.topleft = (x_pos, y_pos)

        # Idea for this: Have 1 rect for left/right collisions and 1 rect for top/down collisions
        # 2 rects are needed because when standing on the ground, one 34x34 rect cannot
        # differentiate whether or not the bottomright collision is from the bottom or the right side
        # 2 rects are like a cross!
        self.collideRectV = self.CollideRect(32, 34)
        self.collideRectH = self.CollideRect(34, 32)
        self.collideRectH.rect.center = self.rect.center
        self.collideRectV.rect.center = self.rect.center
        # https://stackoverflow.com/questions/28805271/pygame-rect-collision-smaller-than-image

        # Only allow to jump for a certain number of frames
        self.jumpCounter = 0

        # todo: Do I need this?
        # player needs to have a rect that's 1 pixel bigger than itself
        self.collideRect = pygame.Rect(0, 0, 34, 34)
        self.collideRect.center = self.rect.center

        # todo: Do I need this?
        self.blockGroup = blockgroup
        self.enemiesGroup = None
        self.itemsGroup = None
        self.coinsGroup = None
        self.otherGroup = None

    def update(self):
        """
        What sprites do on their own, independent of player inputs
        """

        if self.jumpCounter > 0:
            self.jump()
            # After 20 frames, stop jumping
            if self.jumpCounter == 20:
                self.jumpCounter = 0

    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def moveLeft(self):
        self.rect.x -= 2
        self.collideRectH.rect.x -= 2
        self.collideRectV.rect.x -= 2

    def moveRight(self):
        self.rect.x += 2
        self.collideRectH.rect.x += 2
        self.collideRectV.rect.x += 2

    def jump(self):
        self.rect.y -= 4
        self.collideRectH.rect.y -= 4
        self.collideRectV.rect.y -= 4
        self.jumpCounter += 1

    def applyGravity(self):
        # If not in the middle of a jump
        if self.jumpCounter == 0:
            self.rect.y += 4
            self.collideRectH.rect.y += 4
            self.collideRectV.rect.y += 4

    class CollideRect(pygame.sprite.Sprite):
        """
        Helper class to detect when the player sprite is directly next to another sprite.
        Workaround for:
        - Pygame can only detect collisions and not when sprites are next to each other
        - Pygame needs a sprite object to detect collisions and only creating a Rect-object is not sufficient

        Idea: Player class contains 2 of these helper classes and all of the collisions are handled by it!
        """

        def __init__(self, width, height):
            self.rect = pygame.Rect(0, 0, width, height)
