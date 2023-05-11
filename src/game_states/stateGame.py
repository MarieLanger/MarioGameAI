import pygame
import sys
import os
import numpy as np

from .state import State
#from .stateTitle import StateTitle    no!!!! because we want to exit this state, not put another title on top of it!!
#otherwise circular dependency!!!!!!

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

        self.levelMoving = True  #see below:
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


        # Load level ---------------------------------------------------------------------------
        # levelMatrix: A guide which sprites to create
        # currentMatrix: Updates when e.g. enemy positions change too

        path = "\..\data\levels"
        filename = "\level1.txt"
        fullpath = os.getcwd() + path + filename
        self.levelMatrix = np.genfromtxt(fullpath, delimiter='\t')
        #print(self.levelMatrix)
        print("the shape of the level is:", self.levelMatrix.shape)

        # There can be maximally 13x25 tiles visible at 1 time (25 because 2 half tiles can be seen)
        #self.currentMatrix = self.levelMatrix[0:13, 0:25]


        # How far the level got reached, in tiles
        # Initialized by 25: maximally we see the 25th tiles in x-dimension
        # 24: 0-24 = 25 entries
        self.levelProgress = 24


        # Create all the sprite objects -------------------------------------------------
        # Creating the sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()

        # Actually creating the first sprites at the start of the level + adding them into a group

        # The player sees 13x24 tiles at once
        for col in range(24):
            self._loadSpriteColumn(self.levelMatrix[:,col],col)

        self.all_sprites.add(SpriteTest())   #todo: remove this line later





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


        # Use noted down inputs to change model --------------------------------------
        self._borderHandling()


        # WHEN INPUT ANALYZING IS FINISHED, UPDATE SPRITES ------------------------------------------------
        # Update all sprites
        self.all_sprites.update()
        self.playerSprites.update()






    def _evaluateTilePos(self):
        #If another tile got touched
        if self.tilePos==16:
            # Reset tile position
            self.tilePos=0

            #create between 0 and 13 new sprites
            # The 23 means "create it at column 23 on the screen"
            self._loadSpriteColumn(self.levelMatrix[:,self.levelProgress],23)


            # Increase the level progress
            self.levelProgress += 1

            #todo: delete 13 old sprites


    def _borderHandling(self):
        """
        This method deals with the logic that when peach is near a border, the level should not move anymore.
        Most of the time, peach stays at 1 x-position and the level moves.
        However, when approaching a border, if the level moved too, then the game would show the part where
        no level exists = bad
        """

        # If the level moves + peach stays still
        if self.levelMoving:
            if self.rightKeyHold:
                # For the right key, we move all sprites and if another tile gets touched, we load new things
                self.tilePos += 1
                for sprite in self.all_sprites.sprites():
                    sprite.moveLeft()
                self._evaluateTilePos()

            if self.leftKeyHold:
                # As soon as I go left, the level should not move anymore (=peach now moves)
                # Hence, peach-moving state gets entered
                # Also, how close player is to the border gets calculated
                self.tilePos -= 1
                self.levelMoving = False
                self.borderCloseness += 1
                for sprite in self.playerSprites.sprites():
                    sprite.moveLeft()

        # If peach is at the border, the level needs to stay + peach moves
        else:
            if self.rightKeyHold:
                # If right key gets pressed, closeness to border gets smaller
                # If peach is at original closeness-position, peach now stays and sprites move again
                # Hence, states switch
                self.tilePos += 1
                self.borderCloseness -= 1
                if self.borderCloseness==0:
                    self.levelMoving = True
                for sprite in self.playerSprites.sprites():
                    sprite.moveRight()
            if self.leftKeyHold:
                # If the left key was pressed in this state, only the closeness to border increases
                self.tilePos -= 1
                self.borderCloseness += 1
                for sprite in self.playerSprites.sprites():
                    sprite.moveLeft()


    def _loadSpriteColumn(self, column,columnIndex):
        """
        Creates new sprites for 1 new column.

        :param column: 1 column with values (=a 13x1 matrix)
        columnID: Index of column in level-matrix
        :return: No direct returns, but it appends sprites to spritegroups
        """
        for row in range(13):
            #print("currently in y:",row,"  and x:",col)

            # If not 0, then a sprite has to be loaded
            if column[row] != 0:

                # Initialize reference for later
                new_sprite = None

                # CREAING THE SPRITE
                if column[row] == 1:  # If block
                    new_sprite = SpriteBlock(row*16*2,columnIndex*16*2)
                    self.all_sprites.add(new_sprite)
                if column[row] == 2:  # If player
                    print("added player")
                    new_sprite = SpritePlayer(row*16*2,columnIndex*16*2)
                    self.playerSprites.add(new_sprite)
                    #self.all_sprites.add(self.player)









    def display(self, screen):
        screen.fill('black')

        self.all_sprites.draw(screen)
        self.playerSprites.draw(screen)

        #Update everything
        pygame.display.update()


