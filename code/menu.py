import pygame


class Menu:
    def __init__(self, screen):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.screen = screen
        pygame.font.init()  # Initialize the font module
        self.font_title = pygame.font.Font('freesansbold.ttf', 60)
        self.font_field = pygame.font.Font('freesansbold.ttf', 40)

        self.terminate = False

    def end_menu(self,player):
        field_text = self.font_field.render("Play again? (Y/N)", True, self.WHITE)
        field_rect = field_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        title_text = self.font_title.render(player +" won the game!!!", True, self.WHITE)

        while not self.terminate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # Player chose to play again
                        self.terminate = False
                        return True
                    elif event.key == pygame.K_n:
                        # Player chose not to play again
                        self.terminate = True
                        return False

            self.screen.fill(self.BLACK)
            self.screen.blit(title_text, (250, 100))
            self.screen.blit(field_text, field_rect)
            pygame.display.flip()
