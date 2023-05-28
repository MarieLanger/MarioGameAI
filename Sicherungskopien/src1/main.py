import pygame, sys
#from controller.controllerClass import *
#from controller import controllerClass
import controller_components
from settings import *


class Game:

    # MVC components
    controller = None
    model = None
    view = None

    """def __init__(self):
        self.controller = controller_components.Controller()
        # setup pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        # event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # filling screen
            self.screen.fill('black')
            pygame.display.update()
            self.clock.tick(FPS)"""


    def __init__(self):
        self.controller = controller_components.Controller()
        # setup pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()


    def run(self):
        # event loop
        while True:
            #game.HandleEvents();
            #game.Update();
            #game.Draw();

            self.controller.handleInputs()

            # filling screen
            self.screen.fill('black')
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    print("Hello World")
    game = Game()
    game.run()
