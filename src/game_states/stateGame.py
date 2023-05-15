import pygame
import sys
import os
import numpy as np

from .state import State
from .stateGameOver import StateGameOver
# from .stateTitle import StateTitle    no!!!! because we want to exit this state, not put another title on top of it!!
# otherwise circular dependency!!!!!!

from .sprites.spriteTest import SpriteTest  # YOU NEED A DOT BEFORE THE FOLDER NAME AAAAAAAAAAAAAAAAAAAAHHHHHHH
from .sprites.spriteBlock import SpriteBlock
from .sprites.spritePlayer import SpritePlayer
from .sprites.spriteCoin import SpriteCoin
from .sprites.spritePipe import SpritePipe
from .sprites.spriteGoomba import SpriteGoomba
from .sprites.spritePiranha import SpritePiranha
from .sprites.helperSprites import GameOverSprite, KillEnvironmentSpritesSprite
from .sprites.spriteMushroom import SpriteMushroom


class StateGame(State):
    """
    State for when the game gets played
    """

    def __init__(self, game):
        self.game = game

        # Game related variables --------------------------------------------------------------
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 20)

        # Load level ---------------------------------------------------------------------------
        path = "\..\data\levels"
        filename = "\level1.txt"
        fullpath = os.getcwd() + path + filename
        self.levelMatrix = np.genfromtxt(fullpath, delimiter='\t')  # A guide which sprites to create
        print("the shape of the level is:", self.levelMatrix.shape)

        self.initializeLevel()


    def initializeLevel(self):
        """
        Initializes level.
        Putting this into a separate method allows to reset the level after a game over got encountered
        :return:
        """
        # Necessary for movement at borders.
        # When Peach is close to a border or goes back, Peach moves and the sprites stay still.
        # When Peach moves forward, the level moves and peach stays still
        self.levelMoving = True
        self.borderCloseness = 0  # When peach goes left, measure how close she is to the border

        # Pygame only detects when keys got pressed or released, but not when they stay held -----
        # This is a workaround around this
        self.leftKeyHold = False
        self.rightKeyHold = False
        self.upKeyHold = False

        # There can be maximally 13x25 tiles visible at 1 time (25 because 2 half tiles can be seen)
        # self.currentMatrix = self.levelMatrix[0:13, 0:25]

        # How far the level got reached, in tiles
        # Initialized by 25: maximally we see the 25th tiles in x-dimension
        # 24: 0-24 = 25 entries
        self.levelProgress = 23
        self.pixelProgress = 23*32

        # Create all the sprite objects -------------------------------------------------
        # Creating the sprite groups
        self.env_sprites = pygame.sprite.Group()  # contains all sprites except the player
        self.playerSprites = pygame.sprite.Group()
        self.player = None
        self.blockSprites = pygame.sprite.Group()
        self.coinSprites = pygame.sprite.Group()
        self.enemySprites = pygame.sprite.Group()
        self.itemSprites = pygame.sprite.Group()
        self.helperSprites = pygame.sprite.Group()

        # Coins
        self.coinCount = 0

        # Communicate level completed (+1) or game over (-1)
        self.levelOutcome = 0





        # Actually creating the first sprites at the start of the level + adding them into a group ---------------

        # Creating the player
        new_sprite = SpritePlayer(11 * 16 * 2, 2 * 16 * 2, self.blockSprites, self)
        self.playerSprites.add(new_sprite)
        self.player = new_sprite

        # The player sees 13x24 tiles at once
        for col in range(24):
            self._loadSpriteColumn(self.levelMatrix[:, col], col, 0)

        self.helperSprites.add(GameOverSprite(self.player, self))
        self.helperSprites.add(KillEnvironmentSpritesSprite(self.env_sprites))

        self.env_sprites.add(SpriteTest())  # todo: remove this line later


    def handleInputs(self):
        # Note down inputs --------------------------------------------
        # Necessary to have continued movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.exitCurrentState()
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
        # Idea: Let peach move where she wants and afterwards check if a collision occurred with it
        # While doing this, I always have to handle borders
        self._borderHandling(self.leftKeyHold, self.rightKeyHold)


        # You can only jump if you touch the ground, check this here and handle key inputs
        (topCol, bottomCol) = self.player.checkBottomTopTouches()
        if bottomCol:
            # I can only jump if I am standing on the ground
            # I am not a space rocket.
            if self.upKeyHold:
                self.player.jumpKeyPressed()
        else:
            # Newton says that I have to abide by the law of gravity after I jumped
            self.player.applyGravity()
        if topCol:
            self.player.jumpKeyReleased()
            # If I hit something on top I stop jumping
            # I am not a quantum particle tunnel through an energy barrier




        # todo: Collisions with enemies, items, end flag -----------------------------------------------






        # WHEN INPUT ANALYZING IS FINISHED, UPDATE SPRITES ------------------------------------------------
        # Update all sprites
        self.env_sprites.update()    # during update, setLevelOutcome may or may not be called
        self.playerSprites.update()
        self.helperSprites.update()

        # If game over
        if self.levelOutcome == -1:
            return StateGameOver(self.game,self)

        # If level completed
        if self.levelOutcome == +1:
            pass


    def setLevelOutcome(self, value):
        # value: -1 game over   +1 completed
        self.levelOutcome = value

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
                # CREAING THE SPRITES
                if column[row] == 1:  # If block
                    new_sprite = SpriteBlock(row * 16 * 2, columnIndex * 16 * 2 - offset)
                    self.env_sprites.add(new_sprite)
                    self.blockSprites.add(new_sprite)
                elif column[row] == 2:  # If pipe
                    # If column above has pipe, then pipe has already been created
                    if column[row-1] == 2:
                        break
                    height = 32
                    i = 1
                    while True:
                        if column[row+i] == 2:
                            height += 32
                            i += 1
                        else:
                            break
                    new_sprite = SpritePipe(row * 16 * 2, columnIndex * 16 * 2 - offset, height)
                    self.env_sprites.add(new_sprite)
                    self.blockSprites.add(new_sprite)
                    """if column[row] == 2:  # If player
                    #new_sprite = SpritePlayer(row * 16 * 2, columnIndex * 16 * 2, self.env_sprites)
                    # Column index (2nd input is fixed for player!
                    new_sprite = SpritePlayer(row * 16 * 2, 2 * 16 * 2, self.blockSprites)
                    self.playerSprites.add(new_sprite)
                    self.player = new_sprite"""
                elif column[row] == 6:  #if coin
                    new_sprite = SpriteCoin(row * 16 * 2, columnIndex * 16 * 2 - offset, self,self.player)
                    self.env_sprites.add(new_sprite)
                    self.coinSprites.add(new_sprite)
                elif column[row] == 7:  #if goomba
                    new_sprite = SpriteGoomba(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player, self.blockSprites)
                    self.env_sprites.add(new_sprite)
                    self.enemySprites.add(new_sprite)
                elif column[row] == 9:  #if piranha
                    new_sprite = SpritePiranha(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player)
                    self.env_sprites.add(new_sprite)
                    self.enemySprites.add(new_sprite)
                elif column[row] == 4:  #if mushroom
                    new_sprite = SpriteMushroom(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player)
                    self.env_sprites.add(new_sprite)
                    self.itemSprites.add(new_sprite)


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


    def _checkCollisions(self):
        """
        Checks if after walking, peach clipped into something.
        If yes, adjust x-position of everything
        :return: 0: If nothing needs to be changed, -2 if position has to be adjusted by 2 to the left, etc
        """
        move = 0
        col_list = self.player.checkCollisions_blocks()
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
                for sprite in self.env_sprites.sprites():
                    sprite.moveLeft()
                self.pixelProgress += 5
                adjusted_pos = self._checkCollisions()
                if adjusted_pos != 0:
                    for sprite in self.env_sprites.sprites():
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
                    for sprite in self.env_sprites.sprites():
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
                            sprite.move_x(adjusted_pos)   # i flipped the sign and it worked?
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
                            sprite.move_x(adjusted_pos)
                        self.borderCloseness += -adjusted_pos
                    else:
                        # Move whole level and check for collisions again
                        for sprite in self.env_sprites.sprites():
                            sprite.moveLeft(5-self.borderCloseness)
                        self.pixelProgress += 5-self.borderCloseness
                        adjusted_pos = self._checkCollisions()
                        if adjusted_pos != 0:
                            for sprite in self.env_sprites.sprites():
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






    def increaseCoinCounter(self):
        self.coinCount += 1



    def display(self, screen):
        screen.fill('black')

        # Render all sprites
        #self.env_sprites.draw(screen)

        self.enemySprites.draw(screen)  # enemies have to be at least behind the blocks!

        self.blockSprites.draw(screen)
        self.coinSprites.draw(screen)
        self.itemSprites.draw(screen)

        self.playerSprites.draw(screen)  # player is in front of everything

        #self.helperSprites.draw(screen)

        # Render coin text
        textSurface = self.smallFont.render("Münzen: "+str(self.coinCount),False,(255,255,255))
        screen.blit(textSurface, (540,5))


        # Update everything
        #pygame.display.update()
