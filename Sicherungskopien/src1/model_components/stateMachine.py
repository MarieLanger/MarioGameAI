class StateMachine():
    def __init__(self):
        self.stateStack = []

    # looks onto top of stack without altering it
    def peek(self):
        try:
            return self.stateStack[-1]
        except IndexError:  # if stack empty
            return None

    # pushes new state onto the stack
    def push(self,state):
        self.stateStack.append(state)
        return

    # removes top element and returns it
    def pop(self):
        if len(self.stateStack)<1:
            return None
        else:
            self.stateStack.pop()