from player import *


class Wizard(Player):
    def __init__(self, pos_x=100, pos_y=0, color=(255, 0, 0)):
        super().__init__(pos_x, pos_y, color, 100)
        self.squat_key = pygame.K_s
        self.bullet_img = "axe"

    def move(self):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -SPEED
            self.running = True
        if key[pygame.K_d] and self.rect.x + self.rect.width < SCREEN_WIDTH/2-100:
            dx = SPEED
            self.running = True
        # jumping
        if key[pygame.K_w] and not self.jump:
            self.vel_y = -30
            self.jump = True
        if key[pygame.K_SPACE]:
            self.shoot(10)
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
