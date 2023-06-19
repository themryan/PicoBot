"""
@file exploration.py

@description This file provides code to support the exploration mode of the robot

@author Michael Ryan
@date {6/18/23}
"""

from avoidance import Avoidance, AvoidanceAction

class Exploration:
    """
    Drives the robot to explore its surroundings.  Avoiding all obstacles detected by the sonar
    """
    BASE_DISTANCE_THRESHOLD = 45
    HYSTERESIS_DISTANCE_THRESHOLD = 55

    def __init__(self, base_in):
        """
        Constructor for the Exploration class

        @param base_in Base object
        """
        self._dist_threshold = self.BASE_DISTANCE_THRESHOLD
        self._dist_threshold = 0
        self._threshold_count = 0

        self._base = base_in

        self._base.motor.velocities(75, 0)

        self._obstacles = Avoidance(self._base)

        self.__is_left = True
        self._base.output.publish("I'm exploring!")
        self._on_obstacle = False

        self._base.motor.set_accel_scale(10)
        self._base.output.screen("Chat: ", 0, 28, 2)

        self.__is_first_loop = True


    def loop(self):
        """
        Method to be used in the main loop of the code
        """
        if self._obstacles.obstacles() == AvoidanceAction.TURN:
            angular_velocity = 30
            if not self.__is_left:
                angular_velocity = -30

            self._base.motor.velocities(0, angular_velocity)
            self._base.output.screen("Obstacle...", 0, 60, 3)
            self._on_obstacle = True
        elif self._obstacles.obstacles() == AvoidanceAction.NONE:
            self._base.motor.velocities(75, 0)
            self._base.output.screen("Exploring...", 0, 60, 3)

            if self._on_obstacle:
                self.__is_left = not self.__is_left

            self._on_obstacle = False
        else:
            self._on_obstacle = True

            self._base.motor.velocities(-40, 0)
            self._base.output.screen("Obstacle...", 0, 60, 3)

        self._base.motor.drive()

        self._base.output.screen("Distance:  " + str(self._obstacles.distance), 0, 16, 1)

        messages = self._base.input.messages()
        if messages != "" or self.__is_first_loop:
            self._base.output.screen("Chat: " + messages, 0, 28, 2)

        self.__is_first_loop = False
