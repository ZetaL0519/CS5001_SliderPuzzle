"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is game driver for the project
"""

import turtle
from SlideGame import Game


def main():
    game = Game()
    game.start_screen()
    game.make_screen()
    game.make_button()
    game.intro_theme()
    game.create_page()
    game.on_click_position()
    turtle.mainloop()

if __name__ == '__main__':
    main()
