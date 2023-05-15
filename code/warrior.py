from player import *
from wizard import *


class Warrior(Player):
    def __init__(self, pos_x=SCREEN_WIDTH-180, pos_y=200, color=(255, 255, 0)):
        super().__init__(pos_x, pos_y, color, 600)
        self.speech_active = False
        self.squat_key = pygame.K_DOWN
        self.move_left = False
        self.move_right = False
        self.is_squatting_voice = False
        self.bullet_img = "spear"

    def move(self, command):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        if command == "left":
            self.move_right = False
            self.move_left = True
        if command == "right":
            self.move_left = False
            self.move_right = True

        if command == "stop":
            self.move_right = False
            self.move_left = False
        if command == "down" or command =="up":
            self.squat_voice(command)
        key = pygame.key.get_pressed()
        if (key[pygame.K_LEFT] or self.move_left) and self.rect.x > SCREEN_WIDTH/2+100:
            dx = -SPEED
            self.running = True
        if key[pygame.K_RIGHT]or self.move_right:
            dx = SPEED
            self.running = True
        # jumping
        if (key[pygame.K_UP] or command == "up")and not self.jump:
            self.vel_y = -30
            self.jump = True
        if key[pygame.K_m] or command == "go" or command =="yes":
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

    def squat_voice(self, command):
        key = pygame.key.get_pressed()
        if (command =="down") and not self.is_squatting_voice:
            self.is_squatting_voice = True
            self.rect = pygame.Rect((self.rect.x, self.rect.y + 90, 80, 90))
        elif (command =="up") and self.is_squatting_voice:
            self.is_squatting_voice = False
            self.rect = pygame.Rect((self.rect.x, self.rect.y - 90, 80, 180))
