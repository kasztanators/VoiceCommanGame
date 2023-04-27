from player import *
from wizard import *

class Warrior(Player):
    def __init__(self, pos_x=SCREEN_WIDTH-180, pos_y=200, color=(255, 255, 0)):
        super().__init__(pos_x, pos_y, color, 600)
        self.speech_active = False
    def move(self, command):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > SCREEN_WIDTH/2+100:
            dx = -SPEED
            self.running = True
        if key[pygame.K_RIGHT]:
            dx = SPEED
            self.running = True
        # jumping
        if key[pygame.K_SPACE] and not self.jump:
            self.vel_y = -30
            self.jump = True
        if key[pygame.K_m]:
            self.shoot(-10)
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

