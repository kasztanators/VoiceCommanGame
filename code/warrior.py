from player import *
from wizard import *

class Warrior(Player):
    def __init__(self, pos_x=100, pos_y=200, color=(255, 255, 0)):
        super().__init__(pos_x, pos_y, color)


    def move(self):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.check_enemy_position():
            dx = -SPEED
            self.running = True
        if key[pygame.K_RIGHT]:
            dx = SPEED
            self.running = True
        # jumping
        if key[pygame.K_SPACE] and not self.jump and self.check_enemy_position():
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

