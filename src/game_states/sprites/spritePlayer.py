import pygame


class SpritePlayer(pygame.sprite.Sprite):
    """
    The player sprite which can be controlled by the user/AI.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - blockgroup: player has knowledge about the blocks around it (reference)
        - game: player needs to communicate with the game itself (reference)
    """

    def __init__(self, y_pos, x_pos, blockgroup, game):
        pygame.sprite.Sprite.__init__(self)

        # References
        self.blockGroup = blockgroup
        self.game = game

        # Draw the player
        self.image = pygame.Surface((16 * 2, 16 * 2))
        self.image.fill((255, 105, 180))
        self.rect = self.image.get_rect()  # self.image.get_rect() is =Rect(0,0,32,32)
        self.rect.topleft = (x_pos, y_pos)

        # Jumping variables
        self.velocityY = 0
        self.gravity = 0.5

        # Enemy interactions
        self.immunity = False
        self.immunityCounter = 0

        # Player has a state-stack where all the previous states after getting items are stored. Stack data structure.
        self.states = []
        self.states.append(PlayerStateNormal(self))


    def update(self):
        """
        What forces get applied to the player, independent of the user inputs.
        """

        # Apply horizontal velocity to X position and adjust y-position, if necessary
        self.rect.y += self.velocityY
        self.enforceNoVerticalClipping()

        # If player is currently immune, check for how long anymore
        if self.immunity:
            self.immunityCounter += 1
            if self.immunityCounter == 70:
                self.immunity = False
                self.immunityCounter = 0
                self.image.fill((255, 105, 180))

        # States need to be updated too (star removes itself after a while!)
        self.peekState().updateState()

    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """

    def checkCollisions_blocks(self):
        """
        Checks for collisions between player and all sprites in the block-group.
        :return A list with collided sprites
        """
        return pygame.sprite.spritecollide(self, self.blockGroup, False)

    def checkBottomTopTouches(self):
        """
        Checks if the player touches a block either on top or at the bottom (=if the sprite is 1 pixel away)
        :return: (topCol, bottomCol) --> both booleans
        """
        bottomCol = False
        topCol = False

        for sprite in self.blockGroup.sprites():
            # bottomleft --> (x,y)
            bottomCol = sprite.rect.collidepoint((self.rect.bottomleft[0], self.rect.bottomleft[1] + 1)) or \
                        sprite.rect.collidepoint((self.rect.midbottom[0], self.rect.midbottom[1] + 1)) or \
                        sprite.rect.collidepoint((self.rect.bottomright[0] - 1, self.rect.bottomright[1] +1 ))
                        # -1 got added so that the player doesn't stick to a right wall above 1-tile-wide holes
            if bottomCol:
                break

        for sprite in self.blockGroup.sprites():
            topCol = sprite.rect.collidepoint((self.rect.topleft[0], self.rect.topleft[1] + 1)) or \
                     sprite.rect.collidepoint((self.rect.topleft[0], self.rect.topleft[1] + 1)) or \
                     sprite.rect.collidepoint((self.rect.topleft[0], self.rect.topleft[1] + 1))
            if topCol:
                break
        #print("Bottom is touched:", bottomCol)
        return (topCol, bottomCol)

    def enforceNoVerticalClipping(self):
        """
        Idea: Gravity gets applied every iteration and the y-position gets updated every iteration.
        Problem here: The player might clip into the ground too much.
        What this method does: Checks if clipping occured and if yes, adjust the y-position so that player
                               stands on top of the ground.
        Why it works: The rendering occurs after/at the end of update(). So the clipping was never visible!
        :return: Method updates the self.rect.y position
        """

        col_list = self.checkCollisions_blocks()
        if len(col_list) != 0:
            for collided in col_list:
                # Check if the sprites even collide in both x and y (see ipad notes)
                # I need it because there is a loop and I might iterate over multiple sprites
                # If I already fixed the problem with sprite 1, I don't need to adjust it again for sprite 2
                x_col = not (self.rect.right < collided.rect.left or self.rect.left > collided.rect.right)
                y_col = not (self.rect.bottom < collided.rect.top or self.rect.top > collided.rect.bottom)
                if x_col and y_col:
                    # collision on top
                    if self.rect.top <= collided.rect.bottom and self.rect.top >= collided.rect.top:
                        self.rect.top = collided.rect.bottom  # +1
                        self.velocityY = 0
                    # collision at the bottom
                    if self.rect.bottom >= collided.rect.top and self.rect.bottom <= collided.rect.bottom:
                        # Place on top of sprite
                        self.rect.bottom = collided.rect.top  # - 1
                        self.velocityY = 0  # set y-velocity to zero so that the sprite stops jumping

    def applyGravity(self):
        """
        Updates Y-velocity according to gravity. The terminal velocity is 6.
        """
        self.velocityY = min(6, self.velocityY + self.gravity)
        """if self.velocityY + self.gravity > 6:
            self.velocityY = 6
        else:
            self.velocityY += self.gravity"""

    def moveLeft(self, value=5):
        self.rect.x -= value

    def moveRight(self, value=5):
        self.rect.x += value

    def move_x(self, value):
        self.rect.x += value

    def jumpKeyPressed(self):
        """
        Sets the Y-velocity to a value after the key for jumping got pressed.
        Jumping is only allowed if peach stands still (=has Y-velocity 0 at the moment)
        """
        if self.velocityY == 0:
            self.velocityY = -13 #-11

    def jumpKeyReleased(self):
        """
        The jump height is dependent on how long the key has been pressed.
        """
        if self.velocityY < -3 : #-5:
            self.velocityY = self.velocityY / 2 + 1

    def enemyHit(self):
        """
        Enemies delegate how to handle a direct collision to the player.
        The player then delegates this call further to its top state.
        These either gets hit (=True) or hits back (=False)
        """
        # Check top state and delegate call
        top_state = self.peekState()
        player_hit = top_state.handleEnemyCollision()  # here the pop state happens + other states make immune

        # Player can only get hit when player is not immune
        if not self.immunity:
            if player_hit:
                # Depending on state, either remove it or game over
                if len(self.states) == 1:
                    self.game.setLevelOutcome(-1)
                elif len(self.states) > 1:
                    self.removeState(True)
        return player_hit  # True if player got hit, False if player "hits back" via star

    def addState(self, state):
        """
        Adds an item state according to stack data structure.
        """
        self.states.append(state)

    def removeState(self, immunityreset):
        """
        Removes a state according to stack-data structure.
        :param immunityreset: If set to false, immunity does not get set when state gets removed.
                              This is sometimes necessary, e.g. to handle the removal of the star-state.
        """
        self.immunity = immunityreset

        self.peekState().removeAppearance()
        if immunityreset:
            self.image.fill((255, 216, 240))
        # self.states.pop()

    def peekState(self):
        """
        Returns the top state according to stack data structure.
        """
        return self.states[-1]

    def getAllStates(self):
        return self.states




class PlayerState():
    """
    The base class for the states that hold the different states of Peach:
    - Normal tiny
    - Bigger
    - Star
    """

    def __init__(self, player):
        """
        Each state has:
        - A rect
        - A reference to player
        """
        self.player = player

        self.stateID = -1

    def handleEnemyCollision(self):
        """
        Either lowers state (return: True) or kills enemy (return: False)
        """
        pass

    def handleItemCollision(self, itemtype):
        """
        If the item is lower or equal to current state, do nothing, otherwise, add state.
        """
        pass

    def changeAppearance(self):
        """
        Change the appearance of the player sprite when entering state.
        """
        pass

    def removeAppearance(self):
        """
        Removing the changed appearance when state got exited.
        """
        pass

    def updateState(self):
        """
        Some states need to update their internal model. (star)
        """
        pass

    def getID(self):
        return self.stateID


class PlayerStateNormal(PlayerState):
    """
    Class that holds the normal state of Peach
    """

    def __init__(self, player):
        PlayerState.__init__(self, player)

        # width, height
        self.size = [16 * 2, 16 * 2]
        self.color = (255, 105, 180)

        self.stateID = 0

    def handleEnemyCollision(self):
        return True  # Game over

    def handleItemCollision(self, itemtype):
        if itemtype == "mushroom":
            newstate = PlayerStateMushroom(self.player)
            self.player.addState(newstate)
            newstate.changeAppearance()
        elif itemtype == "star":
            newstate = PlayerStateStar(self.player)
            self.player.addState(newstate)
            newstate.changeAppearance()



class PlayerStateMushroom(PlayerState):
    """
    Class that holds the bigger state of Peach. See mushroom item documentation (spriteMushroom.py)
    """

    def __init__(self, player):
        PlayerState.__init__(self, player)
        # width, height
        self.size = [16 * 2, 32 * 2]
        self.color = (255, 105, 180)

        self.stateID = 1

    def handleEnemyCollision(self):
        return True

    def handleItemCollision(self, itemtype):
        if itemtype == "star":
            newstate = PlayerStateStar(self.player)
            self.player.addState(newstate)
            newstate.changeAppearance()

    def changeAppearance(self):
        tmp = self.player.rect.bottomleft
        self.player.image = pygame.Surface(self.player.peekState().size)
        self.player.image.fill((255, 105, 180))
        self.player.rect = self.player.image.get_rect()  # self.image.get_rect() is =Rect(0,0,32,32)
        self.player.rect.bottomleft = tmp

    def removeAppearance(self):
        tmp = self.player.rect.bottomleft
        self.player.states.pop()
        self.player.image = pygame.Surface(self.player.peekState().size)
        self.player.rect = self.player.image.get_rect()
        self.player.rect.bottomleft = tmp

    def updateState(self):
        pass


class PlayerStateStar(PlayerState):
    """
    Class that holds the bigger state of Peach
    """

    def __init__(self, player):
        PlayerState.__init__(self, player)

        # width, height
        self.size = [16 * 2, 32 * 2]
        self.color = (255, 105, 180)

        # counter
        self.counter = 0

        self.stateID = 2

    def handleEnemyCollision(self):
        return False

    def handleItemCollision(self, itemtype):
        if itemtype == "mushroom":
            # Mushroom should get applied before star
            newstate = PlayerStateMushroom(self.player)
            self.player.addState(newstate)
            newstate.changeAppearance()

            self.player.addState(self)
            self.changeAppearance()

    def changeAppearance(self):
        self.player.image.fill((127, 81, 246))

    def removeAppearance(self):
        self.player.image.fill((255, 105, 180))

    def updateState(self):
        self.counter += 1
        if self.counter > 100:
            self.player.removeState(False)
            self.player.states.pop()


