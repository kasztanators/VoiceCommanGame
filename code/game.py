import pygame
from settings import *
import sys
from map import Map
from wizard import Wizard
from warrior import Warrior

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map = Map()
        self.wizard = Wizard()
        self.warrior = Warrior()
        self.wizard.add_enemy(self.warrior)
        self.warrior.add_enemy(self.wizard)




    def run(self):
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.refresh()

            pygame.display.update()
            self.clock.tick(60)

    def refresh(self):
        self.map.refresh(self.screen)

        self.warrior.refresh(self.screen)
        self.wizard.refresh(self.screen)