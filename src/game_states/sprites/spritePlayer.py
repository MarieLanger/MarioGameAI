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
        self.collideRect = self.CollideRect(34,34)
        self._updateCollideRectPositions()
        # https://stackoverflow.com/questions/28805271/pygame-rect-collision-smaller-than-image

        # Jumping
        self.velocityY = 0
        self.gravity = 0.5 #0.4


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

        # https://gamedev.stackexchange.com/questions/29617/how-to-make-a-character-jump


        self.rect.y += self.velocityY #* self.jumpCounter   # Apply horizontal velocity to X position
        self._updateCollideRectPositions()
        #self.applyGravity()
        # Adjust y-position, if necessary
        self.enforceNoVerticalClipping()




    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def checkCollisions_blocks(self,rect):
        """
        Checks for collisions between player and all sprites in the block-group
        :param rect
            None: Checks collision with original rect from player
            horizontal: Checks collision 1 pixel left/right from player
            vertical: Checks collision 1 pixel top/bottom from player
            whole: Checks collision 1 pixel on all sides
        :return A list with collided sprites
        """
        if rect is None:
            return pygame.sprite.spritecollide(self, self.blockGroup, False)
        elif rect == "horizontal":
            return pygame.sprite.spritecollide(self.collideRectH, self.blockGroup, False)
        elif rect == "vertical":
            return pygame.sprite.spritecollide(self.collideRectV, self.blockGroup, False)
        elif rect == "whole":
            return pygame.sprite.spritecollide(self.collideRect, self.blockGroup, False)
        else:
            print("The input rect =",rect, " is not valid!")


    # todo: maybe we don't need this
    def checkCollisionEdge(self, other_sprite, rect):
        """
        Checks on which side the player collides with another sprite
        :param other_sprite: other sprite that is overlapping
        :param rect
            None: Checks collision with original rect from player
            horizontal: Checks collision 1 pixel left/right from player
            vertical: Checks collision 1 pixel top/bottom from player
            whole: Checks collision 1 pixel on all sides
        :return: list of (topCol, bottomCol, leftCol, rightCol)
        """
        topCol = False
        bottomCol = False
        leftCol = False
        rightCol = False

        if rect is None:
            return pygame.sprite.spritecollide(self, self.blockGroup, False)
        elif rect == "horizontal":
            return pygame.sprite.spritecollide(self.collideRectH, self.blockGroup, False)
        elif rect == "vertical":
            return pygame.sprite.spritecollide(self.collideRectV, self.blockGroup, False)
        elif rect == "whole":
            return pygame.sprite.spritecollide(self.collideRect, self.blockGroup, False)
        else:
            print("The input rect =",rect, " is not valid!")

        return (topCol,bottomCol,leftCol,rightCol)



    def enforceNoVerticalClipping(self):
        """
        Idea: Gravity gets applied every iteration and the y-position gets updated every iteration.
        Problem here: The player might clip into the ground too much.
        What this method does: Checks if clipping occured and if yes, adjust the y-position so that player
                                stands on top of the ground.
        # todo: also update the collideRects for now, idk if we actually need them later???
        # todo: Probably also set the velocity in y direction to zero?
        Why it works: The rendering occurs after/at the end of update() So the clipping was never visible
        :return: No direct return, but updates the self.rect.y position
        """

        # todo: potentially inefficient because we check collisions twice?
        # todo: potentially bad coding because the x collisions get handled differently than the y-collisions
        """
        - Player inputs keys
        - Collisions were checked
        - Adjust x position correctly
        
        - Yolo it and apply y positions
        - Check if new position is valid and adjust, if necessary
        """
        col_list = self.checkCollisions_blocks(None)
        #print(col_list, self.rect.bottom)
        if len(col_list) == 0:
            return  # No clipping, wonderful, we can stop here
        else:
            for collided in col_list:
                # Check if the sprites even collide in both x and y, see ipad notes
                # I need it because there is a loop and I might iterate over multiple sprites
                # If i already fixed the problem with sprite 1, I don't need to adjust it again for sprite 2
                #Note: rect.right/left only give you x-positions and bottom/top only y-positions!
                x_col = not (self.rect.right < collided.rect.left or self.rect.left > collided.rect.right)
                y_col = not (self.rect.bottom < collided.rect.top or self.rect.top > collided.rect.bottom)
                if x_col and y_col:
                    # Place on top of sprite
                    self.rect.bottom = collided.rect.top #- 1
                    # It looks like hovering but actually each rectangle has a black part around it
                    self._updateCollideRectPositions()
                    self.velocityY = 0  # set y-velocity to zero so that the sprite stops jumping


    def _updateCollideRectPositions(self):
        self.collideRectH.rect.center = self.rect.center
        self.collideRectV.rect.center = self.rect.center
        self.collideRect.rect.center = self.rect.center

    def moveLeft(self, value=5):
        self.rect.x -= value
        self._updateCollideRectPositions()

    def moveRight(self, value=5):
        self.rect.x += value
        self._updateCollideRectPositions()

    def move_x(self, value):
        self.rect.x += value


    def jumpKeyPressed(self):
        self.velocityY = -15 #-4
        self.jumpCounter = 1

    def jumpKeyReleased(self):
        if self.velocityY < -5:
            self.velocityY = self.velocityY/2 +1

    def applyGravity(self):
        # terminal velocity
        if self.velocityY + self.gravity > 6:
            self.velocityY = 6
        else:
            self.velocityY += self.gravity



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
