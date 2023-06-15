import json
import os

import numpy as np
import pygame

from .sprites.helperSprites import GameOverSprite, KillEnvironmentSpritesSprite
from .sprites.spriteBlock import SpriteBlock
from .sprites.spriteCoin import SpriteCoin
from .sprites.spriteContainer import SpriteContainer
from .sprites.spriteEndflag import SpriteEndflag
from .sprites.spriteGoomba import SpriteGoomba
from .sprites.spriteKoopa import SpriteKoopa
from .sprites.spriteMushroom import SpriteMushroom
from .sprites.spritePipe import SpritePipe
from .sprites.spritePiranha import SpritePiranha
from .sprites.spritePlayer import SpritePlayer
from .sprites.spriteStar import SpriteStar
from .state import State
from .stateGameOver import StateGameOver
from .stateLevelCompleted import StateLevelCompleted

from .handlers.inputHandlerHuman import InputHandlerHuman
from .handlers.inputHandlerAI import InputHandlerAI


class StateGame(State):
    """
    State for when the game gets played with human inputs.
    """

    def __init__(self, game, inputHandler, levelOutcomeHandler):
        State.__init__(self, game)

        data = json.load(open('../data/titleState.json'))
        self.level = data['level']  # a number from 1 to 10
        #self.tinyFont = pygame.font.SysFont('Comic Sans MS', 20)
        self.tinyFont = pygame.font.SysFont('consolas', 17)

        self.inputHandler = None
        if inputHandler == "Human":
            self.inputHandler = InputHandlerHuman(self)
        elif inputHandler == "AI":
            self.inputHandler = InputHandlerAI(self)

        self.levelOutcomeHandler = None
        # todo: set this with levelOutcomeHandler-parameter


        # Declaring game related variables -----------------------------------------------
        self.levelMatrix = None

        self.levelMoving = True
        self.borderCloseness = 0

        # Note down inputs, necessary for continued movement
        self.leftKeyHold = False
        self.rightKeyHold = False
        self.upKeyHold = False
        self.previousUpInput = self.upKeyHold

        self.levelProgress = 0
        self.pixelProgress = 0
        self.enemiesKilled = 0
        self.startTime = 0
        self.currentTime = 0

        self.player = None
        self.playerSprites = None
        self.env_sprites = None
        self.blockSprites = None
        self.enemySprites = None
        self.itemSprites = None
        self.helperSprites = None
        self.endFlagSprites = None
        self.coinCount = 0
        self.levelOutcome = 0

        # Setting the game related variables with values
        self.initializeLevel()

    def initializeLevel(self):
        """
        Initializes level.
        Putting this into a separate method allows to reset the level after a game over got encountered.
        """
        # Load level ---------------------------------------------------------------------------
        path = "\..\data\levels"
        filename = "\level" + str(self.level) + ".txt"
        fullpath = os.getcwd() + path + filename
        self.levelMatrix = np.genfromtxt(fullpath, delimiter='\t')  # A guide which sprites to create
        print("the shape of the level is:", self.levelMatrix.shape)

        # Necessary for movement at borders.
        # When Peach is close to a border or goes back, Peach moves and the sprites stay still.
        # When Peach moves forward, the level moves and peach stays still
        self.levelMoving = True
        self.borderCloseness = 0  # When peach goes left, measure how close she is to the border

        # Pygame only detects when keys got pressed or released, but not when they stay held
        # This is a workaround around this
        self.leftKeyHold = False
        self.rightKeyHold = False
        self.upKeyHold = False
        self.previousUpInput = self.upKeyHold

        # How far the level got reached, in tiles and pixels
        self.levelProgress = 23
        self.pixelProgress = 23 * 32
        self.startTime = pygame.time.get_ticks()
        self.currentTime = pygame.time.get_ticks()

        # Kill counter for enemies
        self.enemiesKilled = 0

        # Coins
        self.coinCount = 0

        # Communicate level completed (+1) or game over (-1)
        self.levelOutcome = 0

        # Kill player if no progress has been made for 10 seconds
        self.levelProgress10secondsAgo = [self.currentTime/1000,self.levelProgress]

        # Creating the sprite groups
        self.env_sprites = pygame.sprite.Group()  # contains all sprites except the player
        self.playerSprites = pygame.sprite.Group()
        self.blockSprites = pygame.sprite.Group()
        self.enemySprites = pygame.sprite.Group()
        self.itemSprites = pygame.sprite.Group()
        self.helperSprites = pygame.sprite.Group()
        self.endFlagSprites = pygame.sprite.Group()


        # Creating the sprites and playing them into the groups
        new_sprite = SpritePlayer(11 * 16 * 2, 2 * 16 * 2, self.blockSprites, self)
        self.player = new_sprite
        self.playerSprites.add(new_sprite)

        # The player sees 13x24 tiles at once
        for col in range(24):
            self._loadSpriteColumn(self.levelMatrix[:, col], col, 0)

        self.helperSprites.add(GameOverSprite(self.player, self))
        self.helperSprites.add(KillEnvironmentSpritesSprite(self.env_sprites))


    def update (self):
        # Update time
        self.currentTime = pygame.time.get_ticks()

        # Get the inputs from the handler
        self.inputHandler.handleInputs()


        # If up-key got released, then register end of jump
        # If-statement checks if up-key got released, that way jumpKeyReleased() is not called in the input-handler!
        if self.previousUpInput and not self.upKeyHold:
            self.player.jumpKeyReleased()
        self.previousUpInput = self.upKeyHold


        # From here: Use noted down inputs to change model
        # HANDLE COLLISIONS WITH BLOCKS -----------------------------------------------------------------------------

        # Left/Right
        # Idea: Let peach move where she wants and afterwards check if a collision occurred with it
        # While doing this, handle borders
        self._borderHandling(self.leftKeyHold, self.rightKeyHold)

        # Top/Bottom
        # Jumping is only allowed when touching the ground
        (topCol, bottomCol) = self.player.checkBottomTopTouches()
        if bottomCol:
            if self.upKeyHold:
                self.player.jumpKeyPressed()
        else:
            self.player.applyGravity()

        # If top got hit, stop jumping
        if topCol:
            self.player.jumpKeyReleased()


        # WHEN INPUT ANALYZING IS FINISHED, UPDATE SPRITES ------------------------------------------------
        # Update all sprites
        self.env_sprites.update()  # during update, setLevelOutcome may or may not be called
        self.playerSprites.update()
        self.helperSprites.update()


        # Induce game over when no progress has been made
        if self.currentTime/1000 > self.levelProgress10secondsAgo[0]+5:
            if self.levelProgress10secondsAgo[1] == self.levelProgress:
                self.levelOutcome = -1
            else:
                self.levelProgress10secondsAgo = [self.currentTime/1000,self.levelProgress]


        # If game over
        if self.levelOutcome == -1:
            return StateGameOver(self.game, self)
        # If level completed
        elif self.levelOutcome == +1:
            return StateLevelCompleted(self.game, self)

    def setLevelOutcome(self, value):
        # value: -1 game over   +1 completed
        self.levelOutcome = value

    def _loadSpriteColumn(self, column, columnIndex, offset):
        """
        Creates new sprites for 1 new column.
        Operates with player position (=offset)

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
                    if column[row - 1] == 2:
                        break
                    height = 32
                    i = 1
                    while True:
                        if column[row + i] == 2:
                            height += 32
                            i += 1
                        else:
                            break
                    new_sprite = SpritePipe(row * 16 * 2, columnIndex * 16 * 2 - offset, height)
                    self.env_sprites.add(new_sprite)
                    self.blockSprites.add(new_sprite)

                elif column[row] == 3:  # If container for coin
                    content_sprite = SpriteCoin(-50, columnIndex * 16 * 2 - offset, self,self.player)
                    self.env_sprites.add(content_sprite)
                    self.itemSprites.add(content_sprite)

                    """content_sprite = SpriteStar(30, columnIndex * 16 * 2 - offset, self.player, self.blockSprites)
                    self.env_sprites.add(content_sprite)
                    self.itemSprites.add(content_sprite)"""

                    new_sprite = SpriteContainer(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player,
                                                 self.blockSprites, self.enemySprites, self.env_sprites, content_sprite, -1)
                    self.env_sprites.add(new_sprite)
                    self.blockSprites.add(new_sprite)

                elif column[row] == 4:  # if container with mushroom
                    """new_sprite = SpriteMushroom(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player,
                                                self.blockSprites)
                    self.env_sprites.add(new_sprite)
                    self.itemSprites.add(new_sprite)"""
                    content_sprite = SpriteMushroom(-50, columnIndex * 16 * 2 - offset, self.player, self.blockSprites)
                    self.env_sprites.add(content_sprite)
                    self.itemSprites.add(content_sprite)

                    new_sprite = SpriteContainer(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player,
                                                 self.blockSprites, self.enemySprites, self.env_sprites, content_sprite, +1)
                    self.env_sprites.add(new_sprite)
                    self.blockSprites.add(new_sprite)
                elif column[row] == 5:  # if container with star
                    content_sprite = SpriteStar(-50, columnIndex * 16 * 2 - offset, self.player, self.blockSprites)
                    self.env_sprites.add(content_sprite)
                    self.itemSprites.add(content_sprite)

                    new_sprite = SpriteContainer(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player,
                                                 self.blockSprites, self.enemySprites, self.env_sprites, content_sprite, +1)
                    self.env_sprites.add(new_sprite)
                    self.blockSprites.add(new_sprite)
                    """new_sprite = SpriteStar(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player, self.blockSprites)
                    self.env_sprites.add(new_sprite)
                    self.itemSprites.add(new_sprite)"""
                elif column[row] == 6:  # if coin
                    new_sprite = SpriteCoin(row * 16 * 2, columnIndex * 16 * 2 - offset, self, self.player)
                    self.env_sprites.add(new_sprite)
                    self.itemSprites.add(new_sprite)
                elif column[row] == 7:  # if goomba
                    new_sprite = SpriteGoomba(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player,
                                              self.blockSprites, self)
                    self.env_sprites.add(new_sprite)
                    self.enemySprites.add(new_sprite)
                elif column[row] == 8:  # if koopa
                    new_sprite = SpriteKoopa(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player,
                                             self.blockSprites, self.enemySprites, self.env_sprites, self)
                    self.env_sprites.add(new_sprite)
                    self.enemySprites.add(new_sprite)
                elif column[row] == 9:  # if piranha
                    new_sprite = SpritePiranha(row * 16 * 2, columnIndex * 16 * 2 - offset, self.player, self)
                    self.env_sprites.add(new_sprite)
                    self.enemySprites.add(new_sprite)
                elif column[row] == 10:
                    new_sprite = SpriteEndflag(row * 16 * 2, columnIndex * 16 * 2 - offset, self, self.player)
                    self.env_sprites.add(new_sprite)
                    self.endFlagSprites.add(new_sprite)

    def _evaluateTilePos(self):
        """
        If another 32x32 tile got touched, load new column
        """
        if int(self.pixelProgress / 32) > self.levelProgress:
            self.levelProgress += 1
            self._loadSpriteColumn(self.levelMatrix[:, self.levelProgress], 23, self.pixelProgress % 32)

    def _checkCollisions(self):
        """
        Checks if after walking, peach clipped into something.
        If yes, adjust x-position of everything.
        :return: 0: If nothing needs to be changed, -2 if position has to be adjusted by 2 to the left, etc.
        """
        move = 0
        col_list = self.player.checkCollisions_blocks()
        if len(col_list) == 0:
            return move  # No clipping occured
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
        no level exists (=bad).
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
                """
                If right key gets pressed, closeness to border gets smaller
                If peach is at original closeness-position, peach now stays and sprites move again
                Hence, states switch

                Further problem here:
                If clip occured, then borderCloseness could be e.g. 4
                For this, peach needs to move 4 pixels
                And then it needs to switch to levelmoving
                AND the level needs to move 1 pixel too
                =5 pixels movement in total
                """

                # If big enough, verfahre wie normal
                if self.borderCloseness > 4:
                    self.borderCloseness -= 5
                    if self.borderCloseness == 0:
                        self.levelMoving = True
                    for sprite in self.playerSprites.sprites():
                        sprite.moveRight()
                    adjusted_pos = self._checkCollisions()
                    if adjusted_pos != 0:
                        for sprite in self.playerSprites.sprites():
                            sprite.move_x(adjusted_pos)
                        self.borderCloseness += -adjusted_pos
                else:  # else, a clip occured and do the above
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
                            sprite.moveLeft(5 - self.borderCloseness)
                        self.pixelProgress += 5 - self.borderCloseness
                        adjusted_pos = self._checkCollisions()
                        if adjusted_pos != 0:
                            for sprite in self.env_sprites.sprites():
                                sprite.move_x(-adjusted_pos)
                            self.pixelProgress += adjusted_pos

                        # Clean up
                        self.pixelProgress += 5 - self.borderCloseness
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

    def increaseEnemyKillCounter(self):
        self.enemiesKilled += 1

    def increaseLevel(self):
        self.level += 1




















    def display(self, screen):
        screen.fill('black')

        # Render all sprites
        self.endFlagSprites.draw(screen)
        self.enemySprites.draw(screen)  # enemies have to be at least behind the blocks!
        self.blockSprites.draw(screen)
        self.itemSprites.draw(screen)
        self.playerSprites.draw(screen)  # player is in front of everything
        # self.helperSprites.draw(screen)

        # Render coin text
        #textSurface = self.smallFont.render("Coins: " + str(self.coinCount), False, (255, 255, 255))
        #screen.blit(textSurface, (530, 5))

        """s = pygame.Surface((700, 64), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((0, 0, 0, 180))  # notice the alpha value in the color
        screen.blit(s, (0, 0))"""

        textSurface1 = self.tinyFont.render("Progress: "+ str(self.pixelProgress-736), False, (175, 125, 145))
        textSurface2 = self.tinyFont.render("Enemy kills: " + str(self.enemiesKilled), False, (170,118,118))
        textSurface3 = self.tinyFont.render("Coins: " + str(self.coinCount), False, (110, 110, 38))
        textSurface4 = self.tinyFont.render("Time: " + str(int((self.currentTime - self.startTime)/1000)), False, (110, 110, 110))
        screen.blit(textSurface1, (10, 455))
        screen.blit(textSurface2, (250, 455))
        screen.blit(textSurface3, (250, 429))
        screen.blit(textSurface4, (540, 455))
