"""
SIYUE LI
CS5001 Slider Puzzle
Fall 2021
This is LeaderBoard helper file for the project
"""

from ValidationService import ValidationService
import turtle
from TextRectangle import TextRectangle

LEADERBOARD_TEXT_Y_START = 270
LEADERBOARD_TEXT_X_START = 180


class LeaderBoard:
    def __init__(self, leaderboard_file):
        """
        Constructor Function
        :param leaderboard_file: it is an object from ValidationService Class
        self.file_content is a nested list that stores names and moves
        """
        self.file = leaderboard_file
        self.file_content = []

    def read_leaderboard(self):
        """
        Function: read_leaderboard
        Read leaderboard_file to see if it is valid and
        Store info in self.file_content
        :return: None
        """
        self.file.validate_leaderboard_file()
        if self.file.get_valid_status():
            leaderboard_info = self.file.get_file_content()

            # Example case: leaderboard_info = ['3: John', '5: Tay']
            for content in leaderboard_info:
                # content = [3, John] [5, Tay]
                content = content.split(" :")
                # self.file_content = [[3, John] [5, Tay]]
                self.file_content.append(content)
        self.display_leaderboard()

    def display_leaderboard(self):
        """
        Function: display_leaderboard
        Display leaderboard info in self.file_content
        :return: None
        """
        y = LEADERBOARD_TEXT_Y_START
        t = turtle.Turtle()

        # Check for empty leaderboard file
        if len(self.file_content) > 0:
            TextRectangle(t, "Leaders：", LEADERBOARD_TEXT_X_START,
                          y, 'blue', 18).write_text()
            y -= 30
            for content in self.file_content:
                if len(content) > 1:
                    player_move = content[0]
                    user_name = content[1]
                    info = ' {} : {}'.format(player_move, user_name)
                    TextRectangle(t, info, LEADERBOARD_TEXT_X_START,
                                  y,
                                  'blue', 15).write_text()
                y -= 32

        # Runs if leaderboard file is empty or doesn't exist
        else:
            TextRectangle(t, "Leaders：", LEADERBOARD_TEXT_X_START, y,
                          'blue', 15).write_text()

    def update_leaderboard(self, player_move, user_name):
        """
        Function: update_leaderboard
        Update the player record to the self.file_content
        :param player_move: int
        :param user_name: str
        :return: None
        """
        # if self.file_content is not empty
        if len(self.file_content) > 0:
            for i in range(len(self.file_content)):
                score = int(self.file_content[i][0])
                # insert in the front of the first score that is larger than player_move
                if player_move <= score:
                    new_list = [player_move, user_name]
                    self.file_content.insert(i, new_list)
                    break
                if i == len(self.file_content) - 1:
                    self.file_content.append([player_move, user_name])
        # if self.file_content is empty
        else:
            self.file_content.append([player_move, user_name])
        self.write_leaderboard()

    def write_leaderboard(self):
        """
        Function: write_leaderboard
        Write into the leaderboard.txt file according to self.file_content
        :return: None
        """
        self.file_content = self.file_content[:10]
        with open(self.file.file, mode='w') as f:
            for i in range(len(self.file_content)):
                content = self.file_content[i]
                if len(content) > 1:
                    f.write('{} :{}\n'.format(content[0], content[1]))
