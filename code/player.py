from abc import abstractmethod

import pygame

from settings import *


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
    @abstractmethod
    def move(self):
        pass

    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def refresh(self, screen):
        self.squat()
        self.move()
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

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
