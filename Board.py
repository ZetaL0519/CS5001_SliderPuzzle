"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is Board helper file for the project
"""

import turtle
from DrawRectangle import DrawRectangle
from TextRectangle import TextRectangle
from LeaderBoard import LeaderBoard
from ValidationService import ValidationService

TEXT_INPUT = "Enter the number of moves (chances) you want (5-200)?"
MOVE_TEXT_X_START = -340
MOVE_TEXT_Y_START = -275

BUTTON_WIDTH = 770
BUTTON_HEIGHT = 105
BUTTON_Y_START = -310

LEADERBOARD_WIDTH = 250
LEADERBOARD_HEIGHT = 495
LEADERBOARD_X_START = 170
LEADERBOARD_Y_START = -185
GAME_X_START = -350
LEADERBOARD_FILE = 'leaderboard.txt'
PATH_REC = "./Resources"
LEADERBOARD_ERROR_MSG = 'leaderboard_error.gif'


class Board:
    def __init__(self, screen):
        """
        Constructor Function
        :param screen: this is turtle.screen from game
        """
        self.t = turtle.Turtle()
        self.screen = screen
        self.t.hideturtle()

        self.leaderboard_file = ValidationService(LEADERBOARD_FILE,
                                                  PATH_REC + LEADERBOARD_ERROR_MSG, self.screen)
        self.leaderboard_text = LeaderBoard(self.leaderboard_file)
        self.user_name = None
        self.number_of_moves = None
        self.x = 0
        self.y = 0

    def set_splash_screen(self, bgpic):
        """
        Function: set_splash_screen
        Set up the splash screen
        :param bgpic: splash_screen.gif
        :return: None
        """
        self.screen.addshape(bgpic)
        self.t.shape(bgpic)
        self.t.showturtle()
        self.t.penup()
        self.screen.ontimer(self.t.goto(0, 0), 1000)
        turtle.clearscreen()

    def user_input(self):
        """
        Function: user_input
        Input user name and number of moves
        :return: None
        """
        self.user_name = turtle.textinput("CS5001 Puzzle Slide", "Your Name:")

        # if the user inputs nothing for user name
        # Assume his name is "no leader"
        if self.user_name is None:
            self.user_name = "No Leader"

        self.number_of_moves = turtle.numinput("5001 Puzzle Slides - Moves",
                                               TEXT_INPUT, 10, 5, 200)
        self.validate_num_input()

    def validate_num_input(self):
        """
        Function: validate_num_input
        Validate the number of moves that user inputs is right
        :return: None
        """
        while type(self.number_of_moves) != float and \
                self.number_of_moves is not None:
            self.number_of_moves = turtle.numinput("5001 Puzzle Slides " +
                                                   "- Moves",
                                                   TEXT_INPUT, 10, 5, 200)

    def make_leaderboard_area(self):
        """
        Function: make_leaderboard_area
        Draw the leaderboard area
        :return: None
        """
        leaderboard_area = DrawRectangle(LEADERBOARD_WIDTH, LEADERBOARD_HEIGHT
                                         , LEADERBOARD_X_START,
                                         LEADERBOARD_Y_START,
                                         'blue', 8)
        leaderboard_area.draw_shape()

    def make_game_area(self):
        """
        Function: make_game_area
        Draw the gameboard area
        :return: None
        """
        game_area = DrawRectangle(LEADERBOARD_HEIGHT, LEADERBOARD_HEIGHT
                                  , GAME_X_START, LEADERBOARD_Y_START,
                                  'black', 8)
        game_area.draw_shape()

    def make_button_area(self):
        """
        Function: make_button_area
        Draw the button and move area
        :return: None
        """
        button_area = DrawRectangle(BUTTON_WIDTH, BUTTON_HEIGHT,
                                    GAME_X_START, BUTTON_Y_START, 'black', 8)
        button_area.draw_shape()

    def display_player_move(self, play_move):
        """
        Function: display_player_move
        :param play_move: (int) the moves that player has played
        :return: None
        """
        play_move_count = 'Player Moves: {}'.format(play_move)
        text = TextRectangle(self.t, play_move_count, MOVE_TEXT_X_START,
                             MOVE_TEXT_Y_START, 'black', '20')
        text.remove_text()
        text.write_text()

    def get_input_name(self):
        return self.user_name

    def get_input_num(self):
        return self.number_of_moves
