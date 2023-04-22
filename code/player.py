from abc import abstractmethod

import pygame

from settings import *


class Player:
    def __init__(self, pos_x=0, pos_y=0,color =(255, 0, 0)):

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.vel_y = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.jump = False
        self.running = False
        self.rect = pygame.Rect((pos_x, pos_y, 80, 180))

    @abstractmethod
    def move(self):
        pass
    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def refresh(self, screen):
        self.move()
        self.draw_player(screen)
