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



        # Pygame only detects when keys got pressed or released, but not when they stay held
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
        #self.currentMatrix = np.chararray((13, 25))

        #13:y, 25:x, 3:z
        # Idea about z-dimension: With 1 fixed (y,x), there can be up to 3 sprites in 1 tile.
        # If currentMatrix[2,6]=[24,4,0]    then that means that at (y,x)=(2,6) there
        # are 2 sprites in that tile: one with id=24 and one with id=4
        # todo: current limitation: There can only be 3 different sprites in 1 tile!
        self.currentMatrix = np.zeros((13,25,3))
        """
        b = np.zeros((5,10,2))

        b[0,0,0] = 1
        b[1,2,0] = 2
        b[1,2,1] = 3
        """

        # Sprite IDs are an integer number. The first ID is 1, the second ID 2,....
        self.currentSpriteID = 0

        # Dictionary where:    keys: spriteID    values: reference to sprite
        self.spriteDict = {}

        # How far the level got reached, in tiles
        # Initialized by 25: maximally we see the 25th tiles in x-dimension
        # 24: 0-24 = 25 entries
        self.levelProgress = 24


        # Create all the sprite objects -------------------------------------------------
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(SpriteTest())   #todo: remove this line later
        self.playerSprites = pygame.sprite.Group()

        # The player sees 13x24 tiles at once
        for col in range(24):

            self._loadSpriteColumn(self.levelMatrix[:,col],col)





    def _generateNewKey(self):
        """
        Increases currentKeyNumber by 1 and returns the actual key.
        :return:
        """
        self.currentSpriteID += 1
        return self.currentSpriteID



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


        # Use noted down inputs to change model ------------------------------------
        self._borderHandling()


        # WHEN INPUT ANALYZING IS FINISHED, UPDATE SPRITES ------------------------------------------------
        # Update all sprites
        self.all_sprites.update()
        self.playerSprites.update()




    def getSpriteListAtPosition(self,key,position):
        """
        A sprite with a certain key wants to ask which other sprites are at a certain location relative from itself.
        :param key:
        :param position:
        :return: A list with the references
        """

        # Find key in matrix
        index = np.where(self.currentMatrix == key)

        # Requested position is obtained by adding the position-entries to the own indexes
        requested_position = self.currentMatrix[index[0]+position[0],index[1]+position[1]]

        # Iterate through the 3 entries:
        found_keys = []
        for i in range(3):
            if requested_position[i] != 0:  #if zero, then there is no sprite
                reference = self.spriteDict[requested_position[i]]
                found_keys.append(reference)

        return found_keys


    def moveSprite(self,key,position):
        """
        Moves a sprite within currentMatrix relative to its current position.
        Example:
            - Sprite has a certain key K and via spriteDict we see that it's at (y,x)=(3,4) in currentMatrix
            - Input: position=(2,-1)
            - New position of sprite is then at (3+2,4-1)=(5,3)
        Idea: Sprite does not need to know where it currently is in matrix, it just needs to tell the game
              How far it wants to move!

        :param key: Key-identifier of the sprite
        :param position: How much it wants to move, relative to current position! Not an absolute value!!
        :return: No return value, but self.currentMatrix gets adjusted
        """

        # Assumption: When I search for a key in the matrix, the key is only there once and the key is present!

        # Find key in matrix
        index = np.where(self.currentMatrix == key)

        # Remove key from its current position in matrix
        self.currentMatrix[index[0],index[1],index[2]] = 0


        # Put key to new position
        # First, find out where there are zeros
        zero_index = np.where(self.currentMatrix[index[0]+position[0],index[1]+position[1]] == 0)

        if len(index[0] == 0):  # If there are no zeroes in that position
            print("Warning, more than 3 sprites in 1 tile! Cannot add another one")
        else:
            self.currentMatrix[index[0]+position[0],index[1]+position[1],zero_index[0][0]] = key






    def _evaluateTilePos(self):
        #If another tile got touched
        if self.tilePos==16:
            # Reset tile position
            self.tilePos=0

            #todo: update self.currentMatrix
            # Increase the level progress


            # shuffle matrix
            print(self.currentMatrix)

            # Shift all entries of matrix 1 position to the left
            self.currentMatrix = np.roll(self.currentMatrix, -1, axis=1)

            #load new entries
            self.currentMatrix[:,-1] = self.levelMatrix[:,self.levelProgress]

            #create sprites
            self._loadSpriteColumn(self.levelMatrix[:,self.levelProgress],23)





            self.levelProgress += 1
            print(self.currentMatrix)



            #todo: load 13 new sprites
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

                # Generate the key and add it to currentMatrix
                new_key = self._generateNewKey()
                #self.currentMatrix[row, columnIndex] = new_key

                # PUTTING THE KEY IN THE CORRECT POSITION IN currentMatrix -----------------------

                # Calculate where the first 0 is within currentMatrix[row,columnIndex]
                # Remember, currentMatrix[row,columnIndex]  has shape (1,3)
                index = np.where(self.currentMatrix[row,columnIndex] == 0)

                """
                Output of index could be: (array([1, 2]), array([0, 0]))
                This means:  (x)(y) --> a zero is at (y=0,x=1) and another zero is at (y=0,x=2)
                HENCE, we don't need the (0,0) information (=>index[1]=(0,0) )
                We only need the info that a zero is at 1 and another one at 2 (=>index[0]=(1,2))
                HENCE, we are actually only interested in that 1 and not the 2, so:
                index[0][0] = 1
                """
                if len(index[0] == 0):  # If there are no zeroes in that position
                    print("Warning, more than 3 sprites in 1 tile! Cannot add another one")
                else:
                    self.currentMatrix[row,columnIndex,index[0][0]] = new_key

                # Initialize reference for later
                new_sprite = None

                # CREAING THE SPRITE
                if column[row] == 1:  # If block
                    new_sprite = SpriteBlock(row*16*2,columnIndex*16*2,new_key)
                    self.all_sprites.add(new_sprite)
                if column[row] == 2:  # If player
                    print("added player")
                    new_sprite = SpritePlayer(row*16*2,columnIndex*16*2,new_key)
                    self.playerSprites.add(new_sprite)
                    #self.env_sprites.add(self.player)


                # Add sprite to dictionary with the assigned key
                self.spriteDict[new_key] = new_sprite







    def display(self, screen):
        screen.fill('black')

        self.all_sprites.draw(screen)
        self.playerSprites.draw(screen)

        #Update everything
        pygame.display.update()


