import pygame


class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.health = max_health

        # colors
        self.bg_color = (255, 0, 0)  # red
        self.health_color = (0, 255, 0)  # green
        self.border_color = (47,79,79)  # dark slate gray
        self.border_width = 3

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))

        pygame.draw.rect(self.surface, self.border_color,
                         (0, 0, self.width, self.height), border_radius=5)
        pygame.draw.rect(self.surface, self.bg_color,
                         (self.border_width, self.border_width,
                          self.width-2*self.border_width, self.height-2*self.border_width),
                         border_radius=5)

    def update(self, health):
        self.health = health
        self.surface.fill((0, 0, 0, 0))

        # draw health bar
        pygame.draw.rect(self.surface, self.border_color,
                         (0, 0, self.width, self.height), border_radius=5)
        pygame.draw.rect(self.surface, self.bg_color,
                         (self.border_width, self.border_width,
                          self.width-2*self.border_width, self.height-2*self.border_width),
                         border_radius=5)
        pygame.draw.rect(self.surface, self.health_color,
                         (self.border_width, self.border_width,
                          self.health/self.max_health*(self.width-2*self.border_width),
                          self.height-2*self.border_width),
                         border_radius=5)

        font = pygame.font.SysFont('Arial', 18)
        text = font.render(f'{self.health}/{self.max_health}', True, (47,79,79))
        self.surface.blit(text, (self.width/2-text.get_width()/2, self.height/2-text.get_height()/2))

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


