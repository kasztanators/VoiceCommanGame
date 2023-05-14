import pygame
from settings import SCREEN_WIDTH


class Bullet:
    def __init__(self, x, y, bullet_list, bullet_speed):
        self.x = x
        self.y = y
        self.speed = bullet_speed
        self.color = (255, 0,0)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.bullet_list = bullet_list

    def draw_bullet(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def refresh(self, screen):
        self.delete_bullet()
        self.move()
        self.draw_bullet(screen)

    def move(self):
        self.x += self.speed
        self.rect.x = self.x

    def delete_bullet(self):
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH-50:
            self.bullet_list.remove(self)
