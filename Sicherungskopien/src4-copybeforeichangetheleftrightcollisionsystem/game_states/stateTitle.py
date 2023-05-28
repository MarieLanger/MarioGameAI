import pygame
import sys
from .state import State
from .stateGame import StateGame

class StateTitle(State):
    """
    State for when the game gets started.
    Allows the user to naivgate to other states, such as the gameplay-state
    """

    def __init__(self, game):
        self.game = game

        # Initialize all the text
        self.text = "Super Princess Peach"
        self.text_pos = (100, 20)  #x-position(low:left,high:right)   y-position (low:up, high:down)
        self.text_col = (255,255,255)

        self.menu = ("Human Input", "AI input","other")
        self.menu_pos = (30, 200)
        self.menu_col = (255,255,255)
        self.menu_distances = 80  # distance between the entries

        self.menuSelection = 0  # 0th, 1st, or 2nd option
        self.menuSelection_col = (255,105,180)  # pink

        # Initialize the font
        pygame.font.init()
        self.smallFont = pygame.font.SysFont('Comic Sans MS', 20)
        self.mediumFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.bigFont = pygame.font.SysFont('Comic Sans MS', 45)

    def handleInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # go left in selection
                    self.menuSelection = (self.menuSelection-1) % 3  # modulo ensures to stay between 0-2
                if event.key == pygame.K_RIGHT:
                    # go right in selection
                    self.menuSelection = (self.menuSelection+1) % 3
                if event.key == pygame.K_SPACE:
                    if self.menuSelection==0:
                        return StateGame(self.game)
        return None

    def display(self, screen):
        screen.fill('black')

        #title
        x_pos = (640-self.bigFont.size(self.text)[0])/2
        self._displayText(self.text,self.text_col,(x_pos,self.text_pos[1]),self.bigFont,screen)

        #menu items
        x_pos = self.menu_pos[0]
        for item in range(3):

            #If the current item is selected, change its color
            if item==self.menuSelection:
                col = self.menuSelection_col
            else:
                col = self.menu_col

            # Render text
            self._displayText(self.menu[item],col,(x_pos,self.menu_pos[1]),self.mediumFont,screen)

            # calculate x_position of next menu item
            # this is dependent on the width of the previous item and the distance
            x_pos += self.mediumFont.size(self.menu[item])[0] + self.menu_distances


        #Update everything
        pygame.display.update()


    def _displayText(self,content,color,position,font,screen):
        textSurface = font.render(content,False,color)
        screen.blit(textSurface, position)
