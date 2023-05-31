from base import Base
import time
import random

class BehaviorBase(BehaviorBase):
    start_time = now()

    def __init__(self, base):
        self._base = base

class Explore(BehaviorBase):

    distance_warning = 1000 #mm
    distance_stop = 10 #mm
    distance_backup = 5 #mm

    def __init__(self, base):
        super(base)
        self._base.output.output_all("I'm exploring")

        random.seed()


    def tick(self):
        base.motor.velocities(random.randint(0, 100), random.randint(0, 100))

        base.motor.drive()


class Remote(BehaviorBase):

    def __init__(self, base):
        super(base)
        self._base.output.output_all("I'm remote")

        # This will be dependent on a solid internet connection


clase Dancing:
    # Dance have format linear, angular, time in ms
    DANCE1 = [
        [0, 50, 300], [0, -50, 600], [0, 50, 300],
        [40, -30, 200], [40, -10, 200], [40, 10, 200], [40, 30, 200],
        [40, 30, 200], [40, 10, 200], [40, -10, 200], [40, -30, 200],
        [-100, 0, 1000],
        [0, 80, 200], [0, 80, 200],
    ]

    DANCE2 = [
        [100, 0, 300], [-100, 0, 300],
        [0, 80, 2000], [0, -80, 2000],

    ]

    dances = [
        DANCE1,
        DANCE2
    ]

    def __init__(self, base):
        super(base)
        self._base.output.output_all("I'm dancing")
        self.__dance_index = 0
        which_dance = random.randint(0, len(dances))
        self.__dance = dances[which_dance]


    def tick(self):
        done = False
        self.__dance_index = self.__dance_index + 1

        if self.__dance_index >= len(self.__dance):
            # Dance is over
            self.__dance_index = 0
            self._base.output_all("All done")
            done = True

        return done


