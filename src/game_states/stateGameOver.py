import sys
import pygame
from .state import State


class StateGameOver(State):
    """
    State for the game over screen.
    Restarts the level after being exited.
    """

    def __init__(self, game, prev_state):
        State.__init__(self, game)
        self.prev_state = prev_state

        # Initialize the font
        pygame.font.init()
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 20)
        self.mediumFont = pygame.font.SysFont('Comic Sans MS', 25)
        self.bigFont = pygame.font.SysFont('Comic Sans MS', 45)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Restart level
                    self.game.exitCurrentState()
                    self.game.stateMachine.peek().initializeLevel()
        return None

    def display(self, screen):
        # Displays level frozen in time, but darker
        self.prev_state.display(screen)
        s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((0, 0, 0, 180))  # notice the alpha value in the color
        screen.blit(s, (0, 0))

        # Display text on screen
        textSurface = self.bigFont.render("Game over!", False, (255, 255, 255))
        screen.blit(textSurface, (195, 30))

        textSurface = self.smallFont.render("(Press space to retry)", False, (255, 255, 255))
        screen.blit(textSurface, (207, 100))
