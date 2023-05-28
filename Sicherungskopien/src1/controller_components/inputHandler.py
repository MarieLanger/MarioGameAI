"""
Base class for handling inputs depending on the current state.
Defines the interface.
Idea: Depending on the model state, handle inputs differently
(Controller has a reference to this)
"""
class InputHandler():
    def handleInputs(self):
        pass