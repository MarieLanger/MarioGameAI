import sys
import pygame

from .state import State


class StateTrainingCompleted(State):
    """
    State for when a level got completed.
    Allows to enter new level by adjusting the main state stack.
    """

    def __init__(self, game, prev_state):
        State.__init__(self, game)
        self.prev_state = prev_state

        # Initialize the font
        pygame.font.init()
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 20)
        self.mediumFont = pygame.font.SysFont('Comic Sans MS', 25)
        self.bigFont = pygame.font.SysFont('Comic Sans MS', 45)

        self.game.stateMachine.peek().increaseLevel()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.exitCurrentState()
                    self.game.exitCurrentState()
        return None

    def display(self, screen):
        # Displays level frozen in time, but darker
        self.prev_state.display(screen)
        s = pygame.Surface((1000, 750), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((0, 0, 0, 180))  # notice the alpha value in the color
        screen.blit(s, (0, 0))

        # Display text on screen
        textSurface = self.bigFont.render("Training finished! :)", False, (255, 255, 255))
        screen.blit(textSurface, (130, 30))

        textSurface = self.smallFont.render("(Press space to go back to the title screen)", False, (255, 255, 255))
        screen.blit(textSurface, (170, 100))
