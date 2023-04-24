from player import *


class Wizard(Player):
    def __init__(self, pos_x=0, pos_y=0, color=(255, 0, 0)):
        super().__init__(pos_x, pos_y, color)

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
        if key[pygame.K_d] and self.check_enemy_position():
            dx = SPEED
            self.running = True
        # jumping
        if key[pygame.K_w] and not self.jump and self.check_enemy_position():
            self.vel_y = -30
            self.jump = True
        if key[pygame.K_p]:
            self.shoot()
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
