import json
import sys
import os

import pygame

from .state import State
from .stateGame import StateGame
from .stateOther import StateOther




class StateTitle(State):
    """
    The title state for when the game gets started.
    Allows the user to navigate to other states, such as the gameplay-state, as well as to select options.
    """

    def __init__(self, game):
        State.__init__(self, game)


        # Initialize all the text
        self.text = "SUPER M[ai]RIO BROS"
        self.text_pos = (80, 20)  # x-position(low:left,high:right)   y-position (low:up, high:down)
        self.text_col = (255, 255, 255)

        self.menu = ("Human input", "AI input", "other")
        self.menu_pos = (30, 150)
        self.menu_col = (255, 255, 255)
        self.menu_distances = 80  # distance between the entries
        self.menuSelection_col = (255, 105, 180)  # pink

        # Sub-menu selections
        self.level_choices = ("all", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.aiType_choices = ("Train AI", "Test AI")
        self.selection_choices = ("speedrun", "speedrun + coins", "speedrun + coins + enemies")
        self.aiSelection_choices = []

        # Get all pickle files from "../data/ai/genomes/"
        #print(os.listdir("../data/ai/genomes/"))
        for file in os.listdir("../data/ai/genomes/"):
            if file.endswith(".pickle"):
                self.aiSelection_choices.append(str(file[0:-7]))

        self.subSelecting = False  # Does user select the sub-options atm or not? (False=not)
        self.subSelection_selected = 0

        # Load titleState.json in data folder and adjust model according to it
        data = json.load(open('../data/titleState.json'))
        # these are all indices of the above lists
        self.menuSelection = data['menuSelection']
        self.level_selected = data['level_selected']
        self.aiType_selected = data['aiType_selected']
        self.selection_selected = data['selection_selected']
        self.aiSelection_selected = data['aiSelection_selected']

        if self.aiSelection_selected >= len(self.aiSelection_choices):
            self.aiSelection_selected = 0

        # Initialize fonts
        pygame.font.init()
        self.tinyFont = pygame.font.SysFont('Comic Sans MS', 17)
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 20)
        self.mediumFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.bigFont = pygame.font.SysFont('Comic Sans MS', 45)





    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Switch from main menu to submenu
                if event.key == pygame.K_x:
                    self.subSelecting = not self.subSelecting

                # Sub-menus
                if self.subSelecting:
                    # Human input
                    if self.menuSelection == 0:
                        if event.key == pygame.K_LEFT:
                            self.level_selected = (self.level_selected - 1) % 10
                        if event.key == pygame.K_RIGHT:
                            self.level_selected = (self.level_selected + 1) % 10
                    # AI input
                    if self.menuSelection == 1:
                        add = 0
                        if event.key == pygame.K_LEFT:
                            add = -1
                        if event.key == pygame.K_RIGHT:
                            add = +1
                        if self.subSelection_selected == 0:
                            self.aiType_selected = (self.aiType_selected + add) % 2
                        elif self.subSelection_selected == 1:
                            self.level_selected = (self.level_selected + add) % 10
                        elif self.subSelection_selected == 2:
                            if self.aiType_selected == 0:
                                self.selection_selected = (self.selection_selected + add) % len(self.selection_choices)
                            else:
                                self.aiSelection_selected = (self.aiSelection_selected + add) % len(
                                    self.aiSelection_choices)
                        add = 0
                        if event.key == pygame.K_DOWN:
                            add = +1
                        elif event.key == pygame.K_UP:
                            add = -1
                        self.subSelection_selected = (self.subSelection_selected + add) % 3

                # Main menu
                else:
                    if event.key == pygame.K_LEFT:
                        # Go left in selection
                        self.menuSelection = (self.menuSelection - 1) % 3  # modulo ensures to stay between 0-2
                    if event.key == pygame.K_RIGHT:
                        # Go right in selection
                        self.menuSelection = (self.menuSelection + 1) % 3
                    if event.key == pygame.K_SPACE:
                        if self.menuSelection == 0:
                            return StateGame(self.game, "Human", "Play")
                        elif self.menuSelection == 1:
                            if self.aiType_selected == 0:
                                return StateGame(self.game, "AI", "Train", self.selection_selected+1)
                            elif self.aiType_selected == 1:
                                return StateGame(self.game, "AI", "Play", self.aiSelection_choices[self.aiSelection_selected])
                        elif self.menuSelection == 2:
                            return StateOther(self.game)



                # Finally, save everything in a json file
                self._saveTitleState()
        return None

    def display(self, screen):
        screen.fill('black')

        # Title
        x_pos = (640 - self.bigFont.size(self.text)[0]) / 2
        self._displayText(self.text, self.text_col, (x_pos, self.text_pos[1]), self.bigFont, screen)

        # Menu items
        x_pos = self.menu_pos[0]
        for item in range(3):
            # If the current item is selected, change its color
            if item == self.menuSelection:
                col = self.menuSelection_col
            else:
                col = self.menu_col
            # Render text
            self._displayText(self.menu[item], col, (x_pos, self.menu_pos[1]), self.mediumFont, screen)
            # Calculate x_position of next menu item, this is dependent on the width of the previous item + distance
            x_pos += self.mediumFont.size(self.menu[item])[0] + self.menu_distances

        # Streifen
        # self._displayText("(settings:)",(80,80,80),(200,210),self.smallFont,screen)
        self._displayText("____________________________________________", (80, 80, 80), (20, 220), self.smallFont,
                          screen)
        self._displayText("____________________________________________", (80, 80, 80), (20, 350), self.smallFont,
                          screen)
        self._displayText("""• Press LEFT/RIGHT to navigate between program states.\n• Press SPACE to select a state, press X to adjust options.\n• Within a state, press X to return to the title screen.""", (180,180,180), (20,380), self.tinyFont, screen)


        # Menu sub selections
        cols = ((100, 100, 100), (255, 255, 255))
        col = 0

        if self.menuSelection == 0:
            text1 = "  • Select level: " + str(self.level_choices[self.level_selected])
            if self.subSelection_selected == 0 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text1, col, (20, 250), self.smallFont, screen)
        elif self.menuSelection == 1:
            text1 = "  • Goal: " + str(self.aiType_choices[self.aiType_selected])
            text2 = "  • Select level: " + str(self.level_choices[self.level_selected])
            if self.aiType_selected == 0:
                text3 = "  • Selection criteria: " + str(self.selection_choices[self.selection_selected])
            else:
                text3 = "  • AI: " + str(self.aiSelection_choices[self.aiSelection_selected])

            if self.subSelection_selected == 0 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text1, col, (20, 250), self.smallFont, screen)

            if self.subSelection_selected == 1 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text2, col, (20, 280), self.smallFont, screen)

            if self.subSelection_selected == 2 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text3, col, (20, 310), self.smallFont, screen)

    def _displayText(self, content, color, position, font, screen):
        """
        Helper function to display text.
        """
        textSurface = font.render(content, False, color)
        screen.blit(textSurface, position)

    def _saveTitleState(self):
        """
        Saves the current state into a json file.
        Happens automatically as soon as inputs got changed.
        """
        with open('../data/titleState.json', 'wb') as f:
            if self.level_selected == 0:
                level = 1
            else:
                level = self.level_selected
            data = {"menuSelection": self.menuSelection,
                    "level_selected": self.level_selected,
                    "level": level,
                    "aiType_selected": self.aiType_selected,
                    "selection_selected": self.selection_selected,
                    "aiSelection_selected": self.aiSelection_selected}
            f.write(json.dumps(data, ensure_ascii=False).encode("utf8"))
