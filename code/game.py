import pygame
from settings import *
import sys
from map import Map
from player import Player


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map = Map()
        self.player = Player()

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

        self.player.refresh(self.screen)
