from game import Game
from menu import Menu

if __name__ == '__main__':
    while True:
        game = Game()
        menu = Menu(game.screen)
        game.run()
        menu.end_menu(game.winner)
        if menu.terminate:
            break
