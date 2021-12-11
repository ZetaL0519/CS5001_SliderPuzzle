"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is TextRectangle helper file for the project
"""

import turtle


class TextRectangle:
    def __init__(self, t, text, x, y, color, pensize):
        """
        Constructor Function
        :param t: turtle that draw the text
        :param text: text sentence that is displayed
        :param x: text starting point, x-coordinate
        :param y: text starting point, y-coordinate
        :param color: color of the text
        :param pensize: pensize of the text
        :return none.,
        """
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.pensize = pensize
        self.t = t

        self.t.speed(0)
        self.t.penup()
        self.t.hideturtle()
        self.t.pencolor(self.color)

    def write_text(self):
        """"""

        self.t.goto(self.x, self.y)
        self.t.write(self.text, False, 'left', ('Arial', self.pensize, 'normal'))

    def remove_text(self):
        self.t.hideturtle()
        self.t.clear()
