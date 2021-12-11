"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is main game class for the project
"""


import turtle
import os
from glob import glob
import random
from Board import Board
from LeaderBoard import LeaderBoard
from ValidationService import ValidationService
from ButtonService import ButtonService
from Slide import Slide
from TextRectangle import TextRectangle
import math

PATH_REC = "./Resources"
PATH_IMAGE = "./Images"
RELOAD_ERROR_MSG = '/file_error.gif'
RELOAD_WARN_MSG = '/file_warning.gif'
LEADERBOARD_FILE = 'leaderboard.txt'
LEADERBOARD_ERROR_MSG = '/leaderboard_error.gif'

QUIT_BUT = "/quitbutton.gif"
LOAD_BUT = "/loadbutton.gif"
RESET_BUT = "/resetbutton.gif"
QUIT_MSG = '/quitmsg.gif'
WIN_MSG = '/winner.gif'
LOSE_MSG = "/Lose.gif"
SPLASH = "/splash_screen.gif"
PATH = glob(r'*.puz')
ENTRIES = [os.path.basename(f) for f in PATH]
CREDIT = '/credits.gif'
DEFAULT_THEME = "mario.puz"
RELOAD_INPUT = "Enter the name of the puzzle you wish to load. Choices are:/n"

QUIT_X = 350
BUTTON_Y = -255
LOAD_X = 260
RESET_X = 170
LOGO_X = 360
LOGO_Y = 270
GAME_X_START = -350
LEADERBOARD_Y_START = -185
LEADERBOARD_HEIGHT = 495


class Game:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.s = turtle.Screen()
        turtle.title("CS5001 Sliding Puzzle Game")

        self.user_name = None
        self.move_num = None
        self.valid_puz_file = None
        self.valid_leader_file = None
        self.puz_info = []

        self.blank = None
        self.logo = None
        self.tile_size = None
        self.unscrambled_slides = []
        self.slides = []
        self.num_of_slides = None
        self.player_move = 0
        self.board = Board(self.s)
        self.quit_button = ButtonService(PATH_REC + QUIT_BUT,
                                         QUIT_X, BUTTON_Y, self.s, PATH_REC + QUIT_MSG)
        self.load_button = ButtonService(PATH_REC + LOAD_BUT,
                                         LOAD_X, BUTTON_Y, self.s)
        self.reset_button = ButtonService(PATH_REC + RESET_BUT,
                                          RESET_X, BUTTON_Y, self.s)
        self.theme = ValidationService(DEFAULT_THEME,
                                       PATH_REC + RELOAD_ERROR_MSG,
                                       self.s, PATH_REC + RELOAD_WARN_MSG)
        self.leader_file = ValidationService(LEADERBOARD_FILE,
                                             PATH_REC + LEADERBOARD_ERROR_MSG, self.s)
        self.leaderboard_text = LeaderBoard(self.leader_file)

    def start_screen(self):
        """
        Function: start_screen
        Set up splash screen and input user name and moves
        :return: None
        """
        self.board.set_splash_screen(PATH_REC + SPLASH)
        self.leader_file.validate_leaderboard_file()
        self.board.user_input()
        self.move_num = self.board.get_input_num()
        self.user_name = self.board.get_input_name()

    def make_screen(self):
        """
        Function: make_screen
        Draw and write the area on the game board
        :return: None
        """
        turtle.clearscreen()
        self.board.make_game_area()
        self.board.make_button_area()
        self.board.make_leaderboard_area()
        self.leaderboard_text.read_leaderboard()

    def make_button(self):
        """
        Function: make_button
        Display all three buttons
        :return: None
        """
        self.quit_button.display_button()
        self.load_button.display_button()
        self.reset_button.display_button()

    def intro_theme(self):
        """
        Function: intro_theme
        Validate directory file and access the slide info
        :return: None
        """
        # Validate puz file
        self.theme.validate_directory_file()
        # clear the list of slides and unscrambled slides
        self.slides = []
        self.unscrambled_slides = []

        if self.theme.valid:
            # get info about number of slides, thumbnail and tile size
            self.num_of_slides = int(self.theme.dict_entry["number"])
            thumb = self.theme.dict_entry["thumbnail"]
            self.tile_size = int(self.theme.dict_entry['size'])
            self.logo = ButtonService(thumb, LOGO_X, LOGO_Y, self.s)

            # iterate through all the slide images
            i = 1
            while i <= self.num_of_slides:
                name = self.theme.dict_entry[str(i)]
                self.theme.validate_image(name)
                # create slide class with name, screen and size
                slide = Slide(name, self.s, self.tile_size)
                # search for the blank slide
                slide.check_blank_status()
                self.unscrambled_slides.append(slide.name)
                self.slides.append(slide)
                i += 1

                # identify blank slide
                if slide.blank:
                    self.blank = slide

    def create_slide_page(self):
        """
        Function: create_slide_page
        Draw slides on the screen
        :return: None
        """
        slide_x_start = GAME_X_START + self.tile_size
        slide_y_start = LEADERBOARD_Y_START + LEADERBOARD_HEIGHT - 90

        self.logo.display_button()
        # customize each puzzle size row
        row_num = math.sqrt(self.num_of_slides)
        for i in range(self.num_of_slides):
            self.slides[i].position_slide(slide_x_start, slide_y_start)

            # record blank slide coordinate
            if self.slides[i].blank:
                self.blank.x = slide_x_start
                self.blank.y = slide_y_start
            # draw each row and column
            if (i + 1) % row_num == 0:
                slide_x_start = GAME_X_START + self.tile_size
                slide_y_start -= self.tile_size + 3
            else:
                slide_x_start += self.tile_size + 3

    def create_page(self):
        """
        Function: create_page
        shuffle the slides list and create game area
        :return:
        """
        random.shuffle(self.slides)
        self.create_slide_page()

    def click_check(self, x, y):
        """
        Function: click_check
        Check whether the click hits the blank slide or the button
        :param x: (float) click x coordinate
        :param y: (float) click y coordinate
        :return: None
        """

        # Get the boundary of buttons and blank slide
        quit_boundary = self.quit_button.get_button_boundary()
        reset_boundary = self.reset_button.get_button_boundary()
        load_boundary = self.load_button.get_button_boundary()

        blank_boundary = self.blank.get_boundary()
        blank_x_lower = blank_boundary[1]
        blank_y_lower = blank_boundary[3]

        # Check if the click is on the quit button
        if ((quit_boundary[1] <= x <= quit_boundary[0]) and
                (quit_boundary[3] <= y <= quit_boundary[2])):
            self.quit_button.quit_service()

        # Check if the click is on the reset button
        elif ((reset_boundary[1] <= x <= reset_boundary[0]) and
              (reset_boundary[3] <= y <= reset_boundary[2])):
            # make sure nothing happens when user hits reset button twice in a row
            reset = True
            for i in range(len(self.slides)):
                if self.slides[i].name != self.unscrambled_slides[i]:
                    reset = False

            # if first time hitting reset
            if not reset:
                # clear the slide list
                self.slides = []
                for i in range(self.num_of_slides):
                    # create new slide with unscrambled slides
                    slide = Slide(self.unscrambled_slides[i], self.s, self.tile_size)
                    slide.check_blank_status()
                    self.slides.append(slide)
                    if slide.blank:
                        self.blank = slide
                self.create_slide_page()

        # if the click hits on the load button
        elif ((load_boundary[1] <= x <= load_boundary[0]) and
              (load_boundary[3] <= y <= load_boundary[2])):
            # check if the theme is valid
            self.theme.reload_warning()
            # remove existing slides
            for i in range(len(self.slides)):
                self.slides[i].remove_slide()
            self.logo.remove_image()
            # clear player move
            self.player_move = 0
            self.board.display_player_move(self.player_move)
            self.intro_theme()
            self.create_page()

        # if the click hits on the blank slide
        else:
            for i in range(len(self.slides)):
                slide = self.slides[i]
                if not slide.blank:
                    slide_boundary = slide.get_boundary()
                    x_upper = slide_boundary[0]
                    x_lower = slide_boundary[1]
                    y_upper = slide_boundary[2]
                    y_lower = slide_boundary[3]

                    # if click hits on one slide and the slide is around the blank slide
                    if (x_lower + y_lower - self.tile_size - 3 ==
                        blank_x_lower + blank_y_lower) or \
                            (x_lower + y_lower + self.tile_size + 3 ==
                             blank_x_lower + blank_y_lower):
                        if x_lower <= x <= x_upper and \
                                y_lower <= y <= y_upper:
                            # swap cards
                            # slide and blank switch shapes and name

                            temp_name = self.blank.name
                            self.blank.switch_position(slide.name)
                            slide.switch_position(temp_name)
                            slide.blank = True
                            self.blank.blank = False
                            # redefine blank slide
                            self.blank = slide
                            self.player_move += 1
                            self.board.display_player_move(self.player_move)
                            self.check_process()
                            break

    def on_click_position(self):
        self.s.onclick(self.click_check)

    def check_process(self):
        self.lose_game()
        self.win_game()

    def check_move_num(self):
        return self.player_move <= self.move_num

    def check_win_game(self):
        """
        Function: check_win_game
        Check if the slide list is the same with the unscrambled list
        :return: None
        """
        for i in range(self.num_of_slides):
            if self.slides[i].name != self.unscrambled_slides[i]:
                return False
        return True

    def lose_game(self):
        """
        Function: lose_game
        Check if the player has lost the game with the move range
        :return: None
        """
        if not self.check_move_num() and not self.check_win_game():
            self.set_screen(PATH_REC + LOSE_MSG)
            self.set_screen(PATH_REC + CREDIT)
            self.s.ontimer(turtle.bye, 1000)

    def win_game(self):
        """
        Function: win_game
        check if the user wins the game and show the win image
        :return: None
        """
        if self.check_win_game() and self.check_move_num():
            self.leaderboard_text.update_leaderboard(self.player_move, self.user_name)
            win_image = PATH_REC + WIN_MSG
            t = turtle.Turtle()
            self.s.addshape(win_image)
            t.shape(win_image)
            t.showturtle()
            t.penup()
            self.s.ontimer(t.goto(0, 0), 2000)
            self.set_screen(PATH_REC + CREDIT)
            self.s.ontimer(turtle.bye(), 1000)

    def set_screen(self, bgpic):
        """
        Function: set_screen
        Set screen for the ending game
        :param bgpic: (str) background pic name
        :return: None
        """
        self.s.addshape(bgpic)
        self.t.shape(bgpic)
        self.t.showturtle()
        self.t.penup()
        self.s.ontimer(self.t.goto(0, 0), 2000)
