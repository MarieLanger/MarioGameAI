class State():
    """
    Interface of the base State class.
    All other States inherit from this class and have to implement the 2 methods.
    (Details on how to implement each method can be found in the respective documentation.)
    """

    def __init__(self,game):
        """
        Initializes the state.
        :param game: All states have a reference to the program that the state is in.
        """
        self.game = game

    def update(self):
        """
        Handle user inputs and update the model accordingly.
        :return: If the inputs induced a state change, return the new state. Otherwise, return None.
        If the inputs induced an exit from the current state, call "self.game.exitCurrentState()"
        """
        return None

    def display(self, screen):
        """
        Renders all the model's content onto the screen.
        :param screen: Screen that got created by the game is the input.
        """
        pass
