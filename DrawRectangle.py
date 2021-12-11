"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is DrawRectangle helper file for the project
"""

import turtle


class DrawRectangle:
    def __init__(self, width, height, x, y, color, pensize):
        """
        Construction Function
        :param width: Rectangle width
        :param height: Rectangle height
        :param x: starting point x-coordinate
        :param y: starting point y-coordinate
        :param color: color of the drawing
        :param pensize: the pensize of the rectangle
        :return none
        """

        self.wid = width
        self.ht = height
        self.x = x
        self.y = y
        self.color = color
        self.pensize = pensize

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.pencolor(self.color)
        self.t.pensize(self.pensize)
        self.t.speed(0)

    def draw_shape(self):
        """
        Function: draw_shape
        Draw the shape according to the attributes
        :return: none
        """
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.pendown()

        for side in range(4):
            if side % 2 == 0:
                self.t.forward(self.wid)
                self.t.left(90)
            else:
                self.t.forward(self.ht)
                self.t.left(90)
