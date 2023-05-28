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

        self.menu = ("Human input", "AI input","other")
        self.menu_pos = (30, 150)
        self.menu_col = (255,255,255)
        self.menu_distances = 80  # distance between the entries

        self.menuSelection = 0  # 0th, 1st, or 2nd option
        self.menuSelection_col = (255,105,180)  # pink

        # Sub-menu selections
        self.level_choices = ("all", 1,2,3,4,5,6,7,8,9,10)
        self.aiType_choices = ("Train AI", "Test AI")
        self.selection_choices = ("speedrun","speedrun + coins", "speedrun + coins + enemies")
        self.aiSelection_choices = ("AI1", "AI2", "AI3") # todo: add new ones here later

        self.level_selected = 0  # these are all indices of the above lists
        self.aiType_selected = 0
        self.selection_selected = 0
        self.aiSelection_selected = 0

        self.subSelecting = False  # Does user select the sub-options atm or not? (False=not)
        self.subSelection_selected = 0






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


                if event.key == pygame.K_x:  # x key to switch from main menu to submenu
                    self.subSelecting = not self.subSelecting

                # Sub-menus
                if self.subSelecting:

                    # human input
                    if self.menuSelection == 0:
                        if event.key == pygame.K_LEFT:
                            self.level_selected = (self.level_selected-1) % 10
                        if event.key == pygame.K_RIGHT:
                            self.level_selected = (self.level_selected+1) % 10

                    # ai input
                    if self.menuSelection == 1:

                        add = 0
                        if event.key == pygame.K_LEFT:
                            add = -1
                        if event.key == pygame.K_RIGHT:
                            add = +1
                        if self.subSelection_selected == 0:
                            self.aiType_selected = (self.aiType_selected+add) % 2
                        elif self.subSelection_selected == 1:
                            self.level_selected = (self.level_selected+add) % 10
                        elif self.subSelection_selected == 2:
                            if self.aiType_selected==0:
                                self.selection_selected = (self.selection_selected+add) % len(self.selection_choices)
                            else:
                                self.aiSelection_selected = (self.aiSelection_selected+add) % len(self.aiSelection_choices)

                        add = 0
                        if event.key == pygame.K_DOWN:
                            add = +1
                        elif event.key == pygame.K_UP:
                            add = -1
                        self.subSelection_selected = (self.subSelection_selected+add)%3


                # Main menu
                else:
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

        # Streifen
        #self._displayText("(settings:)",(80,80,80),(200,210),self.smallFont,screen)
        self._displayText("____________________________________________",(80,80,80),(20,220),self.smallFont,screen)


        # menu sub selections
        cols = ((100,100,100), (255,255,255))
        col = 0


        if self.menuSelection==0:
            text1 = "  • Select level: " + str(self.level_choices[self.level_selected])
            if self.subSelection_selected==0 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text1,col,(20,250),self.smallFont,screen)



        elif self.menuSelection==1:

            text1 = "  • Goal: " + str(self.aiType_choices[self.aiType_selected])
            text2 = "  • Select level: " + str(self.level_choices[self.level_selected])
            if self.aiType_selected==0:
                text3 = "  • Selection criteria: " + str(self.selection_choices[self.selection_selected])
            else:
                text3 = "  • AI: " + str(self.aiSelection_choices[self.aiSelection_selected])



            if self.subSelection_selected==0 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text1,col,(20,250),self.smallFont,screen)


            if self.subSelection_selected==1 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text2,col,(20,280),self.smallFont,screen)


            if self.subSelection_selected == 2 and self.subSelecting:
                col = cols[1]
            else:
                col = cols[0]
            self._displayText(text3,col,(20,310),self.smallFont,screen)




        #Update everything
        #pygame.display.update()


    def _displayText(self,content,color,position,font,screen):
        textSurface = font.render(content,False,color)
        screen.blit(textSurface, position)
