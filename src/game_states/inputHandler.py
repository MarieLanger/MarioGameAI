import pygame
import sys

class InputHandler():

    def analyzeInputs(self, state):
        pass


class InputsHumanGame(InputHandler):
    def analyzeInputs(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                state.game.exitCurrentState()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    state.game.exitCurrentState()
                if event.key == pygame.K_RIGHT:
                    state.rightKeyHold = True
                if event.key == pygame.K_LEFT:
                    state.leftKeyHold = True
                if event.key == pygame.K_UP:
                    state.upKeyHold = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    state.rightKeyHold = False
                if event.key == pygame.K_LEFT:
                    state.leftKeyHold = False
                if event.key == pygame.K_UP:
                    state.upKeyHold = False
                    state.player.jumpKeyReleased()

class InputsAIGame(InputHandler):
    def __init__(self):
        super.__init__()

        self.previousUpInput = True
        self.currentUpInput = False

    def analyzeInputs(self, state):

        # Get current game state
        # Put state through model
        # Calculate output
        # Adjust state.rightKeyHold + state.leftKeyHold + state.upKeyHold + state.player.jumpKeyReleased()


        # Check pygame inputs and close window if necessary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                state.game.exitCurrentState()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    state.game.exitCurrentState()

        # Enable jumping
        if self.previousUpInput and not self.currentUpInput:
            state.player.jumpKeyReleased()





"""class InputsTitle(InputHandler):
    pass

class InputsEnd(InputHandler):
    def analyzeInputs(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.exitCurrentState()
                    game.stateMachine.peek().initializeLevel()
        return None"""

