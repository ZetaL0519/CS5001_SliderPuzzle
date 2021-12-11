"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is ValidationService helper file for the project
"""

import turtle
import os
from glob import glob
import time

PATH_REC = "/Resources"
PATH_IMAGE = "/Images"
RELOAD_ERROR_MSG = 'file_error.gif'
RELOAD_WARN_MSG = 'file_warning.gif'
LEADERBOARD_ERROR_MSG = 'leaderboard_error.gif'
QUIT_MSG = 'quitmsg.gif'
PATH = glob(r'*.puz')
ENTRIES = [os.path.basename(f) for f in PATH]
RELOAD_INPUT = "Enter the name of the puzzle you wish to load. Choices are:\n"
ERROR_LEADERBOARD = "Error: Could not open leaderboard.txt. "


class ValidationService:
    def __init__(self, file, error_image, screen, warn_image=None):
        """
        Constructor Function
        :param file: (str) name of the puz file
        :param error_image: (str) name of the error image file
        :param screen: turtle.screen
        :param warn_image: (str)
         name of the warn image file
         default to None
        """
        self.file = file
        self.error_image = error_image
        self.warn_image = warn_image
        self.s = screen

        self.valid = False
        self.file_content = []
        self.dict_entry = {}
        self.valid_image = []
        self.error = None
        self.error_list = []

    def validate_leaderboard_file(self):
        """
        Function: validate_leaderboard_file
        Validate and read the leaderboard file
        :return: None
        """
        try:
            self.file_content = []
            with open(self.file, mode='r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip('\n')
                    self.file_content.append(line)
                self.valid = True

        # if the file is not found
        # log the error in the error file
        # display error image
        except FileNotFoundError:
            self.error = ERROR_LEADERBOARD
            self.error_logging()
            self.s.bgpic(self.error_image)
            self.s.ontimer(self.remove_image(), 3000)

    def validate_directory_file(self):
        """
        Function: validate_directory_file
        Validate and read the metadata in directory file
        """
        try:
            # default theme
            if self.file is None:
                self.file = "mario.puz"

            # input dict_entry from data in directory file
            with open(self.file, mode='r') as file:
                lines = file.readlines()
                for line in lines:
                    g = line.split(": ")
                    g[1] = g[1].strip("\n")
                    self.dict_entry[g[0]] = g[1]

                # check if the total image number is right
                # with the slide number given
                n = len(lines) - 1
                last = lines[n].split(":")
                if int(self.dict_entry["number"]) != int(last[0]):
                    self.valid = False
                    self.file_not_found(self.error_image)
                else:
                    self.valid = True

        # if file is not found
        # log error and display error image
        except FileNotFoundError:
            self.error = 'Error: File {} does not exist. '.format(self.file)
            self.error_logging()
            self.file_not_found(self.error_image)

    def file_not_found(self, message):
        t = turtle.Turtle()
        t.hideturtle()

        self.s.addshape(message)
        t.shape(message)
        t.showturtle()
        t.penup()
        self.s.ontimer(t.goto(0, 0), 500)
        self.s.ontimer(t.hideturtle(), 1000)

    def validate_image(self, image):
        """
        Function: validate_image
        :param image: (str) image name
        :return: None
        """
        try:
            with open(image, mode='r') as image:
                self.valid_image.append(image)

        except FileNotFoundError:
            self.error = "Error: File Image Not Found"
            self.error_logging()
            self.file_not_found(self.error_image)

    def reload_warning(self):
        """
        Function: reload_warning
        if the file not valid, keep loading file
        :return: None
        """
        self.valid = False
        while not self.valid:
            self.user_input()

    def user_input(self):
        """
        Function: user_input
        User input puzzle file
        :return: None
        """
        # more than 10 puzzle files showing first 10 warning
        if len(ENTRIES) > 10:
            self.file_not_found(self.warn_image)
        # Pop window for inputting the puzzle choice
        choices = ''
        for i in range(min(len(ENTRIES), 10)):
            choices += ENTRIES[i] + '\n'
        self.file = turtle.textinput('Load Puzzle', RELOAD_INPUT + choices)

        self.validate_directory_file()

    def remove_image(self):
        return self.s.bgpic("nopic")

    def get_valid_status(self):
        return self.valid

    def get_file_content(self):
        return self.file_content

    def error_logging(self):
        """
        Function: error_logging
        Log errors in the error file
        :return: None
        """
        with open("5001_puzzle.err", mode='a+', encoding='utf8') as err:
            err.write(f"\n"
                      f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]\n"
                      f"{self.error}\n")
