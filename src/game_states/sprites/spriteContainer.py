import pygame

from .spriteBlock import SpriteBlock
from .spriteCoin import SpriteCoin


class SpriteContainer(SpriteBlock):
    """
    A container that holds 1 content (=item or coin).
    Behaves like a normal block, except that the content can be triggered by hitting it from below.
    If an enemy stands on top of it while container got hit, the enemy dies.
    :param
        - y_pos: starting y position
        - x_pos: starting x position
        - player: Reference to the player sprite
        - blockgroup, enemygroup, envgroup: References to the respective sprite groups
        - content: A reference to the item/coin that's inside the container
    """

    def __init__(self, y_pos, x_pos, player, blockgroup, enemygroup, envgroup, content, contentID):
        SpriteBlock.__init__(self, y_pos, x_pos)

        # References
        self.player = player
        self.blockGroup = blockgroup
        self.enemyGroup = enemygroup
        self.envGroup = envgroup

        self.content = content
        self.contentID = contentID

        # Block-color
        import sys
        self.image = pygame.image.load(sys.path[1] + '/data/Graphics/mushroom/1.png')

        # Containers belong to the block-group, hence, cannot collide with the player.
        # Solution: Creating a colliderect that is wider vertically and check collisions with this.
        # (Blockgroup is needed because e.g. player should be able to stand on a container)
        self.collideRect = pygame.Rect(0, 0, 32, 40)
        self.collideRect.center = self.rect.center

    def update(self):
        """
        What sprites do on their own, independent of player inputs.
        Container checks if the player hit it from below. For more details, see class description.
        """
        if self.player.rect.collidepoint(self.collideRect.midbottom):
            # Change to an "emptied container"
            self._createBlock()
            self._spawnContent()

            # If enemy stands on top of container, kill it
            for enemy in self.enemyGroup.sprites():
                if self.collideRect.colliderect(enemy.rect):
                    enemy.kill()

            # Remove container
            self.kill()

    def _createBlock(self):
        # Creating a normal block-sprite
        new_sprite = SpriteBlock(self.rect.y, self.rect.x)
        self.envGroup.add(new_sprite)
        self.blockGroup.add(new_sprite)

    def _spawnContent(self):
        # Items spawn above, coins spawn "collected"
        if isinstance(self.content, SpriteCoin):
            self.content.rect.topleft = self.rect.bottomleft
        else:
            self.content.rect.bottomleft = self.rect.topleft
            self.content.activate()

    def writeState(self, matrix, playerX, playerY):
        """
        Writing its own position into the state.
        :param matrix:
        :param playerX:
        :param playerY:
        :return:
        """
        if self._withinStateMatrix(playerX, playerY, self.rect.x, self.rect.y):
            # Normalize positions
            newx = self.rect.x - (playerX + self.normX)
            newy = self.rect.y - (playerY + self.normY)

            # Save state in first matrix
            matrix[newy // 32, newx // 32, 1] = self.contentID

    """Adding functionality to the movement methods because colliderect also needs to be updated"""
    def moveLeft(self, value=5):
        self.rect.x -= value
        self.collideRect.x -= value

    def moveRight(self, value=5):
        self.rect.x += value
        self.collideRect.x += value

    def move_x(self, value):
        self.rect.x += value
        self.collideRect.x += value


