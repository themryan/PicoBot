"""
@file output.py

@description This file supports the Racing mode of the robot

@author Michael Ryan
@date {6/18/23}
"""

import base
import time
from avoidance import Avoidance, AvoidanceAction

class Racing:
    """
    @description This class will support the Racing mode will race in a large circle while avoiding obstacles
    """
    BASE_DISTANCE_THRESHOLD = 45
    HYSTERESIS_DISTANCE_THRESHOLD = 55

    def __init__(self, base):

        self._dist_threshold = self.BASE_DISTANCE_THRESHOLD
        self._threshold_count = 0

        self._base = base
        self._base.output.publish("I'm racing!")
        self.__obstacles = Avoidance(self._base)

        self._base.motor.set_accel_scale(10)

        self._base.motor.velocities(0, 0)

        now = time.monotonic_ns()
        self._countdown_time = now + 4e+9 # Countdown for 3 seconds
        self._tick_time = now

        self._racing_velocities = [100, 0]
        self._countdown = 1

    def loop(self):

        now = time.monotonic_ns()
        distance = self._base.sonar.distance()

        if now > self._countdown_time:
            self._racing_velocities = [80, -20]


            if self.__obstacles.obstacles() == AvoidanceAction.NONE:
                self._base.motor.velocities(self._racing_velocities[0], self._racing_velocities[1])
                self._base.output.screen("Racing...", 0, 60, 2)
            elif self.__obstacles.obstacles() == AvoidanceAction.TURN:
                self._base.motor.velocities(60, -40)
                self._base.output.screen("Obstacle...", 0, 60, 2)
            else:
                self._base.motor.velocities(-40, 0)
                self._base.output.screen("Obstacle...", 0, 60, 2)

            self._base.motor.drive()

            self._base.output.screen("Distance:  " + str(self.__obstacles.distance), 0, 16, 1)
            self._base.output.screen("Chat: " + self._base.input.messages(), 0, 28, 3)

        else:
            if now - self._tick_time >= 1e+9:
                if self._countdown < 3:
                    self._countdown = self._countdown + 1
                    self._base.output.screen(str(self._countdown), 54, 36, 1, 5)
                else:
                    self._base.output.screen("GO!", 36, 36, 1, 5)
                    self._base.motor.velocities(100, 0)
                    self._base.motor.drive()

                self._tick_time = now



