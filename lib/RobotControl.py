from base import Base
import adafruit_ticks

class RobotControl:
    DRIVE_MODE_NOT_ACTIVE = 0
    DRIVE_MODE_DRIVING = 1
    DRIVE_MODE_OBSTACLE = 2
    DRIVE_MODE_STUCK = 3

    WARNING_DIST = 20
    EMERGENCY_DIST = 10

    __motor_commands = [[]]

    def __init(self, base):
        self.__mode = self.DRIVE_MODE_NOT_ACTIVE
        self.__timer = 0

    def motor_commands(self, motor_commands):
        self.__motor_commands.append(motor_commands)

    def tick(self):
        base.
        if self.__timer > 0 and self.__mode == self.DRIVE_MODE_DRIVING:
            base.motor_control.drive()
            self.__timer = self.__timer - timer.ticks_ms
        elif self.__timer <= 0:
            if len(motor_commands) > 0:
                if self.__mode == self.DRIVE_MODE_DRIVING or self.__mode == self.DRIVE_MODE_NOT_ACTIVE:
                    self.base.motor_control.



