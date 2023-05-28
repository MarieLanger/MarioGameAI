from .player import *
import pygame, sys
from .inputHandlerTitle import *

"""
The user always controls the whole program
"""
class Controller():

    # There can be a human player or an AI player
    player = None

    # Other MVC components
    model = None
    view = None

    def __init__(self):
        self.setPlayer("human")
        self.inputHandler = InputHandlerTitle()

    # The player is the strategy of Controller (=composition)
    def setPlayer(self, playerType):
        if playerType == "human":
            player = HumanPlayer()
        if playerType == "ai":
            pass  # todo for later

    def handleInputs(self):
        """for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()"""
        self.inputHandler.handleInputs()



    def changeGameState(self, newState, newHandler):
        self.model.setProgramState(newState)
        self.changeInputHandler(newHandler)
        #todo: change view too


    def changeInputHandler(self, newHandler):
        self.inputHandler = newHandler

