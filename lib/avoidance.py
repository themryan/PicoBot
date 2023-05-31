import base

class AvoidanceAction:
    NONE = 0
    TURN = 1
    REVERSE = 2

class Avoidance:
    """
    Provides a class for gauging distance thresholds and avoiding obstacles
    """
    REVERSE_DISTANCE_THRESHOLD = 10
    BASE_DISTANCE_THRESHOLD = 50
    HYSTERESIS_DISTANCE_THRESHOLD = 60

    def __init__(self, base):
        self._base = base

        self._dist_threshold = self.BASE_DISTANCE_THRESHOLD
        self._dist_threshold = 0
        self._threshold_count = 0

        self.distance = 0

    def obstacles(self) -> AvoidanceAction:
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
