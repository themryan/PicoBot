"""
@file robot_modes.py

@description This file supports the existing robot modes

@author Michael Ryan
@date {6/18/23}
"""

import os

class RobotMode:
    """
    These are the currently allowable robot modes
    """
    MODE_EXPLORE = 0
    MODE_DANCE = 1
    MODE_REMOTE = 2
    MODE_RACING = 3
    MODE_DEBUG = 4
    MODE_SLEEP = 5

    modes_strings = [
        "Explore",
        "Dance",
        "Remote",
        "Race",
        "Debug",
        "Sleep"
    ]

    modes_actions_strings = [
        "Exploring",
        "Dancing",
        "Remote",
        "Racing",
        "Debugging",
        "Sleeping"
    ]

    def __init__(self):
        self.__mode = self.MODE_DEBUG
        mode = os.getenv("ROBOT_MODE")
        if mode is not None:

            for index, mode_str in enumerate(self.modes_strings):
                if mode.lower() == mode_str.lower():
                    self.__mode = index

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode



