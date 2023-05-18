import pygame
from settings import SCREEN_WIDTH


class Bullet:
    def __init__(self, x, y, bullet_list, bullet_speed, bullet_img):
        self.x = x
        self.y = y
        self.speed = bullet_speed
        self.bullet_img = pygame.image.load(f"./assets/images/bullet/{bullet_img}.png").convert_alpha()
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.bullet_list = bullet_list
        self.is_rotating = True if bullet_img == "axe" else False
        self.rotating_angle = 0

    def draw_bullet(self, screen):
        if self.is_rotating:
            self.rotating_angle -=8
            self.rotating_angle = self.rotating_angle % 360

        image = pygame.transform.rotate(self.bullet_img,self.rotating_angle)
        screen.blit(image, self.rect)

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
