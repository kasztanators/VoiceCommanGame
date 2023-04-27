import pygame

from settings import *


class Map:
    def __init__(self):
        self.bg_img = pygame.image.load("./assets/images/background/background.jpg").convert_alpha()

    def draw_background(self, screen):
        scaled_bg = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    def refresh(self, screen):
        self.draw_background(screen)
