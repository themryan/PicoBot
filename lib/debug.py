"""
@file dance.py

@description This code outputs standard debug info to the robot screen

@author Michael Ryan
@date {6/18/23}
"""

import base
import time
from display import Display, DebugScreen

class Debug:
    """
    This class outputs a simple screen for debugging purposes
    """
    def __init__(self, base):
        """
        Constructor method for the Debug class

        @param base Base object
        """
        self._base = base

        self._debug_screen = DebugScreen(self._base.output.display)

        self._base.output.publish("I'm debugging!")
        self._base.output.screen("Remote", 0, 16, 1)


    def loop(self):
        self._debug_screen.sonar = str(self._base.sonar.distance())

        throttle = self._base.motor.throttle
        self._debug_screen.motor = "#1 " + str(throttle[0]) + " #2 " + str(throttle[1])

        if self._base.is_connected():
            self._debug_screen.wifi_info = "Connected"
        else:
            self._debug_screen.wifi_info = "Not Connected"


        messages = self._base.input.messages(self._base.topic_pub)
        if messages != "":
            self._debug_screen.channel = messages.replace('\n', " ")


