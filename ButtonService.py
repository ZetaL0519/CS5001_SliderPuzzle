"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is ButtonService helper file for the project
"""

import turtle
import ValidationService

BUTTON_WIDTH = 64
BUTTON_HEIGHT = 64
RELOAD_INPUT = "Enter the name of the puzzle you wish to load. Choices are:/n"
QUIT_BUTTON = 'quitbutton.gif'
LOAD_BUTTON = 'loadbutton.git'
RESET_BUTTON = 'resetbutton.gif'
LIST_NUM = []


class ButtonService:
    def __init__(self, button, x, y, screen, message=None):
        """
        Constructor Function
        :param button: (str) picture name of the button
        :param x: (int) x coordinate of the button
        :param y: (int) y coordinate of the button
        :param screen: turtle.screen of the game board
        :param message: (str) warning pic name of the button
        Default to None
        """
        self.s = screen
        self.button = button
        self.x = x
        self.y = y
        self.message = message

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.s.addshape(self.button)
        self.boundary = []
        self.file = None

    def display_button(self):
        """
        Function: display_button
        Display the button on the screen
        :return: None
        """
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.shape(self.button)
        self.t.pendown()
        self.t.showturtle()

    def get_button_boundary(self):
        """
        Function: get_button_boundary
        Get the button boundary of each button
        :return: self.boundary(list) consists of the coordinates of the boundary
        """
        x_upper_boundary = self.x + (BUTTON_WIDTH / 2)
        self.boundary.append(x_upper_boundary)
        x_lower_boundary = self.x - (BUTTON_WIDTH / 2)
        self.boundary.append(x_lower_boundary)

        y_upper_boundary = self.y + (BUTTON_HEIGHT / 2)
        self.boundary.append(y_upper_boundary)
        y_lower_boundary = self.y - (BUTTON_HEIGHT / 2)
        self.boundary.append(y_lower_boundary)

        return self.boundary

    def quit_service(self):
        """
        Function: quit_service
        Display on the screen and quit game after hitting quit button
        :return:
        """
        t = turtle.Turtle()
        t.hideturtle()

        self.s.addshape(self.message)
        t.shape(self.message)
        t.showturtle()
        t.penup()
        self.s.ontimer(t.goto(0, 0), 2000)
        self.s.ontimer(turtle.bye(), 1000)

    def remove_image(self):
        """
        Function: remove_image
        Remove the button
        :return: None
        """
        self.t.hideturtle()
        self.t.clear()
