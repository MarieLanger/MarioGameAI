import pygame


class SpritePlayer(pygame.sprite.Sprite):
    """
    All sprites inherit from pygame.sprite.Sprite.
    The player
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - blockgroup: player has knowledge about the blocks around it
    """

    def __init__(self, y_pos, x_pos, blockgroup, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.image = pygame.Surface((16 * 2, 16 * 2))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()  # self.image.get_rect() is =Rect(0,0,32,32)
        self.rect.topleft = (x_pos, y_pos)

        # Idea for this: Have 1 rect for left/right collisions and 1 rect for top/down collisions
        # 2 rects are needed because when standing on the ground, one 34x34 rect cannot
        # differentiate whether or not the bottomright collision is from the bottom or the right side
        # 2 rects are like a cross!
        self.collideRectV = self.CollideRect(32, 34)
        self._updateCollideRectPositions()
        # https://stackoverflow.com/questions/28805271/pygame-rect-collision-smaller-than-image

        # Jumping
        self.velocityY = 0
        self.gravity = 0.5 #0.4

        # Enemy interactions
        self.immunity = False
        self.immunityCounter = 0

        # Player states after getting items
        self.states = []
        self.states.append(PlayerStateNormal(self))


        # todo: Do I need this?
        self.blockGroup = blockgroup
        self.itemsGroup = None
        self.otherGroup = None





    def update(self):
        """
        What sprites do on their own, independent of player inputs
        """

        # https://gamedev.stackexchange.com/questions/29617/how-to-make-a-character-jump


        self.rect.y += self.velocityY #  # Apply horizontal velocity to X position
        self._updateCollideRectPositions()
        #self.applyGravity()
        # Adjust y-position, if necessary
        self.enforceNoVerticalClipping()


        if self.immunity:
            self.immunityCounter += 1
            if self.immunityCounter == 70:
                self.immunity = False
                self.immunityCounter = 0
                self.image.fill((255, 105, 180))




    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def checkCollisions_blocks(self):
        """
        Checks for collisions between player and all sprites in the block-group
        :return A list with collided sprites
        """
        return pygame.sprite.spritecollide(self, self.blockGroup, False)

    def checkBottomTopTouches(self):
        """
        Checks if the player touches a block either on top or at the bottom (=if the sprite is 1 pixel away)
        :return: (topCol, bottomCol) --> both booleans
        """
        collisionListV = pygame.sprite.spritecollide(self.collideRectV, self.blockGroup, False)

        # Check the different sides where the player could collide with things
        topCol = False
        bottomCol = False

        for collidingSprite in collisionListV:
            topCol = collidingSprite.rect.collidepoint(self.collideRectV.rect.midtop) or \
                     collidingSprite.rect.collidepoint(self.collideRectV.rect.topleft) or \
                     collidingSprite.rect.collidepoint(self.collideRectV.rect.topright)
            bottomCol = collidingSprite.rect.collidepoint(self.collideRectV.rect.midbottom) or \
                        collidingSprite.rect.collidepoint(self.collideRectV.rect.bottomleft) or \
                        collidingSprite.rect.collidepoint(self.collideRectV.rect.bottomright)
            # https://stackoverflow.com/questions/20180594/pygame-collision-by-sides-of-sprite

        return (topCol, bottomCol)


    def enforceNoVerticalClipping(self):
        """
        Idea: Gravity gets applied every iteration and the y-position gets updated every iteration.
        Problem here: The player might clip into the ground too much.
        What this method does: Checks if clipping occured and if yes, adjust the y-position so that player
                                stands on top of the ground.
        # todo: also update the collideRects for now, idk if we actually need them later???
        Why it works: The rendering occurs after/at the end of update() So the clipping was never visible
        :return: No direct return, but updates the self.rect.y position
        """

        # todo: potentially inefficient because we check collisions twice?
        """
        - Player inputs keys
        - Collisions were checked
        - Adjust x position correctly
        
        - Yolo it and apply y positions
        - Check if new position is valid and adjust, if necessary
        """


        col_list = self.checkCollisions_blocks()
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

                    # collision on top
                    if self.rect.top <= collided.rect.bottom and self.rect.top >= collided.rect.top:
                        self.rect.top = collided.rect.bottom #+1
                        self._updateCollideRectPositions()
                        self.velocityY = 0

                    # collision at the bottom
                    if self.rect.bottom >= collided.rect.top and self.rect.bottom <= collided.rect.bottom:
                        # Place on top of sprite
                        self.rect.bottom = collided.rect.top #- 1
                        # It looks like hovering but actually each rectangle has a black part around it
                        self._updateCollideRectPositions()
                        self.velocityY = 0  # set y-velocity to zero so that the sprite stops jumping





    def _updateCollideRectPositions(self):
        self.collideRectV.rect.center = self.rect.center

    def moveLeft(self, value=5):
        self.rect.x -= value
        self._updateCollideRectPositions()

    def moveRight(self, value=5):
        self.rect.x += value
        self._updateCollideRectPositions()

    def move_x(self, value):
        self.rect.x += value


    def jumpKeyPressed(self):
        # If peach is in the air, the velocity is either <0 (=jumping up)
        # or >0 (=jumping down)
        # When this is the case, peach shouldnt be able to jump too
        if self.velocityY == 0:
            self.velocityY = -11 #-4

    def jumpKeyReleased(self):
        if self.velocityY < -5:
            self.velocityY = self.velocityY/2 +1

    def applyGravity(self):
        # terminal velocity
        if self.velocityY + self.gravity > 6:
            self.velocityY = 6
        else:
            self.velocityY += self.gravity


    def enemyHit(self):
        # todo: The player should have some immunity after getting hit by an enemy
        # Whenever collision,
        self.immunity = True
        self.image.fill((255, 216, 240))

        top_state = self.peekState()
        tmp = top_state.handleEnemyCollision()
        if len(self.states) == 1:
            self.game.setLevelOutcome(-1)



    def addState(self,state):
        self.states.append(state)
        # Then you go from small to big
        if len(self.states) == 2:
            tmp = self.rect.bottomleft
            self.image = pygame.Surface(self.peekState().size)
            self.rect = self.image.get_rect()  # self.image.get_rect() is =Rect(0,0,32,32)
            self.rect.bottomleft = tmp

    def removeState(self):
        if len(self.states) == 2:
            tmp = self.rect.bottomleft
            self.states.pop()
            self.image = pygame.Surface(self.peekState().size)
            self.rect = self.image.get_rect()  # self.image.get_rect() is =Rect(0,0,32,32)
            self.rect.bottomleft = tmp
        elif len(self.states)==1:
            # return something
            pass
        else:
            self.states.pop()




    def peekState(self):
        return self.states[-1]



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


class PlayerState():
    """
    Class that holds the different states of Peach:
    - Normal tiny
    - Bigger
    - Star
    - Fireflower
    """
    def __init__(self):
        """
        Each state has:
        - A rect
        - A vertical collideRect
        - Alternatively, whenever a new state gets entered, update rect from Player-Class
        - todo later: A different sprite
        """
        pass

    def handleEnemyCollision(self):
        """
        - Lower state
        - Kill enemy
        :return:
        """
        pass

    def handleItemCollision(self):
        """
        If the item is lower or equal to current state, do nothing, otherwise, add state
        :return:
        """
        pass

    def spaceKeyPressed(self):
        """
        FireMario should be able to create a flame, the other ones don't
        :return:
        """
        pass

class PlayerStateNormal():
    """
    Class that holds the normal state of Peach
    """
    def __init__(self, player):

        # width, height
        self.size = [16 * 2, 16 * 2]
        self.color = (255, 105, 180)

        # reference
        self.player = player

    def handleEnemyCollision(self):
        # Game over
        pass

    def handleItemCollision(self, itemtype):
        """
        If the item is lower or equal to current state, do nothing, otherwise, add state
        :return:
        """
        if itemtype == "mushroom":
            self.player.addState(PlayerStateBig(self.player))
        elif itemtype == "fireflower":
            self.player.addState(PlayerStateBig(self.player))
            self.player.addState(PlayerStateFireFlower(self.player))
        elif itemtype == "star":
            self.player.addState(PlayerStateBig(self.player))
            self.player.add(PlayerStateStar(self.player))

    def spaceKeyPressed(self):
        """
        FireMario should be able to create a flame, the other ones don't
        :return:
        """
        pass


class PlayerStateBig():
    """
    Class that holds the bigger state of Peach
    """
    def __init__(self, player):

        # width, height
        self.size = [16 * 2, 32 * 2]
        self.color = (255, 105, 180)

        # reference
        self.player = player

    def handleEnemyCollision(self):
        self.player.removeState()
        return True  # yes, player got hit

    def handleItemCollision(self, itemtype):
        """
        If the item is lower or equal to current state, do nothing, otherwise, add state
        :return:
        """
        if itemtype == "fireflower":
            self.player.addState(PlayerStateFireFlower(self.player))
        elif itemtype == "star":
            self.player.add(PlayerStateStar(self.player))

    def spaceKeyPressed(self):
        """
        FireMario should be able to create a flame, the other ones don't
        :return:
        """
        pass


class PlayerStateStar():
    """
    Class that holds the bigger state of Peach
    """
    def __init__(self, player):

        # width, height
        self.size = [16 * 2, 32 * 2]
        self.color = (255, 105, 180)

        # reference
        self.player = player

    def handleEnemyCollision(self):
        self.player.removeState()
        return False  # no, enemy should get hit instead

    def handleItemCollision(self, itemtype):
        """
        If the item is lower or equal to current state, do nothing, otherwise, add state
        :return:
        """
        pass

    def spaceKeyPressed(self):
        """
        FireMario should be able to create a flame, the other ones don't
        :return:
        """
        pass

class PlayerStateFireFlower():
    """
    Class that holds the bigger state of Peach
    """
    def __init__(self, player):

        # width, height
        self.size = [16 * 2, 32 * 2]
        self.color = (255, 105, 180)

        # reference
        self.player = player

    def handleEnemyCollision(self):
        self.player.removeState()
        return True  # yes, player got hit

    def handleItemCollision(self, itemtype):
        """
        If the item is lower or equal to current state, do nothing, otherwise, add state
        :return:
        """
        if itemtype == "star":
            self.player.add(PlayerStateStar(self.player))

    def spaceKeyPressed(self):
        """
        FireMario should be able to create a flame, the other ones don't
        :return:
        """
        pass
