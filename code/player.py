from abc import abstractmethod

import pygame

from settings import *
from bullet import *

class Player:
    def __init__(self, pos_x=0, pos_y=0, color=(255, 0, 0)):

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
        self.is_squatting = False
        self.enemy = None
        self.bullets = []
        self.cooldown = 0
    @abstractmethod
    def move(self):
        pass

    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def refresh(self, screen):
        self.decrease_cooldown()
        self.squat()
        self.move()
        for bullet in self.bullets:
            bullet.refresh(screen)
        self.draw_player(screen)


    def squat(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_c] and not self.is_squatting:
            self.is_squatting = True
            self.rect = pygame.Rect((self.rect.x, self.rect.y + 90, 80, 90))
        elif not key[pygame.K_c] and self.is_squatting:
            self.is_squatting = False
            self.rect = pygame.Rect((self.rect.x, self.rect.y - 90, 80, 180))

    def add_enemy(self, enemy):
        self.enemy = enemy

    def check_enemy_position(self):
        player_rect = self.enemy.rect
        enemy_rect = self.rect

        if player_rect.colliderect(enemy_rect):
            # Collision detected, player cannot move
            return False
        else:
            # No collision detected, player can move
            return True



    def shoot(self):
        if self.cooldown <=0:
            bullet = Bullet(self.rect.x, self.rect.y,self.bullets)
            self.bullets.append(bullet)
            self.cooldown+=10

    def decrease_cooldown(self):
        if self.cooldown >0:
            self.cooldown-=0.5