from .state import State

class TitleState(State):

    def __init__(self):
        self.text = "Super Princess Peach"
        self.text_pos = (20, 30)
        self.text_col = (255,255,255)

        self.menu = ("Human Input", "AI input","other")
        self.menu_pos = (50, 40)
        self.menu_col = (255,255,255)
        self.menu_distances = 20  # distance between the entries

        self.menuSelection = 0  # 0th, 1st, or 2nd option
        self.menuSelection_col = (255,105,180)  # pink


    def changeSelection(self,value):
        """
        Changes the selected options.
        :param value: Either -1 (=go left) or +1 (go right)
        :return:
        """

        # Check if input was valid
        if abs(value) != 1:
            return
        # Add value to selection and bring it between 0-2 if bounds were overstepped (if -1 or 3 occured)
        self.menuSelection = (self.menuSelection+value) % 3