from .stateMachine import *
from .titleState import *

"""
# State constants
STATE_TITLE = 1
STATE_H_SETTINGS = 2
STATE_AI_SETTINGS = 3
STATE_H_PLAY = 4
STATE_AI_PLAY = 5
STATE_AI_TRAIN = 6
"""



class Model():
    """
    The model contains the entire game logic.
    """

    level = None
    spriteList = []
    peachState = None  # Is peach small, big or star? (state design pattern)


    #currentProgramState = 0

    # Stack where all state objects are stored
    stateMachine = StateMachine



    def __init__(self):
        # Start at title screen
        #self.setProgramState(STATE_TITLE)
        self.stateMachine.push(titleState())

    # Whenever Peach moves and the level matrix says there is a new component
    def createLevelComponent(self):
        pass







    # Getter methods  (todo: Other methods to be added later probably)
    def getSpriteList(self):
        return self.spriteList

    # Setter methods
    def setProgramState(self,newState):
        currentProgramState = newState