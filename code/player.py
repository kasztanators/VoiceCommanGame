import pygame

from settings import *


class Player:
    def __init__(self, pos_x=0, pos_y=0):

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.vel_y = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = (255, 0, 0)
        self.jump = False
        self.running = False
        self.rect = pygame.Rect((pos_x, pos_y, 80, 180))

    def move(self):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -SPEED
            self.running = True
        if key[pygame.K_RIGHT]:
            dx = SPEED
            self.running = True
        # jumping
        if key[pygame.K_SPACE] and not self.jump:
            self.vel_y = -30
            self.jump = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - 110:
            self.vel_y = 0
            self.jump = False
            dy = SCREEN_HEIGHT - 110 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def refresh(self, screen):
        self.move()
        self.draw_player(screen)
