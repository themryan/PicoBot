"""
@file avoidance.py

@description This code uses the distance obtained from the base class 
             to provide an obstacle avoidance behavior

@author Michael Ryan
@date {6/18/23}
"""

import base

class AvoidanceAction:
    NONE = 0
    TURN = 1
    REVERSE = 2

class Avoidance:
    """
    @class A class for gauging distance thresholds and returning recommended avoidance actions
    """
    REVERSE_DISTANCE_THRESHOLD = 10
    BASE_DISTANCE_THRESHOLD = 50
    HYSTERESIS_DISTANCE_THRESHOLD = 60

    def __init__(self, base):
        """
        A constructor method that sets the defaults values for the 
            distance threshold
            threshold_count
            distance from any object
        """
        self._base = base

        self._dist_threshold = self.BASE_DISTANCE_THRESHOLD
        self._threshold_count = 0

        self.distance = 0

    def obstacles(self) -> AvoidanceAction:
        """
        Returns a recommended avoidance action depending on the distance of the object and passed threshold parameters
        """
        is_obstacle = AvoidanceAction.NONE
        self.distance = self._base.sonar.distance()

        if self.distance > 0 and self.distance > self._dist_threshold and self.distance > self.REVERSE_DISTANCE_THRESHOLD:
            self._threshold_count = self._threshold_count + 1
            if self._dist_threshold != self.BASE_DISTANCE_THRESHOLD and self._threshold_count < 5:
                # Turn a little bit farther in order to account for narrow focus of sonar sensors
                if self._dist_threshold > self.REVERSE_DISTANCE_THRESHOLD:
                    is_obstacle = AvoidanceAction.TURN
                else:
                    is_obstacle = AvoidanceAction.REVERSE
            else:
                self._threshold_count = 0
                self._dist_threshold = self.BASE_DISTANCE_THRESHOLD
                is_obstacle = AvoidanceAction.NONE
        elif self.distance > self.REVERSE_DISTANCE_THRESHOLD:
            self._threshold_count = 0
            self._dist_threshold = self.HYSTERESIS_DISTANCE_THRESHOLD
            is_obstacle = AvoidanceAction.TURN
        else:
            is_obstacle = AvoidanceAction.REVERSE

        return is_obstacle
