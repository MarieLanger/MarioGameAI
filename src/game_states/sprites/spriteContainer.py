import pygame
from .spriteBlock import SpriteBlock
from .spriteCoin import SpriteCoin

class SpriteContainer(SpriteBlock):
    """
    All sprites inherit from pygame.sprite.Sprite.
    A basic block sprite that does nothing
    :param
        - y_pos: starting y position
        - x_pos: starting x position
    """
    def __init__(self, y_pos, x_pos, player, blockgroup, enemygroup, envgroup, content):
        SpriteBlock.__init__(self, y_pos, x_pos)

        self.player = player
        self.blockGroup = blockgroup
        self.enemyGroup = enemygroup
        self.envGroup = envgroup

        self.content = content

        # Block-color
        self.image.fill((63,234,255))

        # Containers belong to the block-group, hence, cannot collide with the player
        # Solution: Creating a colliderect that is wider on the bottom and check collisions with this
        # (Blockgroup is needed because e.g. player should be able to stand on a container)
        self.collideRect = pygame.Rect(0, 0, 32, 40)
        self.collideRect.center = self.rect.center

    def update(self):
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
        new_sprite = SpriteBlock(self.rect.y, self.rect.x)
        self.envGroup.add(new_sprite)
        self.blockGroup.add(new_sprite)

    def _spawnContent(self):
        # Items spawn above, coins spawn collected
        if isinstance(self.content,SpriteCoin):
            self.content.rect.topleft = self.rect.bottomleft
        else:
            self.content.rect.bottomleft = self.rect.topleft



            # Adding functionality to methods because colliderect also needs to be updated
    def moveLeft(self, value=5):
        self.rect.x -= value
        self.collideRect.x -= value

    def moveRight(self, value=5):
        self.rect.x += value
        self.collideRect.x -= value

    def move_x(self, value):
        self.rect.x += value
        self.collideRect.x -= value




    """
    Below: What sprites do after player inputs -----------------------------------------------------------------
    """
