import pygame
import sys
import os
import numpy as np

from .state import State
# from .stateTitle import StateTitle    no!!!! because we want to exit this state, not put another title on top of it!!
# otherwise circular dependency!!!!!!

from .sprites.spriteTest import SpriteTest  # YOU NEED A DOT BEFORE THE FOLDER NAME AAAAAAAAAAAAAAAAAAAAHHHHHHH
from .sprites.spriteBlock import SpriteBlock
from .sprites.spritePlayer import SpritePlayer


class StateGame(State):
    """
    State for when the game gets played
    """

    def __init__(self, game):
        self.game = game

        # Game related variables --------------------------------------------------------------

        # Position of left down corner within 1 tile. Goes from 0-15
        self.tilePos = 0

        self.levelMoving = True  # see below:
        """Necessary for movement:
        Necessary for movement at borders. 
        When Peach is close to a border or goes back, Peach moves and the sprites stay still.
        When Peach moves forward, the level moves and peach stays still.
        """

        self.borderCloseness = 0  # When peach goes left, measure how close she is to the border

        # Pygame only detects when keys got pressed or released, but not when they stay held -----
        # This is a workaround around this
        self.leftKeyHold = False
        self.rightKeyHold = False
        self.upKeyHold = False

        # Allows to temporarily block keys while not loosing the information that a key got pressed
        # Background: Previously i adjusted the attributes above and it did not allow to unblock keys
        #self.rightKeyBlock = False
        #self.leftKeyBlock = False

        # note down old states
        #self.leftKeyOldState = None
        #self.rightKeyOldState = None

        # Load level ---------------------------------------------------------------------------
        # levelMatrix: A guide which sprites to create
        # currentMatrix: Updates when e.g. enemy positions change too

        path = "\..\data\levels"
        filename = "\level1.txt"
        fullpath = os.getcwd() + path + filename
        self.levelMatrix = np.genfromtxt(fullpath, delimiter='\t')
        print("the shape of the level is:", self.levelMatrix.shape)

        # There can be maximally 13x25 tiles visible at 1 time (25 because 2 half tiles can be seen)
        # self.currentMatrix = self.levelMatrix[0:13, 0:25]

        # How far the level got reached, in tiles
        # Initialized by 25: maximally we see the 25th tiles in x-dimension
        # 24: 0-24 = 25 entries
        self.levelProgress = 23
        self.pixelProgress = 23*32

        # Create all the sprite objects -------------------------------------------------
        # Creating the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.player = None

        # Actually creating the first sprites at the start of the level + adding them into a group

        # The player sees 13x24 tiles at once
        for col in range(24):
            self._loadSpriteColumn(self.levelMatrix[:, col], col, 0)

        self.all_sprites.add(SpriteTest())  # todo: remove this line later

    def handleInputs(self):
        # Note down inputs --------------------------------------------
        # Necessary to have continued movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game.exitCurrentState()
                if event.key == pygame.K_RIGHT:
                    self.rightKeyHold = True
                if event.key == pygame.K_LEFT:
                    self.leftKeyHold = True
                if event.key == pygame.K_UP:
                    self.upKeyHold = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.rightKeyHold = False
                if event.key == pygame.K_LEFT:
                    self.leftKeyHold = False
                if event.key == pygame.K_UP:
                    self.upKeyHold = False
                    # todo: That line destroys every bit of structured code but it makes things also 1000x simpler oof
                    self.player.jumpKeyReleased()
        # From here: Use noted down inputs to change model!





        # HANDLE COLLISIONS WITH BLOCKS -----------------------------------------------------------------------------

        # Left/Right first
        # -----------------------------------------------------------------------------------------------------
        # Idea: Never touch self.rightKeyHold, but alter the input to _borderHandling
        keyinput_left = self.leftKeyHold
        keyinput_right = self.rightKeyHold

        # I always have to handle borders -------------------------------------------------------------------
        self._borderHandling(keyinput_left, keyinput_right)










        # todo -----------------------------------------------------------------------------------------------

        # todo: The following could probably be structured better and written in a cleaner way


        # YOU CAN ONLY JUMP IF YOU TOUCH THE GROUND ------------------------------------------------------
        # Calculate the collisions separately for horizontal/vertical collisions
        collisionListV = pygame.sprite.spritecollide(self.player.collideRectV, self.all_sprites, False)

        # Check the different sides where the player could collide with things
        topCol = False
        bottomCol = False

        for collidingSprite in collisionListV:
            topCol = collidingSprite.rect.collidepoint(self.player.collideRectV.rect.midtop) or \
                     collidingSprite.rect.collidepoint(self.player.collideRectV.rect.topleft) or \
                     collidingSprite.rect.collidepoint(self.player.collideRectV.rect.topright)
            bottomCol = collidingSprite.rect.collidepoint(self.player.collideRectV.rect.midbottom) or \
                        collidingSprite.rect.collidepoint(self.player.collideRectV.rect.bottomleft) or \
                        collidingSprite.rect.collidepoint(self.player.collideRectV.rect.bottomright)
            # https://stackoverflow.com/questions/20180594/pygame-collision-by-sides-of-sprite

        # todo: new idea: Let peach move whereever she wants and afterwards check if a collision occured with it
        # write that code after borderhandling

        # Handle bottom/top collisions
        if bottomCol:
            # I can only jump if I am standing on the ground
            # I am not a space rocket.
            if self.upKeyHold:
                self.player.jumpKeyPressed()
        else:
            # Newton says that I have to abide by the law of gravity if I am jumping
            self.player.applyGravity()
        # ------------------------------------------------------------------------------------------------------

        if topCol:
            pass
            # If I hit something on top I stop jumping
            # I am not a quantum particle tunnel through an energy barrier
            #self.player.jumpCounter = 0"""


        # todo ------------------------------------------------------------------------------------------------


        # todo: Collisions with enemies, coins, items, end flag -----------------------------------------------






        # WHEN INPUT ANALYZING IS FINISHED, UPDATE SPRITES ------------------------------------------------
        # Update all sprites
        self.all_sprites.update()



        self.playerSprites.update()






    def _checkCollisions(self):
        """
        Checks if after walking, peach clipped into something.
        If yes, adjust x-position of everything
        :return: 0: If nothing needs to be changed, -2 if position has to be adjusted by 2 to the left, etc
        """
        move = 0
        col_list = self.player.checkCollisions_blocks(None)
        # todo Assumption to be verified: Peach should not have any vertical collisions at this point??
        if len(col_list) == 0:
            return move # No clipping occured
        else:
            for collided in col_list:

                # Then player collided with right side
                if self.player.rect.left < collided.rect.left:
                    # If a collision happened
                    if self.player.rect.right > collided.rect.left:
                        # put to the left of it
                        if abs(collided.rect.left - self.player.rect.right) > abs(move):
                            move = collided.rect.left - self.player.rect.right

                # Else, player collided with left side
                else:
                    if self.player.rect.left < collided.rect.right:
                        # put to the left of it
                        if abs(collided.rect.right - self.player.rect.left) > abs(move):
                            move = self.player.rect.left - collided.rect.right

            # At the end, return the absolute biggest move
            return move


    def _borderHandling(self, leftinput, rightinput):
        """
        This method deals with the logic that when peach is near a border, the level should not move anymore.
        Most of the time, peach stays at 1 x-position and the level moves.
        However, when approaching a border, if the level moved too, then the game would show the part where
        no level exists = bad

        NEW: Updated, levelProgress and sprite loading
        """
        adjusted_pos = 0

        # If player is too close to the border, don't allow to move any further
        if self.borderCloseness > 59:
            leftinput = False



        # If the level moves + peach stays still
        if self.levelMoving:
            if rightinput:
                # For the right key, we move all sprites and if another tile gets touched, we load new things
                for sprite in self.all_sprites.sprites():
                    sprite.moveLeft()
                self.pixelProgress += 5
                adjusted_pos = self._checkCollisions()
                if adjusted_pos != 0:
                    for sprite in self.all_sprites.sprites():
                        sprite.move_x(-adjusted_pos)
                    self.pixelProgress += adjusted_pos

                self._evaluateTilePos()

            if leftinput:
                # As soon as I go left, the level should not move anymore (=peach now moves)
                # Hence, peach-moving state gets entered
                # Also, how close player is to the border gets calculated
                self.levelMoving = False
                self.borderCloseness += 5
                for sprite in self.playerSprites.sprites():
                    sprite.moveLeft()
                adjusted_pos = self._checkCollisions()
                if adjusted_pos != 0:
                    for sprite in self.all_sprites.sprites():
                        sprite.move_x(adjusted_pos)
                    self.borderCloseness += adjusted_pos

        # If peach is at the border, the level needs to stay + peach moves
        else:
            if rightinput:
                # If right key gets pressed, closeness to border gets smaller
                # If peach is at original closeness-position, peach now stays and sprites move again
                # Hence, states switch

                """
                Further problem here:
                If clip occured, then borderCloseness could be e.g. 4
                For this, peach needs to move 4 pixels
                And then it needs to switch to levelmoving
                AND the level needs to move 1 pixel too
                =5 pixels movement in total
                """

                # if big enough, verfahre wie normal
                if self.borderCloseness > 4:
                    self.borderCloseness -= 5
                    if self.borderCloseness == 0:
                        self.levelMoving = True
                    for sprite in self.playerSprites.sprites():
                        sprite.moveRight()
                    adjusted_pos = self._checkCollisions()
                    if adjusted_pos != 0:
                        for sprite in self.playerSprites.sprites():
                            sprite.move_x(adjusted_pos)   # todo: i flipped the sign and it worked??
                        self.borderCloseness += -adjusted_pos
                else: # else, a clip occured and do the above

                    # Move peach 4 pixels to the right
                    for sprite in self.playerSprites.sprites():
                        sprite.moveRight(self.borderCloseness)
                    # Check for collisions again
                    adjusted_pos = self._checkCollisions()
                    # If collisions, adjust position, if not, try to move whole level
                    if adjusted_pos != 0:
                        for sprite in self.playerSprites.sprites():
                            sprite.move_x(adjusted_pos)   # todo: i flipped the sign and it worked??
                        self.borderCloseness += -adjusted_pos
                    else:
                        # Move whole level and check for collisions again
                        for sprite in self.all_sprites.sprites():
                            sprite.moveLeft(5-self.borderCloseness)
                        self.pixelProgress += 5-self.borderCloseness
                        adjusted_pos = self._checkCollisions()
                        if adjusted_pos != 0:
                            for sprite in self.all_sprites.sprites():
                                sprite.move_x(-adjusted_pos)
                            self.pixelProgress += adjusted_pos

                        # Clean up
                        self.pixelProgress += 5-self.borderCloseness
                        self.levelMoving = True
                        self.borderCloseness = 0
                        self._evaluateTilePos()

            if leftinput:
                # Only allow left movement if peach is not too close to the let border
                # if self.borderCloseness < 25:
                # If the left key was pressed in this state, only the closeness to border increases
                self.borderCloseness += 5
                for sprite in self.playerSprites.sprites():
                    sprite.moveLeft()
                adjusted_pos = self._checkCollisions()
                if adjusted_pos != 0:
                    for sprite in self.playerSprites.sprites():
                        sprite.move_x(-adjusted_pos)
                    self.borderCloseness += adjusted_pos



    def _evaluateTilePos(self):
        # If another tile got touched


        if int(self.pixelProgress/32) > self.levelProgress:
            print("New level column loaded!", self.levelProgress)
            self.levelProgress += 1
            self._loadSpriteColumn(self.levelMatrix[:, self.levelProgress], 23, self.pixelProgress%32)

            # todo: delete 13 old sprites
            # todo: Idea: Have a 13-tiles high death zone at x-position -2 or something like that
            # (so not within the view
            # When sprites collide with that, remove the sprites from their respective group




    def _loadSpriteColumn(self, column, columnIndex, offset):
        """
        Creates new sprites for 1 new column.
        NEW: Operates with player position

        :param column: 1 column with values (=a 13x1 matrix)
        columnID: Index of column in level-matrix
        :return: No direct returns, but it appends sprites to spritegroups
        """
        for row in range(13):
            # If not 0, then a sprite has to be loaded
            if column[row] != 0:

                # Initialize reference for later
                new_sprite = None

                # CREAING THE SPRITE
                if column[row] == 1:  # If block
                    new_sprite = SpriteBlock(row * 16 * 2, columnIndex * 16 * 2 - offset)
                    self.all_sprites.add(new_sprite)
                if column[row] == 2:  # If player
                    #new_sprite = SpritePlayer(row * 16 * 2, columnIndex * 16 * 2, self.all_sprites)
                    # Column index (2nd input is fixed for player!
                    new_sprite = SpritePlayer(row * 16 * 2, 2 * 16 * 2, self.all_sprites)
                    self.playerSprites.add(new_sprite)
                    self.player = new_sprite
                    # self.all_sprites.add(self.player)




    def display(self, screen):
        screen.fill('black')

        self.all_sprites.draw(screen)
        self.playerSprites.draw(screen)

        # Update everything
        pygame.display.update()
