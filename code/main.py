import pygame as pg
import pygame.event
import sys


def print_hi(name):
    print(name)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')

        pg.display.update()
        clock.tick(60)

