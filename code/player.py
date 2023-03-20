import pygame as pg
from support import import_folder

class Player():
    def __init__(self, pos):

        self.direction = pg.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
